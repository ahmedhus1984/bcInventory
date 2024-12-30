import mysql.connector
import json

def load_credentials(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

def mysqlConn():
    credentials_file = 'db.json'
    credentials = load_credentials(credentials_file)
    conn=mysql.connector.connect(host=credentials['mysql_host'], user=credentials['mysql_user'], passwd=credentials['mysql_password'], db=credentials['mysql_db'])
    if conn.is_connected():
        myCursor=mysqlCursor(conn)
        if myCursor:
            return conn, myCursor
    conn.close()
    return False

def mysqlCursor(conn):
    myCursor=conn.cursor(buffered=True)
    if not myCursor:
        return False
    return myCursor

def connClose(conn, cursor):
    cursor.close()
    conn.close()

def getDetailsSearch():
    table, column, param=input('enter table, column and param seperated by comma:\n').split(',')
    return table, column, param

def mysqlSearch(table, column, readParam):
    conn, cursor=mysqlConn()
    query=f'SELECT * FROM {table} WHERE {column} = %s'
    cursor.execute(query, (readParam,))
    blah=cursor.fetchall()
    if len(blah)!=0:
        blah2=readColumns(cursor, table)
        blah3=[]
        for i in range(0, len(blah), 1):
            blah3.append('########################################')
            for j in range(0, len(blah2), 1):
                blah3.append(f'{blah2[j]: <12}: {blah[i][j]}')
        blah3.append('########################################')
        connClose(conn, cursor)
        return blah3
    connClose(conn, cursor)
    return None

def readColumns(cursor, table):
    query=f'desc {table}'
    cursor.execute(query)
    blah=[]
    for i in cursor:
        blah.append(i[0])
    return blah

def getDetailsLogs():
    date, hostname, user, remarks=input('enter date, hostname, user, remarks seperated by comma:\n').split(',')
    return date, hostname, user, remarks

def addLogs(date, hostname, user, remarks):
    conn, cursor=mysqlConn()
    try:
        cursor.execute(f'insert into logs(date, hostname, user, remarks) values("{date}", "{hostname}", "{user}", "{remarks}")')
    except:
        return False
    conn.commit()
    conn.close()
    return True

def getDetailsAddDeleteUser():
    email=input('\nenter email address of user: ').strip().lower()
    department=input('\nenter department of user: ').strip().lower()
    return email, department

def preAddUser(email):
    myString=[]
    myString.append(f'\nusers record for \'{email}\' before insertion:')
    myString2=mysqlSearch('users', 'user', email)
    if myString2:
        for i in myString2:
            myString.append(i)
    return myString

def addUser(email, department):
    conn, cursor=mysqlConn()
    try:
        cursor.execute(f'insert into users values(\'{email}\', \'{department}\')')
    except:
        connClose(conn, cursor)
        return False
    conn.commit()
    connClose(conn, cursor)
    return True


def postAddUser(email):
    myString=[]
    myString.append(f'\nusers record for \'{email}\' after insertion:')
    myString2=mysqlSearch('users', 'user', email)
    if myString2:
        for i in myString2:
            myString.append(i)
    return myString

def preDelUser(email):
    myString=[]
    myString.append(f'\nusers record for \'{email}\' before deletion:')
    myString2=mysqlSearch('users', 'user', email)
    if myString2:
        for i in myString2:
            myString.append(i)
    return myString

def delUser(email, department): 
    conn, cursor=mysqlConn()
    try:
        cursor.execute(f'delete from users where user=\'{email}\' and department=\'{department}\'')
    except:
        connClose(conn, cursor)
        return False
    conn.commit()
    connClose(conn, cursor)
    return True

def postDelUser(email):
    myString=[]
    myString.append(f'\nusers record for \'{email}\' after deletion:')
    myString2=mysqlSearch('users', 'user', email)
    if myString2:
        for i in myString2:
            if i:
                myString.append(i)
    return myString

def getDetailsAddSystem():
    brand, model, serial, hostname, type, shipdate, warrexp, site, department=input('enter brand, model, serial, hostname, type, shipdate, warrexp, site, department seperated by comma:\n').split(',')
    return brand, model, serial, hostname, type, shipdate, warrexp, site, department

def preAddSystem(hostname):
    myString=[]
    myString.append(f'\nsystems record for \'{hostname}\' before insertion:')
    myString2=mysqlSearch('systems', 'hostname', hostname)
    if myString2:
        for i in myString2:
            myString.append(i)
    return myString

def addSystem(brand, model, serial, hostname, type, shipdate, warrexp, site, department):
    conn, cursor=mysqlConn()
    try:
        cursor.execute(f'insert into systems (brand, model, serial, hostname, type, shipdate, warrexp, site, department) values("{brand}", "{model}", "{serial}", "{hostname}", "{type}", "{shipdate}", "{warrexp}", "{site}", "{department}")')
    except:
        connClose(conn, cursor)
        return False
    conn.commit()
    connClose(conn, cursor)
    return True

def postAddSystem(hostname):
    myString=[]
    myString.append(f'\nsystems record for \'{hostname}\' after insertion:')
    myString2=mysqlSearch('systems', 'hostname', hostname)
    if myString2:
        for i in myString2:
            myString.append(i)
    return myString

def getDetailsDelSystem():
    hostname=input('enter hostname to delete:\n')
    return hostname

def preDelSystem(hostname):
    myString=[]
    myString.append(f'\nsystems record for \'{hostname}\' before deletion:')
    myString2=mysqlSearch('systems', 'hostname', hostname)
    if myString2:
        for i in myString2:
            myString.append(i)
    return myString

def delSystem(hostname):
    conn, cursor=mysqlConn()   
    try:
        cursor.execute(f'delete from systems where hostname=\'{hostname}\'')
    except:
        connClose(conn, cursor)
        return False
    conn.commit()
    connClose(conn, cursor)
    return True

def postDelSystem(hostname):
    myString=[]
    myString.append(f'\nsystems record for \'{hostname}\' after deletion:')
    myString2=mysqlSearch('systems', 'hostname', hostname)
    if myString2:
        for i in myString2:
            myString.append(i)
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
        conn.close()
        return False
    contents=cursor.fetchall()
    deviceDepartment=contents[0][0].strip().lower()
    #double confirm hostname availability in case the status is reflected incorrectly as 'pending_deployment'in the systems table
    cursor.execute(f'select * from currown where hostname=\'{hostname}\'')
    result=cursor.rowcount
    if result!=0:
        contents=cursor.fetchall()
        conn.close()
        return False
    #double confirm hostname availability in case the status is reflected incorrectly as 'pending_deployment'in the systems table
    cursor.execute(f'select * from users where user=\'{email}\'')
    result=cursor.rowcount
    if result==0:
        conn.close()
        return False
    else:
        contents=cursor.fetchall()
        userDepartment=contents[0][1].strip().lower()
    if userDepartment==deviceDepartment:
        conn.close()
        return True
    else:
        conn.close()
        return False

def preDeviceIssueStatus(hostname):
    conn, cursor=mysqlConn()
    systemsString=[]
    systemsString.append(f'\nsystems record before issue:')
    systemsString2=mysqlSearch('systems', 'hostname', hostname)
    for i in systemsString2:
        systemsString.append(i)
    currownString=[]
    currownString.append(f'\ncurrent owner record before issue:')
    currownString2=mysqlSearch('currown', 'hostname', hostname)
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
        return False
    conn.commit()
    conn.close()
    return True

def postDeviceIssueStatus(hostname):
    conn, cursor=mysqlConn()
    systemsString=[]
    systemsString.append(f'\nsystems record after issue:')
    systemsString2=mysqlSearch('systems', 'hostname', hostname)
    for i in systemsString2:
        systemsString.append(i)
    currownString=[]
    currownString.append(f'\ncurrent owner record after issue:')
    currownString2=mysqlSearch('currown', 'hostname', hostname)
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
        conn.close()
        return False
    contents=cursor.fetchall()
    deviceDepartment=contents[0][0].strip().lower()
    #double confirm hostname availability in case the status is reflected incorrectly as 'pending_deployment'in the systems table
    cursor.execute(f'select * from currown where hostname=\'{hostname}\'')
    result=cursor.rowcount
    if result!=1:
        conn.close()
        return False
    #double confirm hostname availability in case the status is reflected incorrectly as 'pending_deployment'in the systems table
    cursor.execute(f'select * from users where user=\'{email}\'')
    result=cursor.rowcount
    if result==0:
        conn.close()
        return False
    else:
        contents=cursor.fetchall()
        userDepartment=contents[0][1].strip().lower()
    if userDepartment==deviceDepartment:
        conn.close()
        return True
    else:
        conn.close()
        return False

def preDeviceReturnStatus(hostname):
    conn, cursor=mysqlConn()
    systemsString=[]
    systemsString.append(f'\nsystems record before return:')
    systemsString2=mysqlSearch('systems', 'hostname', hostname)
    for i in systemsString2:
        systemsString.append(i)
    currownString=[]
    currownString.append(f'\ncurrent owner record before return:')
    currownString2=mysqlSearch('currown', 'hostname', hostname)
    for i in currownString2:
        currownString.append(i)
    prevownString=[]
    prevownString.append(f'\nprevious owner record before return:')
    prevownString2=mysqlSearch('prevown', 'hostname', hostname)
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
        return False
    conn.commit()
    conn.close()
    return True

def postDeviceReturnStatus(hostname):
    conn, cursor=mysqlConn()
    systemsString=[]
    systemsString.append(f'\nsystems record after return:')
    systemsString2=mysqlSearch('systems', 'hostname', hostname)
    for i in systemsString2:
        systemsString.append(i)
    currownString=[]
    currownString.append(f'\ncurrent owner record after return:')
    currownString2=mysqlSearch('currown', 'hostname', hostname)
    for i in currownString2:
        currownString.append(i)
    prevownString=[]
    prevownString.append(f'\nprevious owner record after return:')
    prevownString2=mysqlSearch('prevown', 'hostname', hostname)
    for i in prevownString2:
        prevownString.append(i)
    conn.close()
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
        return False
    return True

def swapDeviceReturn(cursor, hostname, email, site, date):
    try:
        cursor.execute(f'insert into prevown select * from currown where hostname=\'{hostname}\' and user=\'{email}\'')
        cursor.execute(f'update prevown set date=\'{date}\' where hostname=\'{hostname}\' and user=\'{email}\'')
        cursor.execute(f'delete from currown where hostname=\'{hostname}\' and user=\'{email}\'')
        cursor.execute(f'update systems set site=\'{site}\', status=\'pending_deployment\' where hostname=\'{hostname}\'')
    except:
        return False
    return True

def deviceSwap(hostnameReturn, hostnameIssue, email, site, date):
    conn, cursor=mysqlConn()
    x=False
    returnList=[]
    issueList=[]
    returnIssueList=[]
    if(deviceReturnChecks(hostnameReturn, email)):
        if(deviceIssueChecks(hostnameIssue, email)):
            returnList.append(preDeviceReturnStatus(hostnameReturn))
            issueList.append(preDeviceIssueStatus(hostnameIssue))
            if swapDeviceReturn(cursor, hostnameReturn, email, site, date):
                returnList.append(postDeviceReturnStatus(hostnameReturn))
                returnIssueList.append(returnList)
                if swapDeviceIssue(cursor, hostnameIssue, email, date):
                    issueList.append(postDeviceIssueStatus(hostnameIssue))
                    returnIssueList.append(issueList)
                    conn.commit()
                    conn.close()
                    x=returnIssueList
    conn.close()
    return x

def choiceSelectTables():
    # hostnameIssue=''
    # hostnameReturn=''
    # email=''
    # department=''
    # site=''
    # date=''
    # user=''
    # remarks=''
    # tableName=''
    # columnName=''
    # searchParam=''
    while True:
        table=input('''
enter an option:
f for searching the database
as for adding a machine
ds for deleting a machine 
a for adding user
d for deleting user
i for device issuance
r for device return
s for device swap
l for logging
x to exit

''')
        match table:
            case 'f':
                tableName, columnName, searchParam=getDetailsSearch()
                print()
                x=mysqlSearch(tableName, columnName, searchParam)
                if x:
                    for i in x:
                        print(i)
                    print()
                else:
                    print(f'\'{searchParam}\' not found in column, \'{columnName}\' in table, \'{tableName}\'')
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
            case 'l':
                date, hostname, user, remarks=getDetailsLogs()
                addLogs(date, hostname, user, remarks)
            case 'x':
                return table
            case _:
                print('wrong choice, only s, h, p, c or x allowed. ')