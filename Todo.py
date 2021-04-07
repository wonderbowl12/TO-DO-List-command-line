import sqlite3
from datetime import date
import ipdb
from pprint import pprint
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
            list_all(new_com[5:])
        if new_com[:7] == 'delete ':
            delete(new_com[7:])

#opens text help document
def help_main():
    f = open('todo_help.txt', 'r')
    print(f.read())


def todo(item):
    if item[:4] == 'edit':
        list_single(item[5:])
    else:
        cursor.execute('INSERT INTO list(Message, Date, STATUS) VALUES(?,?,?)', (item, d3, 0))
        connection.commit()


#Lists single item from todo
def list_single(id_name):
    try:
        select_function(id_name)
        row = cursor.fetchone()
        print('\n')
        print('#      STATUS         ITEM                        DATE')
        print('========================================================')
        print(str(row['id_name'])+ '  '+ status(row['STATUS'])+'   ' + row['Message']+ '           ' +row['Date'])
        print('\n')
    except TypeError:
        print('There is no item with that ID number.')

#Lists all items in todo
def list_all(item):
    if item[3:] == 'all':
        id_db = fetchall()
        if len(id_db) == 0:
            print('There are no items in your TODO list. ')
        else:
            for id in id_db:
                select_function(id)
                row = cursor.fetchone()
                print(row['Message'], row['Date'])


#Selects certain items from sqlite db
def select_function(id_name):
    return cursor.execute('SELECT*FROM list WHERE id_name=?', id_name)

# grabs IDs from db file, very important
def fetchall():
    cursor.execute('SELECT*FROM list')
    rows = cursor.fetchall()
    id_db = []
    for row in rows:
        id_db.append(row[0])
        print(row)
    return id_db

#returns status of todo item
def status(row_status):
    if row_status == 1:
        return 'X COMPLETED'
    else:
        return '  NOT COMPLETED'

#Deletes single item, function used later one
def delete(item):
    cursor.execute('DELETE FROM list WHERE id_name = ?', item)
    connection.commit()


main()