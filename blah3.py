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


def rmSg(conn, cursor):
    cursor.execute('select user from prevown')
    blah=cursor.fetchall()
    print()
    for i in blah:
        if '.sg' in i[0]:
            x=i[0]
            x=i[0].replace('.sg', '')
            cursor.execute(f'update prevown set user=\'{x}\' where user=\'{i[0]}\'')
    conn.commit()

def swapUserId(conn, cursor):
    with open('hehe.csv', 'r') as file:
        for i in file:
            a=i.split(',')[0]
            b=i.split(',')[1].rstrip('\n')
            # print(a)
            # print(b)
            # print()
            cursor.execute(f'update prevown set user=\'{b}\' where user=\'{a}\'')
        conn.commit()    

def copy():
    count=0
    with open('users.csv', 'r') as blah:
        with open('hahaCopied.csv', 'r') as blah2:
            with open('hehe.csv', 'w') as blah3:
                print()
                blah=list(blah)
                blah2=list(blah2)
                for i in range(0, len(blah2)):
                    a0=blah2[i].rstrip('\n').strip('"')
                    a=blah2[i].split()[0].strip('"').lower()
                    for j in range(0, len(blah)):
                        b=blah[j].split(',')[0].lower()
                        if a in b:
                            x=f'{a0},{b}\n'
                            print(x, end='')
                            blah3.write(x)
                            break

def crossCheck(conn, cursor):
    usersList=[]
    departmentList=[]
    with open('users.csv', 'r') as blah:
        for i in blah:
            a=i.split(',')[1].strip().lower()
            usersList.append(a)
        cursor.execute('select department from departments')
        blah=cursor.fetchall()
        for i in blah:
            departmentList.append(i[0].strip().lower())
        print()
        for i in departmentList:
            if i not in usersList:
                    print(i)

def createCommands():
    with open('users.csv', 'r') as file:
        with open('blah.txt', 'w')as file2:
            for i in file:
                x=i.split(',')
                x[1]=x[1].rstrip('\n')
                file2.write('insert into users(user, department)values')
                file2.write(f'(\'{x[0]}\', \'{x[1]}\');\n')
            file2.write(');')

def main():
    conn, myCursor=mysqlConn()
    # rmSg(conn, myCursor)
    # mysqlConnClose(conn)
    # copy()
    # swapUserId(conn, myCursor)
    # crossCheck(conn, myCursor)
    createCommands()
    return 0


main()