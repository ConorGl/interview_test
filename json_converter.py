import json
import sqlite3
from datetime import datetime

SELECT_SQL = """SELECT active_user_count FROM active_customers
                WHERE date = '{date}'"""
INSERT_SQL = "INSERT INTO active_customers VALUES('{date}', '{count}' );"
UPDATE_SQL = """UPDATE active_customers
                set active_user_count={additional_count} + {current_count}
                WHERE date = '{current_date}'"""


def create_table_if_not_exists():
    """
    Checks if the db / table exists and creates it if not
    :return:
    """
    conn = sqlite3.connect('active_customers.db')
    mycur = conn.cursor()
    try:
        mycur.execute("""SELECT * FROM active_customers""")
    except:
        mycur.execute("""CREATE TABLE active_customers
                     ([date] date, [active_user_count] integer)""")
        conn.commit()
    finally:
        conn.close
    return

def check_if_row_exists_in_table(date):
    """
    Checks if a row with the current date already exists
    :param date: date
    :return: int
    """
    conn = sqlite3.connect('active_customers.db')
    mycur = conn.cursor()
    try:
        mycur.execute(SELECT_SQL.format(date=date))
        count = mycur.fetchone()[0]
    except:
        count = None
    return count


def get_customer_count():
    """
    Finds user_engagement events with a time > 300msec and returns a count
    per date
    :return: dict
    """
    with open('bq-results-sample-data.json') as sample:
        customer_engagement = {}
        for line in sample:
            data = json.loads(line) 
            if not data['event_name'] == 'user_engagement':
                continue
            engagement_event = next((e for e in data['event_params']
                                     if e['key'] == 'engagement_time_msec'), None)
            if engagement_event:
                val = int(engagement_event['value'].get('int_value') or 0)
                if val > 3000:
                    date = data['event_date']
                    if customer_engagement.get(date):
                        customer_engagement[date] += 1
                    else:
                        customer_engagement[date] = 1
    return customer_engagement

def run_sql(active_customers):
    """
    Checks whether row exists in table and inserts a new row if it doesn't
    :param active_customers: dict
    :return:
    """
    conn = sqlite3.connect('active_customers.db')
    mycur = conn.cursor()
    for date, count in active_customers.items():
        new_date = datetime.strptime(date, '%Y%m%d')
        current_count_at_date = check_if_row_exists_in_table(new_date.date())
        if current_count_at_date:
            continue
        else:
            mycur.execute(INSERT_SQL.format(date=new_date.date(),
                                            count=count))
    mycur.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_table_if_not_exists()
    customer_count = get_customer_count()
    run_sql(customer_count)
    print("Data successfully loaded")
