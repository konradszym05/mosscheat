# from https://github.com/soachishti/moss.py
import os
from dotenv import load_dotenv
import socket

"""To run this locally:
        1.  Register for a free MOSS account by following the
            instructions at: https://theory.stanford.edu/~aiken/moss/
        2.  You will receive your User ID (a number) via email.
        3.  Create a file named `.env` in the root of this project.
        4.  Add your ID to the file like this:
            MOSS_USER_ID=123456789
"""


class MossDetector:
    languages = (
        "c",
        "cc",
        "java",
        "ml",
        "pascal",
        "ada",
        "lisp",
        "scheme",
        "haskell",
        "fortran",
        "ascii",
        "vhdl",
        "verilog",
        "perl",
        "matlab",
        "python",
        "mips",
        "prolog",
        "spice",
        "vb",
        "csharp",
        "modula2",
        "a8086",
        "javascript",
        "plsql",
    )
    server = "moss.stanford.edu"
    port = 7690

    def __init__(self, user_id, language="c"):
        self.user_id = user_id
        self.options = {"l": "c", "m": 10, "d": 0, "x": 0, "c": "", "n": 250}
        self.codes = []

        if language in self.languages:
            self.options["l"] = language

    def add_code_snippet(self, code: str, filename: str | None = None):
        """
        Adds a code snippet to the list for later submission.

        This method stages a file for upload. It accepts code as either a string or bytes. If bytes
        are provided, they will be decoded.

        Args:
            code (str | bytes): The source code snippet to analyze.
            filename (str | None): An optional display name for the code,
                used in the  report.

        Raises:
            TypeError: If 'code' is not an instance of str or bytes.
        """
        if not isinstance(code, (str, bytes)):
            raise TypeError("code must be str or bytes")
        text = code if isinstance(code, str) else code.decode("utf-8", "ignore")
        self.codes.append((filename, text))

    def upload_string(self, sock, code: str, filename: str, index: int):
        """
        Uploads a single code snippet over the  socket connection.

        This is a method responsible for sending the file
        according to the MOSS protocol. It constructs a MOSS-specific
        header, sends the header, and then sends the code data.
        """
        data = code.encode("utf-8")
        header = f"file {index} {self.options['l']} {len(data)} {filename}\n".encode(
            "utf-8"
        )
        sock.sendall(header)
        sock.sendall(data)

    def send(self, on_send=lambda file_path, display_name: None):
        """
        Organize the connection and submission process to MOSS.

        This method connects to the MOSS server, sends all  options,
        iterates over all staged codes (using `upload_string` for each),
        and sends the final query command. It then waits for the server's
        response, which is the URL to the results.
        """
        s = socket.socket()
        s.connect((self.server, self.port))

        def w(msg):
            s.send(msg.encode("utf-8"))

        w(f"moss {self.user_id}\n")
        w(f"directory {self.options['d']}\n")
        w(f"X {self.options['x']}\n")
        w(f"maxmatches {self.options['m']}\n")
        w(f"show {self.options['n']}\n")

        w(f"language {self.options['l']}\n")
        recv = s.recv(1024).decode()

        if recv.startswith("no"):
            w("end\n")
            s.close()
            raise Exception("send() => Language not accepted by server")

        index = 1
        for filename, code in self.codes:
            self.upload_string(s, code, filename, index)
            if on_send:
                on_send(filename, filename)
            index += 1
        w(f"query 0 {self.options['c']}\n")
        response = s.recv(1024)
        w("end\n")

        return response.decode().strip()

    @staticmethod
    def get_moss_user_id() -> str:
        """
        Retrieves the moss user id from environment variable.
        This method can load MOSS user ID from both production and local development environments.

        - Production (for example Gh Actions): MOSS_USER_ID is expected to be set as an environment variable for example in GitHub Secrets.
        - Local Development: If the ENV variable is not set to 'production' this method will try to load
        environment variable from .env file in the project's root directory using load_dotenv().

        """
        if os.getenv("ENV") != "production":
            load_dotenv()
        moss_id = os.getenv("MOSS_USER_ID")
        if not moss_id:
            raise RuntimeError("MOSS_USER_ID must be set")
        return moss_id

    @classmethod
    def compute_similarity(cls, code_1: str, code_2: str, lang: str = "python", filename1="first_solution.py", filename2="second_solution.py"):
        """
        Computes similarity between two code strings using MOSS.
        - Initializes the detector
        - Adds both code strings
        - Sends them to MOSS for comparison
        """
        m = cls(user_id=cls.get_moss_user_id(), language=lang)
        m.add_code_snippet(code_1, filename1)
        m.add_code_snippet(code_2, filename2)

        return {"url": m.send()}

    # TODO Implement a method that will get users solutions and store them into a map
    # where key is users id and value is a code casted to the string and this map can be passed to the 'compute_similarity_batch'
    @classmethod
    def compute_similarity_batch(cls, codes_dict: dict, lang: str = "python"):
        """
        This method compares series of code snippets using MOSS.
        This is preferred method for comparing n>2 snippets.
        """
        user_id = cls.get_moss_user_id()
        m = cls(user_id=user_id, language=lang)
        for filename, code in codes_dict.items():
            m.add_code_snippet(code, filename)

        url = m.send()
        return {"url": url}



