import sqlite3


def select_sql_lite_table():
    """
    Selects all rows from table active_customers
    :return: list
    """
    conn = sqlite3.connect('active_customers.db')
    mycur = conn.cursor()
    try:
        mycur.execute("SELECT * FROM active_customers")
        rows = mycur.fetchall()
    except:
        rows = None
    conn.close()
    return rows

if __name__ == '__main__':
    results = select_sql_lite_table()
    if results:
        print('date       | active_user_count')
        for date, count in results:
            print(str(date) + ' | ' + str(count))
    else:
        print('No table or database')
