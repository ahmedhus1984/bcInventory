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

def getDetailsAddSystems():
    brand, model, serial, hostname, type, shipdate, warrexp, site, department=input('enter brand, model, serial, hostname, type, shipdate, warrexp, site, department seperated by comma:\n').split(',')
    return brand, model, serial, hostname, type, shipdate, warrexp, site, department

def getDetailsAddDeleteUser():
    email=input('\nenter email address of user: ').strip().lower()
    department=input('\nenter department of user: ').strip().lower()
    return email, department

def getDetailsReturn():
    hostname=input('\nenter hostname of device returned by user: ').strip().lower()
    email=input('\nenter email address of user: ').strip().lower()
    site=input('\nenter site to store returned device (eg. napier or toa payoh): ').strip().lower()
    date=input('\nenter date in this format: \'yyyy mmm dd\': ').strip().lower()
    return hostname, email, site, date

def getDetailsIssue():
    hostname=input('\nenter hostname of device to be issued to user: ').strip().lower()
    email=input('\nenter email address of user: ').strip().lower()
    date=input('\nenter date in this format: \'yyyy mmm dd\': ').strip().lower()
    return hostname, email, date

def getDetailsSwap():
    hostnameReturn=input('\nenter hostname of device to returned by user: ').strip().lower()
    hostnameIssue=input('\nenter hostname of device to issue to user: ').strip().lower() 
    email=input('\nenter email address of user: ').strip().lower()
    site=input('\nenter site to store returned device (eg. napier or toa payoh): ').strip().lower()
    date=input('\nenter date in this format: \'yyyy mmm dd\': ').strip().lower()
    return hostnameReturn, hostnameIssue, email, site, date

def addUser(conn, cursor, email, department):
    print(f'\nusers record for \'{email}\' before insertion of new record, {email}:')
    mysqlRead(cursor, 'users', 'user', email)
    
    #modifications to users table
    try:
        cursor.execute(f'insert into users values(\'{email}\', \'{department}\')')
    except:
        print('unable to insert user, please check if there is an existing record for the user or if any typo')
    #modifications to users table
    
    print(f'\nusers record for \'{email}\' after insertion of new record, {email}:')
    mysqlRead(cursor, 'users', 'user', email)
    
    #save modifications
    commit=input('\ncommit? y/n: ')
    if(commit=='y'):
        conn.commit()
        print('\nmodifications saved!\n')
    else:
        print('\nno updates to database\n')
    #save modifications

def delUser(conn, cursor, email):
    print(f'\nusers record for \'{email}\' before deletion of {email}:')
    mysqlRead(cursor, 'users', 'user', email)
    
    #modifications to users table
    try:
        cursor.execute(f'delete from users where user=\'{email}\'')
    except:
        print('unable to delete user, please check if there is an existing record for the user or if any typo')
    #modifications to users table
    
    print(f'\nusers record for \'{email}\' after deletion of {email}:')
    mysqlRead(cursor, 'users', 'user', email)
    
    #save modifications
    commit=input('\ncommit? y/n: ')
    if(commit=='y'):
        conn.commit()
        print('\nmodifications saved!\n')
    else:
        print('\nno updates to database\n')
    #save modifications

