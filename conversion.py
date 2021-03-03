import sys
import requests
from http import HTTPStatus
import threading
import time
import csv

def csv_file(input_file):
    '''
    read the file, yield fields of the CSV
    Use pandas?
    '''
    csvreader = csv.DictReader(input_file)
    for row in csvreader:
        yield row

class QuotesExchangeratesapi():
    def __init__(self):
        pass

    def get_quote(self, base, target):
        '''
        Send query like this 
        https://api.exchangeratesapi.io/latest?base=USD&symbols=ILS
        Expect {"rates":{"ILS":3.300631859},"base":"USD","date":"2021-03-02"}
        check status, parse JSON, return rate
        '''
        url = f"https://api.exchangeratesapi.io/latest?base={base}&symbols={target}"
        response = requests.get(url)
        status_code = response.status_code
        if response.status_code != HTTPStatus.OK:
            err = f"Got status {status_code} from {url}"
            return None, err
        content = response.json()
        rates = content["rates"]
        rate = float(rates[target])
        return rate, None

class Quotes():
    def __init__(self, get_quote_cb, pairs, polling_time, listeners):
        '''
        get_quote_cb is a function(base, target) returning a quote, can be None
        pairs: [("USD","ILS"), ("USD", "GBP")]
        polling_time (seconds): 6.0
        listeners [function(base, target, rate) - called asynchronously 
        '''
        if get_quote_cb is None:
            get_quote_cb = get_quote
        self.pairs, self.polling_time = pairs, polling_time
        self.listeners, self.get_quote = listeners, get_quote_cb
        self.exit_flag = False
        self.rates = {}
        self.job = threading.Thread(target=self.poll_quotes)
        self.job.start()
    
    def key(self, base, target):
        return f"{base}:{target}"

    def poll_quotes(self):
        new_data = []
        while not self.exit_flag:
            for base, target in self.pairs:
                rate, err = self.get_quote(base, target)
                if err != None:
                    print(f"Failed to get a quote for {base}/{target}:{err}")
                    continue
                key = self.key(base, target)
                #print(f"Got quote {base} {target} {rate}")
                if (not key in self.rates) or (self.rates[key] != rate):
                    self.call_listeners(base, target, rate)
                self.rates[key] = rate
            # Cutting corners: I need a ticker here to avoid drift
            time.sleep(self.polling_time)

    def close(self):
        self.exit_flag = True
        self.job.join()

    def call_listeners(self, base, target, rate):
        for listener in self.listeners:
            # Cutting corners: I assume listener is a non-blocking function
            listener(base, target, rate)

    def quote(self, base, target):
        key = self.key(base, target)
        if not key in self.rates:
            return None, f"No match for the pair {base}:{target}"

        return self.rates[key], None

def execute_orders(orders_file):
    orders_file.seek(0)
    pairs = []
    for row in csv_file(orders_file):
        base, target = row["Base"], row["Target"]
        pairs.append((base, target))

    quotes = Quotes(QuotesExchangeratesapi().get_quote, pairs, 1.0, [])
    # I wait for the first loop to complete
    quotes.close() 

    order_id = 0
    orders_file.seek(0)
    for row in csv_file(orders_file):
        order_id += 1
        base, target, sum = row["Base"], row["Target"], float(row["Sum"])
        # quotes is closed, but I canm stil access the collected data!
        rate, err = quotes.quote(base, target)  
        if err != None:
            print(f"{order_id} from {base} to {target} sum {sum} conversion failed {err}")
            continue

        order_amount = rate * sum
        print(f"{order_id}  {sum}{base} to {target}  rate {rate} total {order_amount}{target}")


def main():
    print("Currency converter")
    orders_file = open(sys.argv[1], 'r')
    orders = execute_orders(orders_file)
    orders_file.close()

if __name__ == "__main__":
    main()
