import sys
import requests
from http import HTTPStatus

def csv_file(input_file):
    '''
    read the file, yield fields of the CSV
    Use pandas?
    '''

    input_file.readline()  # skip the first line
    for line in input_file:
        fields = line.split(",")
        result = []
        for f in fields:
            f = f.strip()
            result.append(f)
        yield tuple(result)

def get_quote(base, target):
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

def execute_orders(orders_file):
    order_id = 0
    for fields_tuple in csv_file(orders_file):
        order_id += 1
        base, sum_s, target = fields_tuple
        sum = float(sum_s)
        rate, err = get_quote(base, target)
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



