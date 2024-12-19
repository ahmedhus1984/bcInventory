import mysql.connector
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def mysqlConn():
    user=input('\nenter username: ')
    pwd=input('enter password: ')
    conn=mysql.connector.connect(host='66.96.216.133', user=user, passwd=pwd, db='bcinv')
    if not conn.is_connected():
        print('unable to connect to sql server.')
        exit(1)
    else:
        cls()
        print('\nconnection success!!!')
        myCursor=mysqlCursor(conn)
        return conn, myCursor

def mysqlCursor(conn):
    myCursor=conn.cursor(buffered=True)
    if not myCursor:
        print('unable to create cursor')
        mysqlConnClose(conn)
        exit(1)
    return myCursor

def deviceIssue(conn, cursor):
    #new user check begins
    hostname=input('\nenter hostname of device to issue to user: ').strip().lower()
    result=0
    cursor.execute(f'select department from systems where hostname=\'{hostname}\' and status=\'pending_deployment\'')
    deviceDepartment=(list(cursor))[0][0].strip().lower()
    result=cursor.rowcount
    if result==0:
        cursor.execute(f'select * from systems where hostname=\'{hostname}\'')
        result=cursor.rowcount
        if result==0:
            print('hostname not found...please contact database admin')
        else:
            print('hostname found, but not available for deployment...please contact database admin')
        return
    else:
        print(f'{result} hostname(s) named \'{hostname}\', from \'{deviceDepartment}\' department found')
    
    #double confirm hostname availability in case the status is reflected correctly in the systems table
    cursor.execute(f'select * from currown where hostname=\'{hostname}\'')
    result=cursor.rowcount
    if result==0:
        print('hostname currently not in use, available for deployment')
    else:
        print(f'{result} hostname(s) named \'{hostname}\' currently in use by {cursor}')
    #double confirm hostname availability in case the status is reflected correctly in the systems table

    email=input('\nenter email address of user: ').strip().lower()
    cursor.execute(f'select * from users where user=\'{email}\'')
    userDepartment=(list(cursor))[0][1].strip().lower()
    result=cursor.rowcount
    if result==0:
        print('user not found...please contact database admin')
        return
    else:
        print(f'{result} user(s) with username, \'{email}\' found')
    cursor.execute(f'select * from users where user=\'{email}\' and department=\'{userDepartment}\'')
    result=cursor.rowcount
    if result==0:
        print('department for user not found...please contact database admin')
        return
    else:
        print(f'{result} user(s) named \'{email}\' from department(s) named \'{userDepartment}\' found')
    if userDepartment==deviceDepartment:
        print('\ndepartments for user and device match...device can be issued to user')
    else:
        print('\ndepartments for user and device are different...please contact database admin')
        return
    # new user check ends

    date=input('enter date in this format: \'yyyy mmm dd\': ').strip().lower()
    print(f'\nsystems record for \'{hostname}\' before changes:')
    site, location, status=mysqlRead(cursor, 'systems', hostname)
    #modifications to systems and currown tables for device issuance
    cursor.execute(f'insert into currown values(\'{date}\', \'{hostname}\', \'{email}\')')
    cursor.execute(f'update systems set site=null, location=null, status=\'deployed\' where hostname=\'{hostname}\'')
    print(f'\nsystems record for \'{hostname}\' after changes:')
    mysqlRead(cursor, 'systems', hostname)
    print(f'\ncurrent owner record for \'{email}\' after insertion of new record:')
    mysqlRead(cursor, 'currown', hostname)
    commit=input('\ncommit? y/n: ')
    if(commit=='y'):
        conn.commit()
        print('\nmodifications saved!\n')
    else:
        print('\nno updates to database\n')

def devIssueRevert(conn, cursor, site, location, status):
    print()
    print(site, location, status)
    print()
    hostname=input('enter hostname to revert issuance: ')
    print(f'\nsystems record for \'{hostname}\' before revertion:')
    mysqlRead(cursor, 'systems', hostname)
    print(f'\ncurrent owner record for \'{hostname}\' before revertion:')
    mysqlRead(cursor, 'currown', hostname)
    cursor.execute(f'delete from currown where hostname=\'{hostname}\'')
    cursor.execute(f'update systems set site=\'{site}\', location=\'{location}\', status=\'{status}\' where hostname=\'{hostname}\';')
    print(f'\nsystems record for \'{hostname}\' after revertion:')
    mysqlRead(cursor, 'systems', hostname)
    print(f'\ncurrent owner record for \'{hostname}\' after revertion:')
    mysqlRead(cursor, 'currown', hostname)
    commit=input('\ncommit? y/n: ')
    if(commit=='y'):
        conn.commit()
        print('\nmodifications saved!\n')
    else:
        print('\nno updates to database\n')



