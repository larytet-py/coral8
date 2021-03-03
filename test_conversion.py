import pytest

quotes = {}
def quote_listener(base, target, rate):
    quotes[f"base:target"] = rate

def test_quotes():
    pairs = [("USD","ILS"), ("USD", "GBP")]
    quotes = Quotes(pairs, 6.0, [quote_listener])
    time.sleep(6.1)
    for base, target in pairs:
