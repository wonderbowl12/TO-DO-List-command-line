import sqlite3
from datetime import date

# CAN YOU FIX YOUR NAMING? GAWD DAMN DONT USE "ITEM" FOR BOTH THE MESSAGE AND ID NAME

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
        if new_com[:8] == 'list all':
            list_all(new_com[5:])
        if new_com[:7] == 'delete ':
            delete(new_com[7:])
        if new_com[:5] == 'flag ':
            flag(new_com[5:])


# opens text help document
def help_main():
    f = open('todo_help.txt', 'r')
    print(f.read())


# Creates 4 attributes, message, date, status (always 0), and flagged (always 0)
def todo(item):
    if item[:4] == 'edit':
        list_single(item[5:])
    else:
        cursor.execute('INSERT INTO list(Message, Date, STATUS, FLAGGED ) VALUES(?,?,?,?)', (item, d3, 0, 0))
        connection.commit()


# Lists single item from todo, there is no reason to have this maybe delete it...
def list_single(id_name):
    try:
        select_function(id_name)
        row = cursor.fetchone()
        print('\n')
        print_status()
        print_item(row)
        print('\n')
    except TypeError:
        print('There is no item with that ID number.')


def print_item(row):
    print(str(row['id_name']) + '  ' + status(row['STATUS']) + '   ' + row['Message'] + '           ' + row['Date'])


def print_status():
    print('#      STATUS            ITEM                        DATE'
          '\n===========================================================')


# Lists all items in todo
def list_all(item):
    id_db = fetchall()
    if len(id_db) == 0:
        print('There are no items in your TODO list. ')
    else:
        print_status()
        check_flag(item)
        print('\n')
        for item in id_db:
            select_function(str(item))
            row = cursor.fetchone()
            print_item(row)

# Selects certain items from sqlite db
def select_function(id_name):
    return cursor.execute('SELECT*FROM list WHERE id_name=?', id_name)


# grabs IDs from db file, very important
def fetchall():
    cursor.execute('SELECT*FROM list')
    rows = cursor.fetchall()
    id_db = []
    for row in rows:
        id_db.append(row[0])
    return id_db


# returns status of todo item
def status(row_status):
    if row_status == 1:
        return 'X COMPLETED'
    else:
        return '  NOT COMPLETED'


# Deletes single item, function used later one
def delete(item):
    cursor.execute('DELETE FROM list WHERE id_name = ?', item)
    connection.commit()


# item is the id and flagged is either a 1 (flag) or 0 (unflag)
def flag(item):
    select_function(item)
    row = cursor.fetchone()
    if row['FLAGGED'] == 1:
        cursor.execute('UPDATE list SET FlAGGED = 0 WHERE id_name = ?', item)
        print('Item was unflagged')
    else:
        cursor.execute('UPDATE list SET FLAGGED = 1 WHERE id_name = ?', item)
        print('Item was flagged')
    connection.commit()


# Checks if item is flagged and prints it, spagetti code needs optimzation maybe order FLAGGED with algorithim
def check_flag(item):
    id_db = fetchall()
    if len(id_db) == 0:
        print('There are no flagged items. ')
    else:
        print('!!THESE ITEMS ARE FLAGGED!!')
        for item in id_db:
            select_function(str(item))
            row = cursor.fetchone()
            if row['FLAGGED'] == 1:
                print_item(row)
            else:
                pass


main()