def mysqlCreateSystems(cursor, table):
    brand, model, serial, hostname, type, shipdate, warrexp, site, location, devdep, status=input('enter brand, model, serial, hostname, type, shipdate, warrexp, site, location, devdep, status seperated by comma:\n').split(',')
    print(brand+'\n'+model+'\n'+serial+'\n'+hostname+'\n'+type+'\n'+shipdate+'\n'+warrexp+'\n'+site+'\n'+location+'\n'+devdep+'\n'+status)
    cursor.execute(f'insert into {table} (brand, model, serial, hostname, type, shipdate, warrexp, site, location, devdep, status) values("{brand}", "{model}", "{serial}", "{hostname}", "{type}", "{shipdate}", "{warrexp}", "{site}", "{location}", "{devdep}", "{status}")')

def mysqlCreateHistLog(cursor, table):
    date, hostname, user, log, remarks=input('enter date, hostname, user, log, remarks seperated by comma:\n').split(',')
    print(date+'\n'+hostname+'\n'+user+'\n'+log+'\n'+remarks)
    cursor.execute(f'insert into {table} (date, hostname, user, log, remarks) values("{date}", "{hostname}", "{user}", "{log}", "{remarks}")')

def mysqlCreatePrevOwn(cursor, table):
    date, hostname, user, log, remarks=input('enter date, hostname, user, log, remarks seperated by comma:\n').split(',')
    print(date+'\n'+hostname+'\n'+user+'\n'+log+'\n'+remarks)
    cursor.execute(f'insert into {table} (date, hostname, user, log, remarks) values("{date}", "{hostname}", "{user}", "{log}", "{remarks}")')

def mysqlCreateCurrOwn(cursor, table):
    date, hostname, user, log, remarks=input('enter date, hostname, user, log, remarks seperated by comma:\n').split(',')
    print(date+'\n'+hostname+'\n'+user+'\n'+log+'\n'+remarks)
    cursor.execute(f'insert into {table} (date, hostname, user, log, remarks) values("{date}", "{hostname}", "{user}", "{log}", "{remarks}")')

def mysqlRead(cursor, table, readParam):
    cursor.execute(f'select * from {table} where hostname=\'{readParam}\'')
    blah=[]
    for i in cursor:
        for j in i:
            blah.append(j)
    blah2=readColumns(cursor, table)
    print()
    for i in range(0, len(blah), 1):
        if(blah2[i]=='site'):
            site=blah[i]
        if(blah2[i]=='location'):
            location=blah[i]
        if(blah2[i]=='status'):
            status=blah[i]
        print(f'{blah2[i]: <12}: {blah[i]}')

def mysqlDelete(cursor, table, delParam):
    cursor.execute(f'delete from {table} where hostname=\'{delParam}\'')

def readColumns(cursor, table):
    cursor.execute(f'desc {table}')
    blah=[]
    for i in cursor:
        blah.append(i[0])
    return blah

def mysqlConnClose(conn):
    conn.close()

def choiceSelectTables(conn, cursor):
# n for new user
# r for resignation
# u for upgrade/swap
# s for systems
# h for histlogs
# p for prevown
# c for currown
    while True:
        table=input('''
enter an option:
i for device issuance
r for device issue revertion
x to exit
''')
        match table:
            # case 's':
            #     table='systems'
            # case 'h':
            #     table='histlogs'
            # case 'p':
            #     table='prevown'
            # case 'c':
            #     table='currown'
            case 'i':
                deviceIssue(conn, cursor)
            case 'r':
                devIssueRevert(conn, cursor, 'napier', 'server room', 'pending_deployment')
            case 'x':
                return table
            case _:
                print('wrong choice, only s, h, p, c or x allowed. ')
        # choiceSelectCrud(table, conn, cursor)

# def choiceSelectCrud(table, conn, cursor):
#     while True:
#         operation=input('enter c (create), r (read), d (delete), rc(read columns), x (exit): ')
#         match operation:
#             case 'c':
#                 match table:
#                     case 'systems':
#                         mysqlCreateSystems(cursor, table)
#                     case 'histlogs':
#                         mysqlCreateHistLog(cursor, table)
#                     case 'prevown':
#                         mysqlCreatePrevOwn(cursor, table)
#                     case 'currown':
#                         mysqlCreateCurrOwn(cursor, table)
#                 conn.commit()
#             case 'r': 
#                 readParam=input('enter hostname to read: ')
#                 mysqlRead(cursor, table, readParam)
#             case 'd': 
#                 delParam=input('enter hostname to delete: ')
#                 mysqlDelete(cursor, table, delParam)
#             case 'rc':
#                 blah=readColumns(cursor, table)
#                 print(blah)
#             case 'x':
#                 return operation
#             case _:
#                 print('wrong choice, only c, r, u, d or x is allowed.')

def main():
    conn, myCursor=mysqlConn()
    a=''
    while True:
        a=choiceSelectTables(conn, myCursor)
        if a=='x':
            print('\nbye!')
            mysqlConnClose(conn)
            return 0


main()