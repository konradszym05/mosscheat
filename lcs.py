from typing import List
from utils import tokenize_code


def lcs(seq_a: List[str], seq_b: List[str]) -> int:
    """
    Counts the longest common subsequence between two sequences.
    Args:
        seq_a (List[str]): The first sequence.
        seq_b (List[str]): The second sequence.
    Returns:
        int: Length of the longest common subsequence.
    """
    m = len(seq_a)
    n = len(seq_b)

    dp = [[0] * (n + 1) for x in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq_a[i - 1] == seq_b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


def compute_lcs(code_1: str, code_2: str) -> float:
    tok1 = tokenize_code(code_1)
    tok2 = tokenize_code(code_2)
    #return lcs(tok1, tok2)/len(tok1)
    return (2.0 * lcs(tok1,tok2)) / (len(tok1) + len(tok2))
