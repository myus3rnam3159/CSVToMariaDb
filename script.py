import csv

def createTable(): 
    data_sources = ["type_data.csv", "toscast_data.csv"]
    for source in data_sources:
        with open(source, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)

if __name__ == '__main__':
    createTable()