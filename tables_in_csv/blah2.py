import csv
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

def mysqlConnClose(conn):
    conn.close()

def compareCols(table, cursor):
    a=getHostCol('systems', cursor)
    b=getHostCol(table, cursor)
    c=[]
    for i in b:
        if i not in a:
            c.append(i)
    for i in c:
        print(i)
    print(f'no. of hosts not found in systems: {len(c)}')


def getHostCol(table, cursor):
    a=[]
    cursor.execute(f'select hostname from {table}')
    count=0
    for i in cursor:
        count+=1
        a.append(i[0])
    print(f'\n{count} records entered\n\n')
    return a


def main():
    conn, myCursor=mysqlConn()
    table=input('enter table name to check: ')
    compareCols(table, myCursor)
    mysqlConnClose(conn)


main()