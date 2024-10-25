import csv

from mariadb import Connection
import mariadb
from typing import List, Tuple


def create_connection() -> Connection:
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


def remove_quotation_marks(list: List[str]) -> [str]:
    cleaned_data = []
    for s in list:
        cleaned_data.append(s.replace("'", ""))
    return cleaned_data


def get_table_metadata() -> List[Tuple[str, List[str]]]:
    data_sources = ["type_data.csv", "toscast_data.csv"]

    result: List[Tuple[str, List[str]]] = []
    for source in data_sources:
        with open(source, 'r') as file:
            reader = csv.reader(file)

            result.append(
                (source.replace(".csv", ""), remove_quotation_marks(next(reader)))
            )
    return result


def gen_column_name_sql(col_names: List[str], data_types: List[str]) -> str:
    if len(col_names) != len(data_types):
        raise ValueError("The number of columns and data types must match!")
    return ", ".join(f"(col) (dtype)" for col, dtype in zip(col_names, data_types))

type_col_types: List[str] = ["DATETIME", "VARCHAR(10)", "VARCHAR(1)", "INT", "INT", "INT", "INT", "INT" "DECIMAL", "VARCHAR(100)", "VARCHAR"]
toscast_types: List[str]

if __name__ == '__main__':
    metas = get_table_metadata()
    print(metas)
    conn = create_connection()

    for table_name, column_names in metas:
        if table_name == "type_data":

            column_names.pop()
            create_table_sql = f"CREATE TABLE {table_name} ({gen_column_name_sql(column_names, typedata_col_types)})"

            print(f"{create_table_sql}\n")
