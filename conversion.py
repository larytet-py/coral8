import requests

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
    r =requests.get(url)
    status_code = r.status_code
    if r.status_code != HTTPStatus.OK:
        print(f"Got status {status_code} from {url}")
        return None, False

def execute_commands(commands_file):
    for fields_tuple in csv_file(commands_file):
        base, sum_s, target = fields_tuple
        sum = int(sum_s)

def main():
    commands_file = open(sys.argv[1], 'r')
    commands = execute_commands(commands_file)
    commands_file.close()
