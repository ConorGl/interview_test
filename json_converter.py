import json
import sqlite3

SELECT_SQL = """SELECT active_user_count FROM ACTIVE_CUSTOMERS
                WHERE date = '{date}'"""
INSERT_SQL = "INSERT INTO ACTIVE_CUSTOMERS VALUES({date}, '{count}' );"
UPDATE_SQL = """UPDATE ACTIVE_CUSTOMERS
                set active_user_count={additional_count} + {current_count}
                WHERE date = '{current_date}'"""


def create_table_if_not_exists():
    conn = sqlite3.connect('active_customers.db')
    mycur = conn.cursor()
    try:
        mycur.execute("""SELECT * FROM ACTIVE_CUSTOMERS""")
    except:
        mycur.execute("""CREATE TABLE ACTIVE_CUSTOMERS
                     ([date] date, [active_user_count] integer)""")
        conn.commit()
    conn.close


def check_if_row_exists_in_table(date):
    conn = sqlite3.connect('active_customers.db')
    mycur = conn.cursor()
    try:
        mycur.execute(SELECT_SQL.format(date=date))
        count = mycur.fetchone()[0]
    except:
        count = None
    return count


def get_customer_count():
    with open('bq-results-sample-data.json') as sample:
        data = [json.loads(line) for line in sample]
    customer_engagement = {}
    for line in data:
        if not line['event_name'] == 'user_engagement':
            continue
        engagement_event = next((e for e in line['event_params'] if e['key'] == 'engagement_time_msec'), None)
        if engagement_event:
            val = int(engagement_event['value'].get('int_value') or 0)
            if val > 3000:
                date = line['event_date']
                if customer_engagement.get(date):
                    customer_engagement[date] += 1
                else:
                    customer_engagement[date] = 1
    return customer_engagement


def run_sql(active_customers):
    conn = sqlite3.connect('active_customers.db')
    mycur = conn.cursor()
    for date, count in active_customers.items():
        current_count_at_date = check_if_row_exists_in_table(date)
        if current_count_at_date:
            continue
        else:
            mycur.execute(INSERT_SQL.format(date=date, count=count))
    mycur.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_table_if_not_exists()
    customer_count = get_customer_count()
    run_sql(customer_count)
    print("Data successfully loaded")
