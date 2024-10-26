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
    return ", ".join(f"{col} {dtype}" for col, dtype in zip(col_names, data_types))

type_col_types: List[str] = ["DATETIME", "VARCHAR(10)", "VARCHAR(1)", "INT", "INT", "INT", "INT", "INT", "DECIMAL", "VARCHAR(100)", "VARCHAR(10)"]
toscast_types: List[str] = ["DATETIME", "VARCHAR(10)", "VARCHAR(10)", "INT", "DECIMAL", "INT", "DECIMAL", "DECIMAL", "INT", "DECIMAL", "DECIMAL"]

def genSQLCreateTable(table: str, columns: str) -> str:
    return f"CREATE TABLE {table} (id INT AUTO_INCREMENT, {columns}, PRIMARY KEY(id), UNIQUE KEY (id));"

if __name__ == '__main__':
    metas = get_table_metadata()
    print(metas)
    conn = create_connection()

    result_table_cols: list[str]

    for table_name, column_names in metas:
        if table_name == "type_data":

            column_names.pop()
            sql = genSQLCreateTable(
                table_name,
                gen_column_name_sql(column_names, type_col_types)
            )

            result_table_cols = column_names
            print(f"{sql}\n")

        elif table_name == "toscast_data":
            sql = genSQLCreateTable(
                table_name,
                gen_column_name_sql(column_names, toscast_types)
            )
            print(f"{sql}\n")

            result_table_cols = result_table_cols + column_names[2:]

    print(f"{result_table_cols}\n")

    result_table = "result"