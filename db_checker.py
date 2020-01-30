import sqlite3

def select_sql_lite_table():
    conn = sqlite3.connect('active_customers.db') 
    mycur = conn.cursor()
    try:
        mycur.execute("SELECT * FROM ACTIVE_CUSTOMERS")
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