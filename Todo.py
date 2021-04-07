import sqlite3
from datetime import date
import ipdb

connection = sqlite3.connect('Todo_list_2.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

print('Welcome to DA To-Do List')
today = date.today()
d2 = today.strftime("%B %d, %Y")
print('Today is ' + d2)
d3 = today.strftime("%m/%d/%y")

def main():
    print('Tip: Don\'t forget to type \' help \' if you need it!\n')
    while True:
        command = input('>>> ')
        new_com = command.lower()
        if new_com == 'help':
            help_main()
        if new_com[:4] == 'todo':
            todo(new_com[5:])
        if new_com[:5] == 'list ':
            list_function(new_com[5:])


def help_main():
    f = open('todo_help.txt', 'r')
    print(f.read())

def todo(item):
    if item[:4] == 'edit':
        select_function(item[4:])
        row = cursor.fetchone()
        print(row['Message'], row['Date'])

    else:
        cursor.execute('INSERT INTO list(Message, Date) VALUES(?,?)', (item, d3))
        connection.commit()
        connection.close()

def list_function(item):
    if item[3:] == 'all':
        id_db = fetchall()
        if len(id_db) == 0:
            print('There are no items in your TODO list. ')
        else:
            for id in id_db:
                select_function(id)
                row = cursor.fetchone()
                print(row['Message'], row['Date'])



def select_function(id_name):
    print(cursor.execute('SELECT*FROM list WHERE id_name=?', id_name))

# grabs IDs from db file, very important
def fetchall():
    cursor.execute('SELECT*FROM list')
    rows = cursor.fetchall()
    id_db = []
    for row in rows:
        id_db.append(row[0])
        print(row)
    return id_db



main()