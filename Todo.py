import sqlite3
from datetime import date
import random



# CAN YOU FIX YOUR NAMING? GAWD DAMN DONT USE "ITEM" FOR BOTH THE MESSAGE AND ID NAME

connection = sqlite3.connect('Todo_list_2.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
# Prints the start up
print('Welcome to DA To-Do List')
today = date.today()
d2 = today.strftime("%B %d, %Y")
print('Today is ' + d2)
d3 = today.strftime("%m/%d/%y")
tips = ['Don\'t forget to type \' help \' if you need it!\n', 'Flagged items will always be shown right underneath\n'
                                                              'the flagged banner. If there is nothing there then\n'
                                                              'no items are flagged!']


# Main function
def main():
    print('Tip: ' + random.choice(tips))
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
        if new_com[:5] == 'done ':
            done(new_com[5:])


# opens text help document
def help_main():
    f = open('todo_help.txt', 'r')
    print(f.read())


# Creates 4 attributes, message, date, status (always 0), and flagged (always 0), if user wants to edit the
# code then updates the .db file
def todo(item):
    if item[:4] == 'edit':
        print_banner()
        list_single(item[5:])
        cursor.execute('UPDATE list SET Message=? WHERE id_name =?', (input('Update message >>> '), item[5:]))
        connection.commit()
        print('Todo item {} updated.'.format(item[5:]))
    else:
        cursor.execute('INSERT INTO list(Message, Date, STATUS, FLAGGED ) VALUES(?,?,?,?)', (item, d3, 0, 0))
        connection.commit()


# Lists single item from todo, there is no reason to have this maybe delete it...
def list_single(id_name):
    try:
        select_function(id_name)
        row = cursor.fetchone()
        print_item(row)
        print('')
    except TypeError:
        print('There is no item with that ID number.')


def print_item(row):
    print(str(row['id_name']) + '  ' + status(row['STATUS']) + '   ' + newLine(row['Message'], 25) + ' ' * 20 + row[
        'Date'])
    print('')


def print_banner():
    print('#      STATUS                TODO                        DATE'
          '\n====================================================================')


# recursively adds a newline every nth character
def newLine(text, lineLength):
    if len(text) <= lineLength:
        return text
    else:
        return text[:lineLength] + '\n' + ' ' * 21 + newLine(text[lineLength:], lineLength)


# Lists all items in todo
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
        return '  X COMPLETED'
    else:
        return '  NOT COMPLETED'


# Deletes single item, function used later one
def delete(item):
    cursor.execute('DELETE FROM list WHERE id_name = ?', item)
    print('Item {} deleted.'.format(item))
    connection.commit()


# item is the id and flagged is either a 1 (flag) or 0 (unflag)
def flag(id_name):
    select_function(id_name)
    row = cursor.fetchone()
    if row['FLAGGED'] == 1:
        cursor.execute('UPDATE list SET FlAGGED = 0 WHERE id_name = ?', id_name)
        print('Item {} was unflagged'.format(id_name))
    else:
        cursor.execute('UPDATE list SET FLAGGED = 1 WHERE id_name = ?', id_name)
        print('Item {} was flagged'.format(id_name))
    connection.commit()


# Checks if item is flagged and prints it, spagetti code needs optimzation maybe order FLAGGED with algorithim
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
    print('=' * 68)

def done(item):
    if item[:5] == 'today':
        pass
    if item[:4] == 'week':
        pass
    if item[:5] == 'month':
        pass
    if item[:3] == 'all':
        pass
    else:
        select_function(item)
        row = cursor.fetchone()
        if row['STATUS'] == 0:
            cursor.execute('UPDATE list SET STATUS = 1 WHERE id_name = ?', item)
        else:
            cursor.execute('UPDATE list SET STATUS = 0 WHERE id_name = ?', item)
        connection.commit()

main()
