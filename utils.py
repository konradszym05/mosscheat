import re
import ast
import builtins
import keyword
from typing import List, Tuple, Set


def remove_comments_and_docstrings(code: str) -> str:
    """
    Remove comments and docstrings from a block of Python source code.

    This function strips:
      - Single-line comments (starting with '#')
      - Multi-line comments and docstrings enclosed in triple quotes
    It does not modify indentation or non-comment code structure.

    Args:
        code (str): The raw Python source code as a string.

    Returns:
        str: The code with all comments and docstrings removed.
    """
    code = re.sub(r"#.*", "", code)
    code = re.sub(r'("""|\'\'\')(?:.|\n)*?\1', "", code)
    return code.strip()


def normalize_code(code: str) -> Tuple[str, dict]:
    """
    Normalize Python code by replacing user-defined names with placeholders.

    Specifically, it performs the following transformations:
      - Replace user-defined variable names with "<VAR>"
      - Replace user-defined function names with "<FUNC>"
      - Replace user-defined class names with "<CLASS>"
      - Preserve indentation (crucial for Python syntax)
      - Remove empty or comment-only lines
      - Retain built-in names and keywords unchanged

    The function parses the source code into an AST, identifies user-defined names,
    and reconstructs a normalized version of the code using `ast.unparse()`.

    Args:
        code (str): The input Python source code.

    Returns:
        Tuple[str, dict]:
            - The first element is the normalized code as a string.
            - The second element is a dictionary containing sets of:
                {
                    "variables": {user variable names},
                    "functions": {user function names},
                    "classes": {user class names}
                }

    Example:
        >>> normalize_code("class MyClass:\\n    pass\\nobj = MyClass('Test')")
        ('class <CLASS>:\\n    pass\\n<VAR> = <CLASS>(<STR>)',
         {'variables': {'obj'}, 'functions': set(), 'classes': {'MyClass'}})
    """

    def name_is_builtin(name):
        return name in dir(builtins) or keyword.iskeyword(name)

    code_clean = remove_comments_and_docstrings(code)
    if not code_clean.strip():
        return "", {}

    tree = ast.parse(code_clean)

    # First pass: collect function & class names
    class Collector(ast.NodeVisitor):
        def __init__(self):
            self.funcs: Set[str] = set()
            self.classes: Set[str] = set()
            self.import_aliases: Set[str] = set()

        def visit_FunctionDef(self, node):
            if not name_is_builtin(node.name):
                self.funcs.add(node.name)
            self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node):
            if not name_is_builtin(node.name):
                self.funcs.add(node.name)
            self.generic_visit(node)

        def visit_ClassDef(self, node):
            if not name_is_builtin(node.name):
                self.classes.add(node.name)
            self.generic_visit(node)

        def visit_Import(self, node):
            for alias in node.names:
                if alias.asname:
                    self.import_aliases.add(alias.asname)
            self.generic_visit(node)

        def visit_ImportFrom(self, node):
            for alias in node.names:
                if alias.asname:
                    self.import_aliases.add(alias.asname)
            self.generic_visit(node)

    collector = Collector()
    collector.visit(tree)

    # Second pass: normalization
    class Normalizer(ast.NodeTransformer):
        def __init__(self, funcs, classes, import_aliases):
            self.vars: Set[str] = set()
            self.funcs = funcs
            self.classes = classes
            self.import_aliases = import_aliases

        def visit_Name(self, node):
            if isinstance(node.ctx, (ast.Store, ast.Load, ast.Del)):
                if node.id in self.funcs:
                    node.id = "<FUNC>"
                elif node.id in self.classes:
                    node.id = "<CLASS>"
                elif node.id in self.import_aliases:
                    # Do not normalize import aliases
                    return node
                elif not name_is_builtin(node.id):
                    self.vars.add(node.id)
                    node.id = "<VAR>"
            return node

        def visit_arg(self, node):
            if not name_is_builtin(node.arg):
                self.vars.add(node.arg)
                node.arg = "<VAR>"
            return node

        def visit_FunctionDef(self, node):
            if not name_is_builtin(node.name):
                node.name = "<FUNC>"
            self.generic_visit(node)
            return node

        def visit_AsyncFunctionDef(self, node):
            if not name_is_builtin(node.name):
                node.name = "<FUNC>"
            self.generic_visit(node)
            return node

        def visit_ClassDef(self, node):
            if not name_is_builtin(node.name):
                node.name = "<CLASS>"
            self.generic_visit(node)
            return node

        def visit_Attribute(self, node):
            self.generic_visit(node)

            # Check if the base of the attribute is user-defined (<VAR> or <CLASS>)
            if isinstance(node.value, ast.Name) and node.value.id in {
                "<VAR>",
                "<CLASS>",
            }:
                if not name_is_builtin(node.attr):
                    self.vars.add(node.attr)
                    node.attr = "<VAR>"

            return node

    normalizer = Normalizer(
        collector.funcs, collector.classes, collector.import_aliases
    )
    tree = normalizer.visit(tree)
    ast.fix_missing_locations(tree)
    normalized_code = ast.unparse(tree)

    # Keep indentation but remove blank lines
    normalized_code = "\n".join(
        line.rstrip() for line in normalized_code.splitlines() if line.strip()
    )
    normalized_code = re.sub(r"\n{2,}", "\n", normalized_code)
    normalized_code = normalized_code.strip("\n")

    return normalized_code, {
        "variables": normalizer.vars,
        "functions": collector.funcs,
        "classes": collector.classes,
    }


TOKEN_REGEX = re.compile(
    r"""
        (==|!=|<=|>=|\+\+|--|\+=|-=|\*=|/=|&&|\|\||::|->|=>|<<|>>|===|
        [A-Za-z_]\w* |
        \d+\.\d+\.\d+\.\d+ | \d+\.\d+ | \d+ |
        [()\[\]{};,.<>+\-*/%=&|^!~?:]
        )
    """,
    re.VERBOSE,
)


def tokenize_code(code: str) -> List[str]:
    """
    Tokenize a code string into a list of tokens.
    The function first removes comments and docstrings. It then uses
    TOKEN_REGEX to find all matching tokens. A token is
    defined as a word (name of variable or function or
    an operator or separator for example: +, ==,; and so on.
    Args:
        code:
    Returns:
        List[str]: A list of tokens.
    """
    code = remove_comments_and_docstrings(code)
    return [m.group(0) for m in TOKEN_REGEX.finditer(code)]
