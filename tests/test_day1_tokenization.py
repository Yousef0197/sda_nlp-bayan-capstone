from bayan.tokenization import corpus_fertility, token_fertility, truncation_rate


def toy_tokenize(text: str) -> list[str]:
    return text.replace("الخدمة", "ال خدمة").split()


def test_fertility():
    assert token_fertility("الخدمة ممتازة", toy_tokenize) == 1.5
    assert corpus_fertility(["الخدمة ممتازة", "سريع"], toy_tokenize) == 1.25


def test_truncation_rate_reserves_special_tokens():
    texts = ["a b", "a b c d"]
    assert truncation_rate(texts, str.split, max_length=5, special_tokens=2) == 0.5


def test_arabic_clitic_wabialkhidma():
    """Distinction: connected Arabic clitics must be tested explicitly."""

    base_tokens = toy_tokenize("الخدمة")
    clitic_tokens = toy_tokenize("وبالخدمة")

    assert base_tokens == ["ال", "خدمة"]
    assert clitic_tokens == ["وبال", "خدمة"]

    # كلمة واحدة بحسب الفراغات، لكنها قد تصبح عدة رموز بعد الترميز.
    assert token_fertility("وبالخدمة", toy_tokenize) == 2.0
