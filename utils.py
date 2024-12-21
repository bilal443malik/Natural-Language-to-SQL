import sqlite3

def clean_input_string(input_string):
    to_remove = ["```", "sql", "\\", "`"]
    for item in to_remove:
        input_string = input_string.replace(item, "")
    return " ".join(input_string.split())

def execute_sql_query(sql_query):
    try:
        conn = sqlite3.connect('chinook.db')
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        conn.close()
        return columns, results
    except sqlite3.Error as e:
        return None, f"SQL Error: {str(e)}"