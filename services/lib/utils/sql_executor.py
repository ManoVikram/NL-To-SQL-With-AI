def _pg_data_type_to_string(data_type_code):
    type_map = {
        23: 'INTEGER',
        25: 'TEXT',
        1043: 'VARCHAR',
        1082: 'DATE',
        1114: 'TIMESTAMP',
        1700: 'NUMERIC',
        16: 'BOOLEAN'
    }
    
    return type_map.get(data_type_code, 'UNKNOWN')

def execute(connection, sql_query):
    # Step 1 - Create a cursor
    cursor = connection.cursor()

    # Step 2 - Execute the SQL
    cursor.execute(sql_query)

    # Step 3 - Get the column details
    columns = [
        {
            "name": desc[0],
            "data_type": _pg_data_type_to_string(desc[1])
        }
        for desc in cursor.description
    ]

    # Step 4 - Get the rows
    rows = cursor.fetchall()

    # Step 5 - Close the cursor
    cursor.close()

    # Step 6 - Return the results
    return {
        "columns": columns,
        "rows": rows
    }