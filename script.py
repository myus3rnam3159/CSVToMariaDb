import csv

from mariadb import Connection
import mariadb
from typing import List, Tuple

def createConnection() -> Connection :
    try:
        conn_params = {
            "user": "root",
            "password": "root",
            "host": "localhost",
            "port": 3306,
            "database": "equipment",
        }
        con = mariadb.connect(**conn_params)
        print("Connected to mariadb successfully\n")
        return con
    except mariadb.Error as e:
        print(f"Error connecting to the database: {e}\n")

def removeQuotationMarks(list:List[str]) -> [str]:
    cleaned_data = []
    for s in list:
        cleaned_data.append(s.replace("'", ""))
    return cleaned_data

def getTableMetadata() -> List[Tuple[str, List[str]]]:
    data_sources = ["type_data.csv", "toscast_data.csv"]

    result: List[Tuple[str, List[str]]] = []
    for source in data_sources:

        with open(source, 'r') as file:
            reader = csv.reader(file)

            result.append(
                (source.replace(".csv", ""), removeQuotationMarks(next(reader)))
            )
    return result

if __name__ == '__main__':
    metas = getTableMetadata()
    print(metas)
    conn = createConnection()


