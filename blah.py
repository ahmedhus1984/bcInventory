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

def changeUn(myCursor):
    myCursor.execute('select user from currown where user like\'%.sg%\'')
    blah=myCursor.fetchall()
    for i in blah:
        # print(i[0])
        x=i[0].replace('.sg', '')
        # print(x)
        # print()
        myCursor.execute(f'update currown set user=\'{x}\' where user=\'{i[0]}\'')
    myCursor.execute('select user from currown where user like\'%.sg%\'')
    blah=myCursor.fetchall()
    for i in blah:
        print(i)


def main():
    conn, myCursor=mysqlConn()
    changeUn(myCursor)
    conn.commit()
    mysqlConnClose(conn)
    return 0


main()