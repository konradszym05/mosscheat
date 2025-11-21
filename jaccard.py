from typing import List
from utils import normalize_code


def compute_jaccard_similarity(code_1: str, code_2: str, n: int) -> float:
    """
    Args:
        code_1, code_2: str - two code snippets
        n: int - how many tokens are taken into account

    Return:
        float - jaccard similarity between two pieces of code

    Steps:
    1. Normalize both code snippets.
    2. Build token n-grams.
    3. Convert into sets and compute Jaccard similarity.
    """
    norm1 = normalize_code(code_1)[0]
    norm2 = normalize_code(code_2)[0]

    tokens1 = norm1.split()
    tokens2 = norm2.split()

    # using n-grams to capture local token context
    ngrams1 = build_ngrams(tokens1, n)
    ngrams2 = build_ngrams(tokens2, n)

    set1 = set(ngrams1)
    set2 = set(ngrams2)

    # safeguard against 0/0
    if not set1 and not set2:  # both empty -> dissmiliar
        return 0.0
    if not set1 or not set2:  # one empty -> dissimiliar
        return 0.0

    # Jaccard similarity
    intersection = len(set1 & set2)
    union = len(set1 | set2)

    return intersection / union


def build_ngrams(tokens: List[str], n: int) -> List[str]:
    """
    Build token n-grams (sliding window of size n) to keep local context.
    """
    if len(tokens) < n:
        return []

    num_ngrams = len(tokens) - n + 1
    result = []
    for i in range(num_ngrams):
        window = tokens[i : i + n]
        ngram = " ".join(window)
        result.append(ngram)

    return result
