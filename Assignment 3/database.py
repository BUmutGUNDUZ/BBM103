from sys import argv
def main():
    try:
        database = {}
        input = argv[1]
        with open(input, mode="r") as lines:
            lines = lines.readlines()
            for element in lines:
                try:
                    element = element.strip()
                    if not element:  # Checking whether the line is empty or not
                        continue
                    if "INSERT" in element.split() or "UPDATE" in element.split() or "CREATE_TABLE" in element.split():
                        element = element.strip().split(maxsplit=2)
                        table_name = element[1]
                    else:
                        element = element.strip().split(maxsplit=3)
                        table_name = element[1]
                    if element[0] == "CREATE_TABLE":
                        header = element[-1].split(",")
                        CREATE_TABLE(database, table_name, header)
                    elif element[0] == "INSERT":
                        INSERT(database, table_name, *tuple(map(str, element[-1].split(","))))
                    elif element[0] == "SELECT":
                        where = element[3].split(maxsplit=1)
                        selected_item = eval(where[1])  # Convert string to dictionary
                        columns = element[2].split(",")
                        SELECT(database, table_name, *columns, WHERE=selected_item)
                    elif element[0] == "UPDATE":
                        element = element[-1].strip().split("WHERE")
                        update_part = element[0].strip()
                        where_part = element[1].strip()
                        update = eval(update_part)
                        where = eval(where_part)
                        UPDATE(database, table_name, update, WHERE=where)
                    elif element[0] == "DELETE":
                        if len(element) == 2:
                            DELETE(database, table_name, WHERE=None)
                        else:
                            where_part = eval(element[-1])
                            DELETE(database, table_name, WHERE=where_part)
                    elif element[0] == "COUNT":
                        if element[-1] == "*":
                            where_part = element[-1]
                            COUNT(database, table_name, WHERE=where_part)
                        else:
                            where_part = eval(element[-1])
                            COUNT(database, table_name, WHERE=where_part)
                    elif element[0] == "JOIN":
                        element[1] = element[1].split(",")
                        table_name1 = element[1][0]
                        table_name2 = element[1][-1]
                        on_column = element[-1]
                        JOIN(database, table_name1, table_name2, on_column)
                except Exception as e:
                    pass
        save(database)
    except Exception:
        pass
def save(database): #The 'save' function was created because if 'return' is used, it will exit the for loop.
    return database
def draw_table(database, table_name, header_length):
    columns = database[table_name]["columns"]
    data = database[table_name]["data"]
    column_widths = []
    for col in columns:
        column_widths.append(len(col))
    for row in data:
        for i, col in enumerate(row):
            column_widths[i] = max(column_widths[i], len(str(col)))
    def draw_line():
        line = "+"
        for width in column_widths:
            line += "-" * (width + 2) + "+"
        print(line)
    draw_line()
    for i, col in enumerate(columns):
        print(f"| {col:<{column_widths[i]}}", end=" ")
    print("|")
    draw_line()
    for row in data:
        for i, col in enumerate(row):
            print(f"| {col:<{column_widths[i]}}", end=" ")
        print("|")
    if data:
        draw_line()
    print(f"{'#' * header_length}\n")
def CREATE_TABLE(database, table_name, header):
    try:
        header_length = 55
        print(f"###################### CREATE #########################".ljust(header_length, "#"))
        print(f"Table '{table_name}' created with columns:", header)
        print(f"{'#' * header_length}\n")
        database[table_name] = {"columns": header, "data": []}
    except Exception:
        pass
def INSERT(database, table_name, *args):
    header_length = 55
    try:
        if table_name not in database:
            raise ValueError(f"Table {table_name} not found")
        if not len(args) == len(database[table_name]["columns"]):
            raise ValueError(f"The column and the number of data to be entered are not equal")
        database[table_name]["data"].append(tuple(map(str, args)))
        print(f"###################### INSERT #########################".ljust(header_length, "#"))
        print(f"Inserted into '{table_name}': {tuple(map(str, args))}\n")
        print("Table:", table_name)
        draw_table(database, table_name, header_length)
    except ValueError as e:
        print(f"###################### INSERT #########################".ljust(header_length, "#"))
        print(str(e).strip("'"))
        if "column and the number of data" not in str(e):
            print(f"Inserted into '{table_name}': {args}")
        print(f"{'#' * header_length}\n")
    except Exception:
        pass
