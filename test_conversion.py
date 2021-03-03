import pytest
import conversion
import time

collected_quotes = {}
def get_key(base, target):
    return (base, target)

def quote_listener(base, target, rate):
    collected_quotes[get_key(base, target)] = rate

class QuotesMock():
    '''
    Serve quotes in a specific order
    I do not care about the actual pair
    '''
    def __init__(self, quotes):
        self.quotes = quotes
        self.quote_idx = 0

    def get_quote(self, base, target):
        rate, err = self.quotes[self.quote_idx]
        self.quote_idx += 1
        return rate, err

def test_quotes_async():
    mock_data = [(0.3, None), (0.5, None), (0.3, None), (0.5, None)]
    quotes_mock = QuotesMock(mock_data)
    pairs = [("USD","ILS"), ("USD", "GBP")]
    quotes = conversion.Quotes(quotes_mock.get_quote, pairs, 1.0, [quote_listener])
    quotes.close()
    idx = 0
    for base, target in pairs:
        key = get_key(base, target)
        assert key in collected_quotes, f"Key {key} is missing in quotes"
        rate = collected_quotes[key]
        expected_rate = mock_data[idx][0]
        assert rate == expected_rate, f"Actual {rate} expected {expected_rate}"
        idx += 1

def test_quotes_sync():
    mock_data = [(0.3, None), (0.3, None)]
    quotes_mock = QuotesMock(mock_data)
    pairs = [("USD","ILS")]
    quotes = conversion.Quotes(quotes_mock.get_quote, pairs, 1.0, [])
    quotes.close()
    rate, err = quotes.quote("USD", "ILS")
    assert err == None, f"Error is not None {err}"    
    expected_rate = mock_data[0][0]
    assert rate == expected_rate, f"Actual {rate} expected {expected_rate}"
    rate, err = quotes.quote("GBP", "ILS")
    assert err != None, f"Error is None {err}"


def test_quotes_sync_error():
    mock_data = [(0.3, "error")]
    quotes_mock = QuotesMock(mock_data)
    pairs = [("BOB","ILS")]
    quotes = conversion.Quotes(quotes_mock.get_quote, pairs, 1.0, [])
    quotes.close()
    rate, err = quotes.quote("BOB", "ILS")
    assert err != None, f"Error is None"    

