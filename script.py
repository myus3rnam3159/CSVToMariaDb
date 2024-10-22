import csv
import mariadb

def createTables(): 
    data_sources = ["type_data.csv", "toscast_data.csv"]
    for source in data_sources:
        with open(source, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)
conn_params = {
    "user": "root",
    "password": "root",
    "host": "localhost",
    "port": "3306",
    "database": "equipment",
}

if __name__ == '__main__':
    createTables()