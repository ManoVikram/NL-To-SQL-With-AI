def load(connection):
    # Step 1 - Create a cursor
    cursor = connection.cursor()

    # Stpp 2 - Fetch the schema details
    cursor.execute("""
        SELECT 
            table_name,
            column_name,
            data_type,
            is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """)

    # Step 3 - Process the results and format the schema for LLM
    tables = {}
    for row in cursor.fetchall():
        table_name, column_name, data_type, is_nullable = row
        
        if table_name not in tables:
            tables[table_name] = []
        
        tables[table_name].append({
            "column_name": column_name,
            "data_type": data_type,
            "is_nullable": is_nullable == "YES"
        })

        schema_text = "DATABASE SCHEMA:\n\n"
        for table_name, columns in tables.items():
            schema_text += f"Table: {table_name}\n"
            for column in columns:
                nullable_text = "nullable" if column["is_nullable"] else "not null"
                schema_text += f" - {column["column_name"]} ({column["data_type"], {nullable_text}})\n"
            schema_text += "\n"

    # Step 4 - Close the cursor
    cursor.close()

    return schema_text