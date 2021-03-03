import pytest


def test_quotes():
    pairs = [("USD","ILS"), ("USD", "GBP")]
    quotes = Quotes(pairs, 6.0, )