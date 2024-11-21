import mysql.connector

def mysqlConn():
    user=input('enter username: ')
    pwd=input('enter password: ')
    conn=mysql.connector.connect(host='66.96.216.133', user=user, passwd=pwd, db='bcinv')
    if not conn.is_connected():
        print('unable to connect to sql server.')
        exit(1)
    else:
        print('connection success!!!')
        myCursor=mysqlCursor(conn)
        return conn, myCursor

def mysqlCursor(conn):
    myCursor=conn.cursor(buffered=True)
    if not myCursor:
        print('unable to create cursor')
        mysqlConnClose(conn)
        exit(1)
    return myCursor

def mysqlCreate(table, cursor):
    serial, hostname, type, shipDate, warrExp, site, location, status, department, model=input('enter serial, hostname, type, shipDate, warrExp, site, location, status, department, model seperated by space:\n').split(',')
    print(serial+'\n'+hostname+'\n'+type+'\n'+shipDate+'\n'+warrExp+'\n'+site+'\n'+location+'\n'+status+'\n'+department+'\n'+model)
    cursor.execute(f'insert into {table} (serial, hostname, type, shipDate, warrExp, site, location, status, department, model) values("{serial}", "{hostname}", "{type}", "{shipDate}", "{warrExp}", "{site}", "{location}", "{status}", "{department}", "{model}");')

def mysqlRead(table, serial, cursor):
    cursor.execute(f'select * from {table} where serial="{serial}"')
    for i in cursor:
        for j in i:
            print(j)

def mysqlConnClose(conn):
    conn.close()

def choiceSelect(conn, cursor):
    a=input('enter table to view record; s for systems, l for logs, u for users, x to exit: ')
    match a:
        case 's':
            a='systems'
        case 'l':
            a='logs'
        case 'u':
            a='users'
        case 'x':
            return a
        case _:
            print('wrong choice, only s, l or u allowed. ')
            exit(2)
    b=input('enter c, r, u or d for create, read, update or delete respectively: ')
    match b:
        case 'c':
            mysqlCreate(a, cursor)
            conn.commit()
        case 'r':
            c=input('enter serial number: ')
            mysqlRead(a, c, cursor)
        case _:
            print('wrong choice, only c, r, u or d allowed.')
            exit(3)
    return b

def main():
    conn, myCursor=mysqlConn()
    a=''
    while True:
        choiceSelect(conn, myCursor)
        if a=='x':
            print('bye!')
            mysqlConnClose(conn)
            return 0

main()