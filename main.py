import sqlite3
from datetime import date
import random

# connects to db file
connection = sqlite3.connect('Todo_list_2.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

# Prints the start up title, date, and tips
print('Welcome to DA To-Do List')
today = date.today()
d2 = today.strftime("%B %d, %Y")
print('Today is ' + d2)
d3 = today.strftime("%m/%d/%y")
tips = ['Don\'t forget to type \' help \' if you need it!\n', 'Flagged items will always be shown right underneath\n'
                                                              'the flagged banner. If there is nothing there then\n'
                                                              'no items are flagged!',
        'If an item is flagged, you will ALWAYS\n'
        'be asked for permission before deleting. ']


# Main function
def main():
    print('Tip: ' + random.choice(tips))

    while True:
        command = input('>>> ')
        if command.lower() == 'help':
            help_main()
        if command.lower()[:4] == 'todo':
            todo(command[5:])
        if command.lower()[:10] == 'todo edit ':
            todo_edit(command[10:])
        if command.lower()[:8] == 'list all':
            list_all(command[5:])
        if command.lower()[:10] == 'delete all':
            delete_all()
        if command.lower() == 'delete done':
            delete_completed()
        elif command.lower()[:7] == 'delete ':
            try:
                delete(command[7:])
            except Exception:
                error()
        if command.lower()[:5] == 'flag ':
            try:
                flag(command[5:])
            except Exception:
                error()
        if command.lower()[:8] == 'done all':
            done_all()
        elif command.lower()[:5] == 'done ':
            try:
                done(command[5:])
            except Exception:
                error()


def error():
    print('Command not recognized.')


# opens text help document
def help_main():
    f = open('todo_help.txt', 'r')
    print(f.read())


# Selects certain items from sqlite db
def select_function(id_name):
    return cursor.execute('SELECT*FROM list WHERE id_name=?', id_name)


# function to update certain attributes
def update(attribute, atr_update, id_name):
    return cursor.execute('UPDATE list SET {} = ? WHERE id_name =? '.format(attribute), (atr_update, id_name))


# Deletes single item, function used in different delete functions
def delete(id_name):
    select_function(str(id_name))
    row = cursor.fetchone()
    if row['FLAGGED'] == 1:
        delete_flag(id_name)
    else:
        cursor.execute('DELETE FROM list WHERE id_name = ?', id_name)
        print('Item {} deleted.'.format(id_name))
        connection.commit()


# If item is flagged this function confirms before deleting it
def delete_flag(id_name):
    if input('{} is a flagged item, are you sure you want to delete? '.format(id_name)).lower() == 'yes':
        cursor.execute('DELETE FROM list WHERE id_name = ?', id_name)
        print('Item {} deleted.'.format(id_name))
        connection.commit()
    else:
        print('Command not recognized.')


# deletes all to-do items
def delete_all():
    id_db = fetchall()
    for id_name in id_db:
        delete(str(id_name))


# Delete completed items
def delete_completed():
    id_db = fetchall()
    for id_name in id_db:
        select_function(str(id_name))
        row = cursor.fetchone()
        if row['STATUS'] == 1:
            cursor.execute('DELETE FROM list WHERE id_name=?', str(id_name))
            connection.commit()
        else:
            pass

    print('All \'Completed\' items deleted.')


# recursively adds a newline every nth character for printing the message to make sure everything fits
def newLine(text, lineLength):
    if len(text) <= lineLength:
        return text
    else:
        return text[:lineLength] + '\n' + ' ' * 40 + newLine(text[lineLength:], lineLength)


# returns status of to-do item
def status(row_status):
    if row_status == 1:
        return '    X COMPLETED'
    else:
        return '  NOT COMPLETED'


# prints row of data from sql db
def print_item(row):
    print(str(row['id_name']) + '  ' * 2 + row['Date'] + '  ' * 2 + status(row['STATUS']) + ' ' * 8 + newLine(
        row['Message'], 30))
    print('')


# prints the banner whenever a to-do list is printed
def print_banner():
    print('#      DATE        STATUS                        TODO'
          '\n=========================================================================')


# Creates 4 attributes, message, date, status (default 0), and flagged (default 0), if user wants to edit the
# code then updates the .db file
def todo(item):
    cursor.execute('INSERT INTO list(Message, Date, STATUS, FLAGGED ) VALUES(?,?,?,?)', (item, d3, 0, 0))
    connection.commit()
    list_all('all')


def todo_edit(id_name):
    print_banner()
    list_single(id_name)
    update('Message', input('Update Item Description >>> '), id_name)
    print('Todo item {} updated.'.format(id_name))
    list_all('all')


# Lists single item from to-do, used in list all function
def list_single(id_name):
    try:
        select_function(id_name)
        row = cursor.fetchone()
        print_item(row)
        print('')
    except TypeError:
        print('There is no item with that ID number.')


# Lists all items in to-do
def list_all(item):
    id_db = fetchall()
    if len(id_db) == 0:
        print('There are no items in your TODO list. ')
    else:
        print_banner()
        check_flag(item)
        print('\n')
        for item in id_db:
            list_single(str(item))


# grabs IDs from db file, very important
def fetchall():
    cursor.execute('SELECT*FROM list')
    rows = cursor.fetchall()
    id_db = []
    for row in rows:
        id_db.append(row[0])
    return id_db


# item is the id and flagged is either a 1 (flag) or 0 (unflag)
def flag(id_name):
    select_function(id_name)
    row = cursor.fetchone()
    if row['FLAGGED'] == 1:
        update('FLAGGED', 0, id_name)
        print('Item {} was unflagged'.format(id_name))
    else:
        update('FLAGGED', 1, id_name)
        print('Item {} was flagged'.format(id_name))
    connection.commit()


# Checks if item is flagged and prints it, spaghetti code needs optimization maybe order FLAGGED with algorithm
def check_flag(id_name):
    id_db = fetchall()
    print('!!THESE ITEMS ARE FLAGGED!!')
    print('')
    for id_name in id_db:
        select_function(str(id_name))
        row = cursor.fetchone()
        if row['FLAGGED'] == 1:
            print_item(row)
        else:
            pass
    print('=' * 73)


def done(id_name):
    select_function(id_name)
    row = cursor.fetchone()
    if row['STATUS'] == 0:
        update('STATUS', 1, id_name)
        print('Item {} has been marked \'Completed\''.format(id_name))
    else:
        update('STATUS', 0, id_name)
        print('Item {} has been marked \'Not completed\''.format(id_name))
    connection.commit()
    list_all('all')


def done_all():
    id_db = fetchall()
    for id_name in id_db:
        select_function(str(id_name))
        row = cursor.fetchone()
        if row['STATUS'] == 1:
            pass
        else:
            update('STATUS', 1, id_name)
    print('All items have been marked \'Completed!\'')
    list_all('all')


main()
