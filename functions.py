import mysql.connector
import yaml

def mysqlConn():
    database=yaml.safe_load(open('db.yaml'))
    conn=mysql.connector.connect(host=database['mysql_host'], user=database['mysql_user'], passwd=database['mysql_password'], db=database['mysql_db'])
    if not conn.is_connected():
        print('unable to connect to sql server.')
        exit(1)
    else:
        # print('connection success!!!')
        myCursor=mysqlCursor(conn)
        return conn, myCursor

def mysqlCursor(conn):
    myCursor=conn.cursor(buffered=True)
    if not myCursor:
        print('unable to create cursor')
        conn.close()
        exit(1)
    return myCursor

def mysqlRead(cursor, table, column, readParam):
    cursor.execute(f'select * from {table} where {column}=\'{readParam}\'')
    blah=cursor.fetchall()
    blah2=readColumns(cursor, table)
    blah3=[]
    blah3.append('########################################')
    for i in range(0, len(blah), 1):
        for j in range(0, len(blah2), 1):
            blah3.append(f'{blah2[j]: <12}: {blah[i][j]}')
        blah3.append('########################################')
    blah3.append('########################################')
    return blah3

def readColumns(cursor, table):
    cursor.execute(f'desc {table}')
    blah=[]
    for i in cursor:
        blah.append(i[0])
    return blah

def getDetailsAddDeleteUser():
    email=input('\nenter email address of user: ').strip().lower()
    department=input('\nenter department of user: ').strip().lower()
    return email, department

def preAddUser(email):
    conn, cursor=mysqlConn()
    myString=[]
    myString.append(f'\nusers record for \'{email}\' before insertion:')
    myString2=mysqlRead(cursor, 'users', 'user', email)
    for i in myString2:
        myString.append(i)
    conn.close()
    return myString

def addUser(email, department):
    conn, cursor=mysqlConn()
    try:
        cursor.execute(f'insert into users values(\'{email}\', \'{department}\')')
    except:
        print('unable to insert user, please check if there is an existing record for the user or if any typo')
        return False
    conn.commit()
    conn.close()
    return True


def postAddUser(email):
    conn, cursor=mysqlConn()
    myString=[]
    myString.append(f'\nusers record for \'{email}\' after insertion:')
    myString2=mysqlRead(cursor, 'users', 'user', email)
    for i in myString2:
        myString.append(i)
    conn.close()
    return myString

def preDelUser(email):
    conn, cursor=mysqlConn()
    myString=[]
    myString.append(f'\nusers record for \'{email}\' before deletion:')
    myString2=mysqlRead(cursor, 'users', 'user', email)
    for i in myString2:
        myString.append(i)
    conn.close()
    return myString

def delUser(email, department): 
    conn, cursor=mysqlConn()
    try:
        cursor.execute(f'select * from users where user=\'{email}\' and department=\'{department}\'')
    except:
        return False
    blah=cursor.fetchall()
    if len(blah)==0:
        return False
    try:
        cursor.execute(f'delete from users where user=\'{email}\' and department=\'{department}\'')
    except:
        return False
    conn.commit()
    conn.close()
    return True

def postDelUser(email):
    conn, cursor=mysqlConn()
    myString=[]
    myString.append(f'\nusers record for \'{email}\' after deletion:')
    myString2=mysqlRead(cursor, 'users', 'user', email)
    for i in myString2:
        if i:
            myString.append(i)
    conn.close()
    return myString

def getDetailsAddSystem():
    brand, model, serial, hostname, type, shipdate, warrexp, site, department=input('enter brand, model, serial, hostname, type, shipdate, warrexp, site, department seperated by comma:\n').split(',')
    return brand, model, serial, hostname, type, shipdate, warrexp, site, department

def preAddSystem(hostname):
    conn, cursor=mysqlConn()
    myString=[]
    myString.append(f'\nsystems record for \'{hostname}\' before insertion:')
    myString2=mysqlRead(cursor, 'systems', 'hostname', hostname)
    for i in myString2:
        myString.append(i)
    conn.close()
    return myString

def addSystem(brand, model, serial, hostname, type, shipdate, warrexp, site, department):
    conn, cursor=mysqlConn()
    try:
        cursor.execute(f'insert into systems (brand, model, serial, hostname, type, shipdate, warrexp, site, department) values("{brand}", "{model}", "{serial}", "{hostname}", "{type}", "{shipdate}", "{warrexp}", "{site}", "{department}")')
    except:
        print(f'unable to insert new machine, \'{hostname}\' into systems table')
        return False
    conn.commit()
    conn.close()
    return True

