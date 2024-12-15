import psycopg2

def insert_data_into_postgres(data, host, db, user, password):
    """Insert data into PostgreSQL."""
    print(f"host {host}, db{db},user{user},password{password}")
    conn = psycopg2.connect(
        host=host,
        database='postgres',
        user=user,
        password=password,
    )
    cursor = conn.cursor()

    # Example query - adjust fields and table name to match your schema
    for record in data:
        cursor.execute(
            """
            INSERT INTO my_table (field1, field2, field3)
            VALUES (%s, %s, %s)
            """,
            (record["field1"], record["field2"], record["field3"]),
        )

    conn.commit()
    cursor.close()
    conn.close()
