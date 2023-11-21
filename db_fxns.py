# core package
import sqlite3

# set connect the datbase
conn = sqlite3.connect("data.db", check_same_thread=False)
c = conn.cursor()


# make a creating table function
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS tasktable(task TEXT, task_status TEXT, task_due_date DATE)')

# make a adding data function
def add_data(task, task_status, task_due_date):
    # to avoid SQL injection, it is better to use (?, ?, ?)
    c.execute('INSERT INTO tasktable(task, task_status, task_due_date) VALUES (?, ?, ?)',(task, task_status, task_due_date))   # the query must be passed as a tuple type such as (AAA,)
    conn.commit()

# make a viewing all data function
def view_all_data():
    c.execute('SELECT * FROM tasktable')
    data = c.fetchall()
    return data

def view_unique_tasks():
    c.execute('SELECT DISTINCT task FROM tasktable')
    data = c.fetchall()
    return data


def get_task(task):
    c.execute("SELECT * FROM tasktable WHERE task=?", (task,))   # the query must be passed as a tuple type such as (AAA,)
    data = c.fetchall()
    return data


def edit_task_data(new_task, new_task_status, new_task_due_date, task, task_status, task_due_date):
    c.execute("UPDATE tasktable SET task=?, task_status=?, task_due_date=? WHERE task=? and task_status=? and task_due_date=?",(new_task, new_task_status, new_task_due_date, task, task_status, task_due_date))
    conn.commit()
    data = c.fetchall()
    return data
    

def delete_data(task):
    c.execute('DELETE FROM tasktable WHERE task=?',(task,)) # the query must be passed as a tuple type such as (AAA,)
    conn. commit()