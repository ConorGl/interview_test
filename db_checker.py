import sqlite3

def select_sql_lite_table():
    conn = sqlite3.connect('active_customers.db') 
    mycur = conn.cursor()
    mycur.execute("SELECT * FROM ACTIVE_CUSTOMERS")
    return mycur.fetchall()

if __name__ == '__main__':
    print(select_sql_lite_table())