def SELECT(database, table_name, *columns, WHERE=None):
    header_length = 55
    try:
        if table_name not in database:
            raise ValueError(f"Table {table_name} not found")
        headers = database[table_name]["columns"]
        table = database[table_name]["data"]
        if "*" in columns:
            selected_headers = headers
            selected_indices = list(range(len(headers)))
        else:
            selected_headers = []
            selected_indices = []
            for col in columns:
                if col in headers:
                    selected_headers.append(col)
                    selected_indices.append(headers.index(col))
                else:
                    raise ValueError(f"Column {col} does not exist")
        if WHERE:
            for key in WHERE:
                if key not in headers:
                    raise KeyError(f"Column {key} does not exist")
        selected_rows = []
        for element in table:
            if all(element[headers.index(k)] == v for k, v in WHERE.items()):
                selected_row = tuple(element[idx] for idx in selected_indices)
                selected_rows.append(selected_row)
        print(f"###################### SELECT #########################".ljust(header_length, "#"))
        print("Condition:", WHERE)
        #The if control was added because even if the code does not give an error,
        #the appropriate data may not be found according to the conditions
        if selected_rows:
            print(f"Select result from '{table_name}': {selected_rows}")
        else:
            print(f"Select result from '{table_name}': None")
        print(f"{'#' * header_length}\n")
    except ValueError as e:
        print(f"###################### SELECT #########################".ljust(header_length, "#"))
        print(str(e).strip("'"))
        print("Condition:", WHERE)
        print(f"Select result from '{table_name}': None")
        print(f"{'#' * header_length}\n")
    except KeyError as e:
        print(f"###################### SELECT #########################".ljust(header_length, "#"))
        print(str(e).strip("'"))
        print("Condition:", WHERE)
        print(f"Select result from '{table_name}': None")
        print(f"{'#' * header_length}\n")
    except Exception:
        pass
def UPDATE(database, table_name, update, WHERE=None):
    header_length = 55
    try:
        if table_name not in database:
            raise ValueError(f"Table {table_name} not found")
        table = database.get(table_name, {}).get("data", [])
        headers = database.get(table_name, {}).get("columns", [])
        for update_column in update:
            if update_column not in headers:
                raise KeyError(f"Column {update_column} does not exist")
        if WHERE:
            for key in WHERE:
                if key not in headers:
                    raise KeyError(f"Column {key} does not exist")
        updated_rows = 0
        for element in table:
            if all(element[headers.index(k)] == v for k, v in WHERE.items()):
                idx = table.index(element)
                element = list(element)
                for update_column, update_value in update.items():
                    updating_index = headers.index(update_column)
                    element[updating_index] = update_value
                table[idx] = tuple(element)
                updated_rows += 1
        database[table_name]["data"] = table
        print(f"###################### UPDATE #########################".ljust(header_length, "#"))
        print(f"Updated '{table_name}' with {update} where {WHERE}")
        print(f"{updated_rows} rows updated.\n")
        print("Table:", table_name)
        draw_table(database, table_name, header_length)
    except ValueError as ve:
        print(f"###################### UPDATE #########################".ljust(header_length, "#"))
        print(f"Updated '{table_name}' with {update} where {WHERE}")
        print(str(ve).strip("'"))
        print("0 rows updated.")
        print(f"{'#' * header_length}\n")
    except KeyError as ke:
        print(f"###################### UPDATE #########################".ljust(header_length, "#"))
        print(f"Updated '{table_name}' with {update} where {WHERE}")
        print(str(ke).strip("'"))
        print("0 rows updated.\n")
        print("Table:", table_name)
        draw_table(database, table_name, header_length)
    except Exception:
        pass
