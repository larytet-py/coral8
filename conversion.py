

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

def execute_commands(commands_file):
    for fields_tuple in csv_file(commands_file):
        base, sum_s, target = fields_tuple
        sum = int(sum_s)

def main():
    commands_file = open(sys.argv[1], 'r')
    commands = execute_commands(commands_file)
    commands_file.close()