def deviceIssue(conn, cursor, hostname, email, date):
    #issue check begins
    cursor.execute(f'select department from systems where hostname=\'{hostname}\' and status=\'pending_deployment\'')
    result=cursor.rowcount
    if result==0:
        print(f'either host \'{hostname}\' not found or host \'{hostname}\' has a status other than \'pending_deployment\' in systems table\n\nplease contact database admin')
        return
    contents=cursor.fetchall()
    deviceDepartment=contents[0][0].strip().lower()
    #double confirm hostname availability in case the status is reflected incorrectly as 'pending_deployment'in the systems table
    cursor.execute(f'select * from currown where hostname=\'{hostname}\'')
    result=cursor.rowcount
    if result==0:
        print('hostname currently not in use, available for deployment')
    else:
        contents=cursor.fetchall()
        print(f'{result} hostname(s) named \'{hostname}\' currently in use by {contents[0][0]}...please contact database admin')
        return
    #double confirm hostname availability in case the status is reflected incorrectly as 'pending_deployment'in the systems table

    cursor.execute(f'select * from users where user=\'{email}\'')
    result=cursor.rowcount
    if result==0:
        print('user not found...please contact database admin')
        return
    else:
        contents=cursor.fetchall()
        userDepartment=contents[0][1].strip().lower()
        print(f'{result} user(s) with username, \'{email}\' found')
    if userDepartment==deviceDepartment:
        print('\ndepartments for user and device match...device can be issued to user')
    else:
        print('\ndepartments for user and device are different...please contact database admin')
        return
    #issue check ends

    print(f'\nsystems record for \'{hostname}\' before insertion of new record:')
    mysqlRead(cursor, 'systems', 'hostname', hostname)
    print(f'\ncurrent owner record for \'{email}\' before insertion of new record:')
    mysqlRead(cursor, 'currown', 'hostname', hostname)

    #modifications to systems and currown tables for device issuance
    cursor.execute(f'insert into currown values(\'{date}\', \'{hostname}\', \'{email}\')')
    cursor.execute(f'update systems set site=null, status=\'deployed\' where hostname=\'{hostname}\'')
    #modifications to systems and currown tables for device issuance

    print(f'\nsystems record for \'{hostname}\' after insertion of new record:')
    mysqlRead(cursor, 'systems', 'hostname', hostname)
    print(f'\ncurrent owner record for \'{email}\' after insertion of new record:')
    mysqlRead(cursor, 'currown', 'hostname', hostname)

    #save modifications
    commit=input('\ncommit? y/n: ')
    if(commit=='y'):
        conn.commit()
        print('\nmodifications saved!\n')
    else:
        print('\nno updates to database\n')
    #save modifications

def deviceReturn(conn, cursor, hostname, email, site, date):
    #return check begins
    cursor.execute(f'select department from systems where hostname=\'{hostname}\' and status=\'deployed\'')
    result=cursor.rowcount
    if result==0:
        print(f'either host \'{hostname}\' not found or host \'{hostname}\' has a status other than \'deployed\' in systems table\n\nplease contact database admin')
        return
    contents=cursor.fetchall()
    deviceDepartment=contents[0][0].strip().lower()
    #double confirm hostname availability in case the status is reflected incorrectly as 'pending_deployment'in the systems table
    cursor.execute(f'select * from currown where hostname=\'{hostname}\'')
    result=cursor.rowcount
    if result==1:
        print('hostname currently deployed, available for return')
    else:
        print(f'hostname \'{hostname}\' has no records for current owner...please contact database admin')
        return
    #double confirm hostname availability in case the status is reflected incorrectly as 'pending_deployment'in the systems table

    cursor.execute(f'select * from users where user=\'{email}\'')
    result=cursor.rowcount
    if result==0:
        print('user not found...please contact database admin')
        return
    else:
        contents=cursor.fetchall()
        userDepartment=contents[0][1].strip().lower()
        print(f'{result} user(s) with username, \'{email}\' found')
    if userDepartment==deviceDepartment:
        print('\ndepartments for user and device match...device can be returned by user')
    else:
        print('\ndepartments for user and device are different...please contact database admin')
        return
    #return check ends

    print(f'\nsystems info before update: ')
    mysqlRead(cursor, 'systems', 'hostname', hostname)
    print(f'\ncurrown info before update: ')
    mysqlRead(cursor, 'currown', 'hostname', hostname)
    print(f'\nprevown info before update: ')
    mysqlRead(cursor, 'prevown', 'hostname', hostname)

    #modifications to systems and currown tables for device issuance 
    cursor.execute(f'insert into prevown select * from currown where hostname=\'{hostname}\' and user=\'{email}\'')
    cursor.execute(f'update prevown set date=\'{date}\' where hostname=\'{hostname}\' and user=\'{email}\'')
    cursor.execute(f'delete from currown where hostname=\'{hostname}\' and user=\'{email}\'')
    cursor.execute(f'update systems set site=\'{site}\', status=\'pending_deployment\' where hostname=\'{hostname}\'')
    #modifications to systems and currown tables for device issuance
    
    print(f'\nsystems info after update: ')
    mysqlRead(cursor, 'systems', 'hostname', hostname)
    print(f'\ncurrown info after update: ')
    mysqlRead(cursor, 'currown', 'hostname', hostname)
    print(f'\nprevown info after update: ')
    mysqlRead(cursor, 'prevown', 'hostname', hostname)

    #save modifications
    commit=input('\ncommit? y/n: ')
    if(commit=='y'):
        conn.commit()
        print('\nmodifications saved!\n')
        return 0
    else:
        print('\nno updates to database\n')
        return 1
    #save modifications