def postAddSystem(hostname):
    conn, cursor=mysqlConn()
    myString=[]
    myString.append(f'\nsystems record for \'{hostname}\' after insertion:')
    myString2=mysqlRead(cursor, 'systems', 'hostname', hostname)
    for i in myString2:
        myString.append(i)
    conn.close()
    return myString

def getDetailsDelSystem():
    hostname=input('enter hostname to delete:\n')
    return hostname

def preDelSystem(hostname):
    conn, cursor=mysqlConn()
    myString=[]
    myString.append(f'\nsystems record for \'{hostname}\' before deletion:')
    myString2=mysqlRead(cursor, 'systems', 'hostname', hostname)
    for i in myString2:
        myString.append(i)
    conn.close()
    return myString

def delSystem(hostname):
    conn, cursor=mysqlConn()
    try:
        cursor.execute(f'select * from systems where hostname=\'{hostname}\'')
    except:
        return False
    blah=cursor.fetchall()
    if len(blah)==0:
        return False    
    try:
        cursor.execute(f'delete from systems where hostname=\'{hostname}\'')
    except:
        return False
    conn.commit()
    conn.close()
    return True

def postDelSystem(hostname):
    conn, cursor=mysqlConn()
    myString=[]
    myString.append(f'\nsystems record for \'{hostname}\' after deletion:')
    myString2=mysqlRead(cursor, 'systems', 'hostname', hostname)
    for i in myString2:
        myString.append(i)
    conn.close()
    return myString

def getDetailsIssue():
    hostname=input('\nenter hostname of device to be issued to user: ').strip().lower()
    email=input('\nenter email address of user: ').strip().lower()
    date=input('\nenter date in this format: \'yyyy mmm dd\': ').strip().lower()
    return hostname, email, date

def deviceIssueChecks(hostname, email):
    conn, cursor=mysqlConn()
    cursor.execute(f'select department from systems where hostname=\'{hostname}\' and status=\'pending_deployment\'')
    result=cursor.rowcount
    if result==0:
        print(f'either host \'{hostname}\' not found or host \'{hostname}\' has a status other than \'pending_deployment\' in systems table\n\nplease contact database admin')
        conn.close()
        return False
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
        conn.close()
        return False
    #double confirm hostname availability in case the status is reflected incorrectly as 'pending_deployment'in the systems table
    cursor.execute(f'select * from users where user=\'{email}\'')
    result=cursor.rowcount
    if result==0:
        print('user not found...please contact database admin')
        conn.close()
        return False
    else:
        contents=cursor.fetchall()
        userDepartment=contents[0][1].strip().lower()
        print(f'{result} user(s) with username, \'{email}\' found')
    if userDepartment==deviceDepartment:
        print('\ndepartments for user and device match...device can be issued to user')
        conn.close()
        return True
    else:
        print('\ndepartments for user and device are different...please contact database admin')
        conn.close()
        return False

def preDeviceIssueStatus(hostname):
    conn, cursor=mysqlConn()
    systemsString=[]
    systemsString.append(f'\nsystems record before issue:')
    systemsString2=mysqlRead(cursor, 'systems', 'hostname', hostname)
    for i in systemsString2:
        systemsString.append(i)
    currownString=[]
    currownString.append(f'\ncurrent owner record before issue:')
    currownString2=mysqlRead(cursor, 'currown', 'hostname', hostname)
    for i in currownString2:
        currownString.append(i)
    conn.close()
    return systemsString, currownString


def deviceIssue(hostname, email, date):
    conn, cursor=mysqlConn()
    try:
        cursor.execute(f'insert into currown values(\'{date}\', \'{hostname}\', \'{email}\')')
        cursor.execute(f'update systems set site=null, status=\'deployed\' where hostname=\'{hostname}\'')
    except:
        print(f'unable to make modifications for issuance of device \'{hostname}\' to user \'{email}\' into systems table')
        return False
    conn.commit()
    conn.close()
    return True

def postDeviceIssueStatus(hostname):
    conn, cursor=mysqlConn()
    systemsString=[]
    systemsString.append(f'\nsystems record after issue:')
    systemsString2=mysqlRead(cursor, 'systems', 'hostname', hostname)
    for i in systemsString2:
        systemsString.append(i)
    currownString=[]
    currownString.append(f'\ncurrent owner record after issue:')
    currownString2=mysqlRead(cursor, 'currown', 'hostname', hostname)
    for i in currownString2:
        currownString.append(i)
    conn.close()
    return systemsString, currownString



def getDetailsReturn():
    hostname=input('\nenter hostname of device returned by user: ').strip().lower()
    email=input('\nenter email address of user: ').strip().lower()
    site=input('\nenter site to store returned device (eg. napier or toa payoh): ').strip().lower()
    date=input('\nenter date in this format: \'yyyy mmm dd\': ').strip().lower()
    return hostname, email, site, date

