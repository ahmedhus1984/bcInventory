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

def mysqlCreate(cursor, table):
    serial, hostname, type, shipDate, warrExp, site, location, status, department, model, brand=input('enter serial, hostname, type, shipDate, warrExp, site, location, status, department, model, brand seperated by comma:\n').split(',')
    print(serial+'\n'+hostname+'\n'+type+'\n'+shipDate+'\n'+warrExp+'\n'+site+'\n'+location+'\n'+status+'\n'+department+'\n'+model)
    cursor.execute(f'insert into {table} (serial, hostname, type, shipDate, warrExp, site, location, status, department, model, brand) values("{serial}", "{hostname}", "{type}", "{shipDate}", "{warrExp}", "{site}", "{location}", "{status}", "{department}", "{model}", "{brand}");')

def mysqlRead(cursor, table, readParam):
    blah=readColumns(cursor, table)
    cursor.execute(f'select * from {table} where serial=\'{readParam}\'')
    blah2=[]
    for i in cursor:
        for j in i:
            blah2.append(j)
    print()
    for i in range(0, len(blah), 1):
        print(f'{blah[i]: <12}: {blah2[i]}')
    print()


def readColumns(cursor, table):
    cursor.execute(f'select column_name from information_schema.columns where table_schema=\'bcinv\' and table_name=\'{table}\'')
    blah=cursor.fetchall()
    blah2=[]
    for i in blah:
        blah2.append(i[0])
    return blah2

def mysqlConnClose(conn):
    conn.close()

def choiceSelect(conn, cursor):
    while True:
        table=input('enter option to view a table; s for systems, l for logs, u for users, x to exit: ')
        match table:
            case 's':
                table='systems'
                break
            case 'l':
                table='logs'
                break
            case 'u':
                table='users'
                break
            case 'x':
                return table
            case _:
                print('wrong choice, only s, l or u allowed. ')
    while True:
        operation=input('enter c, r, u, d to create, read, update, delete records, x to exit: ')
        match operation:
            case 'c':
                mysqlCreate(cursor, table)
                conn.commit()
                break
            case 'e':
                blah=readColumns(cursor, table)
                print(blah)
                break
            case 'r':
                readParam=input('enter serial number: ')
                mysqlRead(cursor, table, readParam)
                break
            case 'x':
                return operation
            case _:
                print('wrong choice, only c, r, u, d or x is allowed.')

def main():
    conn, myCursor=mysqlConn()
    a=''
    while True:
        a=choiceSelect(conn, myCursor)
        if a=='x':
            print('bye!')
            mysqlConnClose(conn)
            return 0

main()