def deviceSwap(conn, cursor, hostnameReturn, hostnameIssue, email, site, date):
    a=deviceReturn(conn, cursor, hostnameReturn, email, site, date)
    if a==0:
        deviceIssue(conn, cursor, hostnameIssue, email, date)
    else:
        print('swap safely aborted')

def addSystem(conn, cursor, brand, model, serial, hostname, type, shipdate, warrexp, site, department):
    print(f'\nsystems record for \'{hostname}\' before insertion:')
    mysqlRead(cursor, 'systems', 'hostname', hostname)

    #modifications to users table
    try:
        cursor.execute(f'insert into systems (brand, model, serial, hostname, type, shipdate, warrexp, site, department) values("{brand}", "{model}", "{serial}", "{hostname}", "{type}", "{shipdate}", "{warrexp}", "{site}", "{department}")')
    except:
        print(f'unable to insert new machine, \'{hostname}\' into systems table')
    #modifications to users table

    print(f'\nsystems record for \'{hostname}\' after insertion:')
    mysqlRead(cursor, 'systems', 'hostname', hostname)

    #save modifications
    commit=input('\ncommit? y/n: ')
    if(commit=='y'):
        conn.commit()
        print('\nmodifications saved!\n')
    else:
        print('\nno updates to database\n')
    #save modifications


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

def mysqlRead(cursor, table, column, readParam):
    cursor.execute(f'select * from {table} where {column}=\'{readParam}\'')
    blah=cursor.fetchall()
    blah2=readColumns(cursor, table)
    print('########################################')
    for i in range(0, len(blah), 1):
        for j in range(0, len(blah2), 1):
            print(f'{blah2[j]: <12}: {blah[i][j]}')
        print('########################################')
    print('########################################')

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
    hostnameIssue=''
    hostnameReturn=''
    email=''
    department=''
    site=''
    date=''
    while True:
        table=input('''
enter an option:
                    
a for adding user
d for deleting user
as for adding a machine
i for device issuance
r for device return
s for device swap
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
                hostnameIssue, email, date=getDetailsIssue()
                deviceIssue(conn, cursor, hostnameIssue, email, date)
            case 'r':
                hostnameIssue, email, site, date=getDetailsReturn()
                deviceReturn(conn, cursor, hostnameIssue, email, site, date)
            case 's':
                hostnameReturn, hostnameIssue, email, site, date=getDetailsSwap()
                deviceSwap(conn, cursor, hostnameReturn, hostnameIssue, email, site, date)
            case 'a':
                email, department=getDetailsAddDeleteUser()
                addUser(conn, cursor, email, department)
            case 'd':
                email, department=getDetailsAddDeleteUser()
                delUser(conn, cursor, email)
            case 'as':
                brand, model, serial, hostname, type, shipdate, warrexp, site, department=getDetailsAddSystems()
                addSystem(conn, cursor, brand, model, serial, hostname, type, shipdate, warrexp, site, department)
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
#                 mysqlRead(cursor, table, 'hostname', readParam)
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