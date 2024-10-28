from typing import List, Tuple
import csv
import mariadb
from mariadb import Connection
from datetime import  datetime

type_col_types: List[str] = ["DATETIME", "VARCHAR(10)", "VARCHAR(1)", "INT", "INT", "INT", "INT", "INT", "DECIMAL", "INT", "VARCHAR(10)"]
toscast_types: List[str] = ["DATETIME", "VARCHAR(10)", "VARCHAR(10)", "INT", "DECIMAL", "INT", "DECIMAL", "DECIMAL", "INT", "DECIMAL", "DECIMAL"]

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

def remove_quotation_marks(list: List[str]) -> List[str]:
    cleaned_data = []
    for s in list:
        cleaned_data.append(s.replace("'", ""))
    return cleaned_data

def format_values_sql(vals: List[str], types: List[str]) -> str:
    sql: str = ", "

    values: List[str] = []
    for index, v in enumerate(vals):

        if types[index] in ["INT", "DECIMAL"]:
            temp: str = v.replace("'", "")
            if v != '':
                values.append(temp)
            else:
                values.append('NULL'.replace("'", ""))
        elif types[index] == "DATETIME":
            values.append(f"'{v}'")
        else:
            values.append(v)

    return sql.join(values)

def gen_insert_sql(table: str, cols: List[str], data: List[str]) -> str:
    if len(cols) != len(data):
        raise ValueError("The number of columns and data values must match!")

    column_list: str
    value_list: str

    if table == "type_data":
        cols.pop()
        column_list = ", ".join(cols)

        data.pop()
        value_list = format_values_sql(data, type_col_types)


    sql = f"INSERT INTO {table} ({column_list}) VALUES ({value_list});"
    print(f"Insert sql statement: {sql}\n")
    return sql


data_sources = ["type_data.csv"]

if __name__ == "__main__":

    conn = create_connection()

    for source in data_sources:
        statement: str;
        with open(source, 'r') as file:

            reader = csv.reader(file)
            headers = next(reader)

            for row in reader:
                statement = gen_insert_sql(source.replace(".csv", ""), remove_quotation_marks(headers), row)

                try:
                    conn.cursor().execute(statement)
                except Exception as e:
                    print(f"Error while inserting new data row to type_data table: {e}")