def deviceReturnChecks(hostname, email):
    conn, cursor=mysqlConn()
    cursor.execute(f'select department from systems where hostname=\'{hostname}\' and status=\'deployed\'')
    result=cursor.rowcount
    if result==0:
        print(f'either host \'{hostname}\' not found or host \'{hostname}\' has a status other than \'deployed\' in systems table\n\nplease contact database admin')
        conn.close()
        return False
    contents=cursor.fetchall()
    deviceDepartment=contents[0][0].strip().lower()
    #double confirm hostname availability in case the status is reflected incorrectly as 'pending_deployment'in the systems table
    cursor.execute(f'select * from currown where hostname=\'{hostname}\'')
    result=cursor.rowcount
    if result==1:
        print('hostname currently deployed, available for return')
    else:
        print(f'hostname \'{hostname}\' has no records for current owner...please contact database admin')
        conn.close()
        return False
    #double confirm hostname availability in case the status is reflected incorrectly as 'pending_deployment'in the systems table
    cursor.execute(f'select * from users where user=\'{email}\'')
    result=cursor.rowcount
    if result==0:
        print('user not found...please contact database admin')
        conn.close()
        return False
    else:
        contents=cursor.fetchall()
        userDepartment=contents[0][1].strip().lower()
        print(f'{result} user(s) with username, \'{email}\' found')
    if userDepartment==deviceDepartment:
        print('\ndepartments for user and device match...device can be returned by user')
        conn.close()
        return True
    else:
        print('\ndepartments for user and device are different...please contact database admin')
        conn.close()
        return False

def preDeviceReturnStatus(hostname):
    conn, cursor=mysqlConn()
    systemsString=[]
    systemsString.append(f'\nsystems record before return:')
    systemsString2=mysqlRead(cursor, 'systems', 'hostname', hostname)
    for i in systemsString2:
        systemsString.append(i)
    currownString=[]
    currownString.append(f'\ncurrent owner record before return:')
    currownString2=mysqlRead(cursor, 'currown', 'hostname', hostname)
    for i in currownString2:
        currownString.append(i)
    prevownString=[]
    prevownString.append(f'\nprevious owner record before return:')
    prevownString2=mysqlRead(cursor, 'prevown', 'hostname', hostname)
    for i in prevownString2:
        prevownString.append(i)
    conn.close()
    return systemsString, currownString, prevownString

def deviceReturn(hostname, email, site, date):
    conn, cursor=mysqlConn()
    try:
        cursor.execute(f'insert into prevown select * from currown where hostname=\'{hostname}\' and user=\'{email}\'')
        cursor.execute(f'update prevown set date=\'{date}\' where hostname=\'{hostname}\' and user=\'{email}\'')
        cursor.execute(f'delete from currown where hostname=\'{hostname}\' and user=\'{email}\'')
        cursor.execute(f'update systems set site=\'{site}\', status=\'pending_deployment\' where hostname=\'{hostname}\'')
    except:
        print(f'unable to make modifications for return of device \'{hostname}\' to user \'{email}\' into systems table')
        return False
    conn.commit()
    conn.close()
    return True

def postDeviceReturnStatus(hostname):
    conn, cursor=mysqlConn()
    systemsString=[]
    systemsString.append(f'\nsystems record after return:')
    systemsString2=mysqlRead(cursor, 'systems', 'hostname', hostname)
    for i in systemsString2:
        systemsString.append(i)
    currownString=[]
    currownString.append(f'\ncurrent owner record after return:')
    currownString2=mysqlRead(cursor, 'currown', 'hostname', hostname)
    for i in currownString2:
        currownString.append(i)
    prevownString=[]
    prevownString.append(f'\nprevious owner record after return:')
    prevownString2=mysqlRead(cursor, 'prevown', 'hostname', hostname)
    for i in prevownString2:
        prevownString.append(i)
    conn.close()
    print(systemsString)
    print(currownString)
    print(prevownString)
    return systemsString, currownString, prevownString



def getDetailsSwap():
    hostnameReturn=input('\nenter hostname of device to returned by user: ').strip().lower()
    hostnameIssue=input('\nenter hostname of device to issue to user: ').strip().lower() 
    email=input('\nenter email address of user: ').strip().lower()
    site=input('\nenter site to store returned device (eg. napier or toa payoh): ').strip().lower()
    date=input('\nenter date in this format: \'yyyy mmm dd\': ').strip().lower()
    return hostnameReturn, hostnameIssue, email, site, date

