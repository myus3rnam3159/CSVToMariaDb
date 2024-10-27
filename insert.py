from typing import List, Tuple
import csv

type_col_types: List[str] = ["DATETIME", "VARCHAR(10)", "VARCHAR(1)", "INT", "INT", "INT", "INT", "INT", "DECIMAL", "VARCHAR(100)", "VARCHAR(10)"]
toscast_types: List[str] = ["DATETIME", "VARCHAR(10)", "VARCHAR(10)", "INT", "DECIMAL", "INT", "DECIMAL", "DECIMAL", "INT", "DECIMAL", "DECIMAL"]

def remove_quotation_marks(list: List[str]) -> [str]:
    cleaned_data = []
    for s in list:
        cleaned_data.append(s.replace("'", ""))
    return cleaned_data

def format_values_sql(vals: List[str], types: List[str]) -> str:
    #here
    for index, v in enumerate(vals):
        if types[index]:
            pass


def gen_insert_sql(table: str, cols: List[str], data: List[str]):
    if len(cols) != len(data):
        raise ValueError("The number of columns and data values must match!")

    column_list = ", ".join(cols)
    value_list: str

    if table == "type_date":
        value_list = format_values_sql(data, type_col_types)


    sql = f"INSERT INTO {table} ({column_list}) VALUES ({value_list});"
    print(f"Insert sql statement: {sql}\n")
    return


data_sources = ["type_data.csv"]

if __name__ == "__main__":

    for source in data_sources:
        with open(source, 'r') as file:

            reader = csv.reader(file)
            headers = next(reader)

            for row in reader:
                gen_insert_sql(source.replace(".csv", ""), remove_quotation_marks(headers), row)

