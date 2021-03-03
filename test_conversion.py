import pytest

quotes = {}
def get_key(base, target):
    return f"base:target"

def quote_listener(base, target, rate):
    quotes[get_key(base, target)] = rate

def test_quotes_async():
    pairs = [("USD","ILS"), ("USD", "GBP")]
    quotes = Quotes(pairs, 6.0, [quote_listener])
    time.sleep(6.1)
    for base, target in pairs:
        key = get_key(base, target)
        assert key in quotes, f"Key {key} is missing in quotes"
    quotes.close()

def test_quotes_sync():
    pairs = [("USD","ILS")]
    quotes = Quotes(pairs, 6.0, [quote_listener])
    time.sleep(1.0)
    rate, err = quotes.quote("USD", "ILS")
    assert err == None, f"Error is not None {err}"    
    rate, err = quotes.quote("GBP", "ILS")
    assert err != None, f"Error is None {err}"
    quotes.close()