def swapDeviceIssue(cursor, hostname, email, date):
    try:
        cursor.execute(f'insert into currown values(\'{date}\', \'{hostname}\', \'{email}\')')
        cursor.execute(f'update systems set site=null, status=\'deployed\' where hostname=\'{hostname}\'')
    except:
        print(f'unable to make modifications for issuance of device \'{hostname}\' to user \'{email}\' into systems table')
        return False
    return True

def swapDeviceReturn(cursor, hostname, email, site, date):
    try:
        cursor.execute(f'insert into prevown select * from currown where hostname=\'{hostname}\' and user=\'{email}\'')
        cursor.execute(f'update prevown set date=\'{date}\' where hostname=\'{hostname}\' and user=\'{email}\'')
        cursor.execute(f'delete from currown where hostname=\'{hostname}\' and user=\'{email}\'')
        cursor.execute(f'update systems set site=\'{site}\', status=\'pending_deployment\' where hostname=\'{hostname}\'')
    except:
        print(f'unable to make modifications for return of device \'{hostname}\' to user \'{email}\' into systems table')
        return False
    return True

def deviceSwap(hostnameReturn, hostnameIssue, email, site, date):
    conn, cursor=mysqlConn()
    returnList=[]
    issueList=[]
    returnIssueList=[]
    if(deviceReturnChecks(hostnameReturn, email)):
        if(deviceIssueChecks(hostnameIssue, email)):
            print()
            returnList.append(preDeviceReturnStatus(hostnameReturn))
            print()
            issueList.append(preDeviceIssueStatus(hostnameIssue))
            print()
            if swapDeviceReturn(cursor, hostnameReturn, email, site, date):
                returnList.append(postDeviceReturnStatus(hostnameReturn))
                returnIssueList.append(returnList)
                if swapDeviceIssue(cursor, hostnameIssue, email, date):
                    issueList.append(postDeviceIssueStatus(hostnameIssue))
                    returnIssueList.append(issueList)
                    conn.commit()
                    conn.close()
                    return returnIssueList
    conn.close()
    return 'swap update failed but safely aborted'

def mysqlCreateHistLog(cursor, table):
    date, hostname, user, log, remarks=input('enter date, hostname, user, log, remarks seperated by comma:\n').split(',')
    print(date+'\n'+hostname+'\n'+user+'\n'+log+'\n'+remarks)
    cursor.execute(f'insert into {table} (date, hostname, user, log, remarks) values("{date}", "{hostname}", "{user}", "{log}", "{remarks}")')

def choiceSelectTables():
    hostnameIssue=''
    hostnameReturn=''
    email=''
    department=''
    site=''
    date=''
    while True:
        table=input('''
enter an option:

as for adding a machine
ds for deleting a machine 
a for adding user
d for deleting user
i for device issuance
r for device return
s for device swap
x to exit

''')
        match table:
            case 'i':
                hostnameIssue, email, date=getDetailsIssue()
                if(deviceIssueChecks(hostnameIssue, email)):
                    print()
                    print(preDeviceIssueStatus(hostnameIssue))
                    print()
                    deviceIssue(hostnameIssue, email, date)
                    print()
                    print(postDeviceIssueStatus(hostnameIssue))
                    print()
            case 'r':
                hostnameReturn, email, site, date=getDetailsReturn()
                if(deviceReturnChecks(hostnameReturn, email)):
                    print()
                    print(preDeviceReturnStatus(hostnameReturn))
                    print()
                    deviceReturn(hostnameReturn, email, site, date)
                    print()
                    print(postDeviceReturnStatus(hostnameReturn))
                    print()
            case 's':
                hostnameReturn, hostnameIssue, email, site, date=getDetailsSwap()
                print()
                print(deviceSwap(hostnameReturn, hostnameIssue, email, site, date))
                print()
            case 'a':
                email, department=getDetailsAddDeleteUser()
                print()
                print(preAddUser(email))
                print()
                addUser(email, department)
                print()
                print(postAddUser(email))
                print()
            case 'd':
                email, department=getDetailsAddDeleteUser()
                print()
                print(preDelUser(email))
                print()
                delUser(email, department)
                print()
                print(postDelUser(email))
                print()
            case 'as':
                brand, model, serial, hostname, deviceType, shipdate, warrexp, site, department=getDetailsAddSystem()
                print()
                print(preAddSystem(hostname))
                print()
                addSystem(brand, model, serial, hostname, deviceType, shipdate, warrexp, site, department)
                print()
                print(postAddSystem(hostname))
                print()
            case 'ds':
                hostname=getDetailsDelSystem()
                print()
                print(preDelSystem(hostname))
                print()
                delSystem(hostname)
                print()
                print(postDelSystem(hostname))
                print()
            case 'x':
                return table
            case _:
                print('wrong choice, only s, h, p, c or x allowed. ')