def DELETE(database, table_name, WHERE=None):
    header_length = 55
    try:
        if table_name not in database:
            raise ValueError(f"Table {table_name} not found")
        table = database.get(table_name, {}).get("data", [])
        headers = database.get(table_name, {}).get("columns", [])
        if WHERE is None:
            deleted_rows = len(table)
            table.clear()
        else:
            rows_to_remove = []
            for element in table:
                for where_column, where_value in WHERE.items():
                    if where_column not in headers:
                        raise KeyError(f"Column {where_column} does not exist")
                    column_index = headers.index(where_column)
                    column_value = str(element[column_index])
                    if column_value != str(where_value):
                        break
                else:
                    rows_to_remove.append(element)
            deleted_rows = 0
            for row in rows_to_remove:
                table.remove(row)
                deleted_rows += 1
        print(f"###################### DELETE #########################".ljust(header_length, "#"))
        print(f"Deleted from '{table_name}' where", WHERE)
        print(f"{deleted_rows} rows deleted.\n")
        print("Table:", table_name)
        draw_table(database, table_name, header_length)
    except ValueError as ve:
        print(f"###################### DELETE #########################".ljust(header_length, "#"))
        print(f"Deleted from '{table_name}' where {WHERE}")
        print(str(ve).strip("'"))
        print("0 rows deleted.")
        print(f"{'#' * header_length}\n")
    except KeyError as ke:
        print(f"###################### DELETE #########################".ljust(header_length, "#"))
        print(f"Deleted from '{table_name}' where {WHERE}")
        print(str(ke).strip("'"))
        print("0 rows deleted.\n")
        print("Table:", table_name)
        draw_table(database, table_name, header_length)
    except Exception:
        pass
def COUNT(database, table_name, WHERE=None):
    header_length = 55
    try:
        if table_name not in database:
            raise ValueError(f"Table {table_name} not found")
        table = database.get(table_name, {}).get("data", [])
        headers = database.get(table_name, {}).get("columns", [])
        if WHERE == "*":
            counter = len(table)
        else:
            for key in WHERE:
                if key not in headers:
                    raise KeyError(f"Column {key} does not exist")
            counter = 0
            for element in table:
                if all(element[headers.index(k)] == v for k, v in WHERE.items()):
                    counter += 1
        print(f"###################### COUNT #########################".ljust(header_length - 1, "#"))
        print("Count:", counter)
        print(f"Total number of entries in '{table_name}' is {counter}")
        print(f"{'#' * header_length}\n")
    except ValueError as ve:
        print(f"###################### COUNT #########################".ljust(header_length - 1, "#"))
        print(str(ve).strip("'"))
        print(f"Total number of entries in '{table_name}' is 0")
        print(f"{'#' * header_length}\n")
    except KeyError as ke:
        print(f"###################### COUNT #########################".ljust(header_length - 1, "#"))
        print(str(ke).strip("'"))
        print(f"Total number of entries in '{table_name}' is 0")
        print(f"{'#' * header_length}\n")
    except Exception:
        pass
def JOIN(database, table1_name, table2_name, on_column):
    header_length = 55
    try:
        if table1_name not in database:
            raise ValueError(f"Table {table1_name} does not exist")
        elif table2_name not in database:
            raise ValueError(f"Table {table2_name} does not exist")
        table1 = database.get(table1_name, {}).get("data", [])
        headers1 = database.get(table1_name, {}).get("columns", [])
        table2 = database.get(table2_name, {}).get("data", [])
        headers2 = database.get(table2_name, {}).get("columns", [])
        if on_column not in headers1 and on_column not in headers2:
            raise ValueError(f"Column {on_column} does not exist")
        index1 = headers1.index(on_column)
        index2 = headers2.index(on_column)
        joined_headers = headers1 + headers2
        joined_table = []
        for row1 in table1:
            for row2 in table2:
                if row1[index1] == row2[index2]:
                    joined_row = list(row1) + list(row2)
                    joined_table.append(joined_row)
        database["Joined Table"] = {"columns": joined_headers, "data": joined_table}
        print(f"####################### JOIN #######################".ljust(header_length, "#"))
        print(f"Join tables {table1_name} and {table2_name}")
        print(f"Join result ({len(joined_table)} rows):\n")
        print("Table: Joined Table")
        draw_table(database, "Joined Table", header_length)
    except ValueError as ve:
        print(f"####################### JOIN ########################".ljust(header_length, "#"))
        print(f"Join tables {table1_name} and {table2_name}")
        print(str(ve).strip("'"))
        print(f"{'#' * header_length}\n")
    except Exception:
        pass
if __name__ == "__main__":
    main()
