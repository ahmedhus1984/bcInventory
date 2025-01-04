import mysql.connector
import json

def load_credentials(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

def mysqlConn():
    credentials_file = 'C:\\Users\\MLSI-HusseinAhmed\\source\\repos\\web_development\\bcInventory\\db.json'
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
    hostname=input('enter hostname:\n')
    return hostname

def mysqlRead(cursor, table, column, param):
    query=f'SELECT * FROM {table} WHERE {column} = %s'
    cursor.execute(query, (param,))
    blah1=cursor.fetchall()
    blahColumns=readColumns(cursor, table)
    blahTemp=[]
    for i in range(0, len(blah1), 1):
        for j in range(0, len(blahColumns), 1):
            blahTemp.append(f'{blahColumns[j]: <12}: {blah1[i][j]}')
    return blahTemp   

def mysqlSearch(cursor, hostname):
    blahMain=[]
    blahTemp=[]
    blahTemp2=[]

    blahTemp.append(f'systems record for {hostname}:')
    blahTemp2=mysqlRead(cursor, 'systems', 'hostname', hostname)
    for i in blahTemp2:
        blahTemp.append(i)
    blahMain.append(blahTemp)
    blahTemp=[]

    blahTemp.append(f'currown record for {hostname}:')
    blahTemp2=mysqlRead(cursor, 'currown', 'hostname', hostname)
    for i in blahTemp2:
        blahTemp.append(i)
    blahMain.append(blahTemp)
    blahTemp=[]
    
    blahTemp.append(f'prevown record for {hostname}:')
    blahTemp2=mysqlRead(cursor, 'prevown', 'hostname', hostname)
    for i in blahTemp2:
        blahTemp.append(i)
    blahMain.append(blahTemp)
    blahTemp=[]
    
    blahTemp.append(f'logs record for {hostname}:')
    blahTemp2=mysqlRead(cursor, 'logs', 'hostname', hostname)
    for i in blahTemp2:
        blahTemp.append(i)
    blahMain.append(blahTemp)
    blahTemp=[]

    return blahMain

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

def searchUser(cursor, email):
    blahMain=[]
    blahTemp=mysqlRead(cursor, 'users', 'user', email)
    for i in blahTemp:
        blahMain.append(i)
    return blahMain

def addUser(cursor, email, department):
    try:
        cursor.execute(f'insert into users values(\'{email}\', \'{department}\')')
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)
    return True

def preDelUser(cursor, email):
    myString=[]
    myString.append(f'\nusers record for \'{email}\' before deletion:')
    myString2=mysqlSearch(cursor, 'users', 'user', email)
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

def postDelUser(cursor, email):
    myString=[]
    myString.append(f'\nusers record for \'{email}\' after deletion:')
    myString2=mysqlSearch(cursor, 'users', 'user', email)
    if myString2:
        for i in myString2:
            if i:
                myString.append(i)
    return myString

def getDetailsAddSystem():
    brand, model, serial, hostname, devtype, shipdate, warrexp, site, department=input('enter brand, model, serial, hostname, devtype, shipdate, warrexp, site, department seperated by comma:\n').split(',')
    return brand, model, serial, hostname, devtype, shipdate, warrexp, site, department

def preAddSystem(cursor, hostname):
    myString=[]
    myString.append(f'\nsystems record for \'{hostname}\' before insertion:')
    myString2=mysqlSearch(cursor, 'systems', 'hostname', hostname)
    if not myString2:
        return None
    for i in myString2:
        myString.append(i)
    return myString

def addSystem(cursor, brand, model, serial, hostname, devtype, shipdate, warrexp, site, department):
    try:
        cursor.execute(f'insert into systems (brand, model, serial, hostname, type, shipdate, warrexp, site, department) values("{brand}", "{model}", "{serial}", "{hostname}", "{devtype}", "{shipdate}", "{warrexp}", "{site}", "{department}")')
    except:
        return False
    return True

def postAddSystem(cursor, hostname):
    myString=[]
    myString.append(f'\nsystems record for \'{hostname}\' after insertion:')
    myString2=mysqlSearch(cursor, 'systems', 'hostname', hostname)
    if myString2:
        for i in myString2:
            myString.append(i)
    return myString

def getDetailsDelSystem():
    hostname=input('enter hostname to delete:\n')
    return hostname

def preDelSystem(cursor, hostname):
    myString=[]
    myString.append(f'\nsystems record for \'{hostname}\' before deletion:')
    myString2=mysqlSearch(cursor, 'systems', 'hostname', hostname)
    if myString2:
        for i in myString2:
            myString.append(i)
        return myString
    return None

def delSystem(cursor, hostname):
    try:
        cursor.execute(f'delete from systems where hostname=\'{hostname}\'')
    except:
        return False
    return True

def postDelSystem(cursor, hostname):
    myString=[]
    myString.append(f'\nsystems record for \'{hostname}\' after deletion:')
    myString2=mysqlSearch(cursor, 'systems', 'hostname', hostname)
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
    blah=[False]
    cursor.execute(f'select department from systems where hostname=\'{hostname}\' and status=\'pending_deployment\'')
    result=cursor.rowcount
    if result==0:
        conn.close()
        blah[0]=False
        blah.append(f'unable to issue \'{hostname}\'. either \'{hostname}\' not in database or has already been deployed')
        return blah
    contents=cursor.fetchall()
    deviceDepartment=contents[0][0].strip().lower()
    #double confirm hostname availability in case the status is reflected incorrectly as 'pending_deployment'in the systems table
    cursor.execute(f'select * from currown where hostname=\'{hostname}\'')
    result=cursor.rowcount
    if result!=0:
        contents=cursor.fetchall()
        blah[0]=False
        blah.append(f'unable to issue \'{hostname}\'. \'{hostname}\' already been deployed')
        for i in contents:
            blah.append(i)
        connClose(conn, cursor)
        return blah
    #double confirm hostname availability in case the status is reflected incorrectly as 'pending_deployment'in the systems table
    cursor.execute(f'select * from users where user=\'{email}\'')
    result=cursor.rowcount
    if result==0:
        blah[0]=False
        blah.append(f'unable to issue \'{hostname}\'. user \'{email}\' not found in database')
        connClose(conn, cursor)
        return False
    else:
        contents=cursor.fetchall()
        userDepartment=contents[0][1].strip().lower()
    if userDepartment==deviceDepartment:
        connClose(conn, cursor)
        blah[0]=True
        return blah
    else:
        connClose(conn, cursor)
        blah[0]=False
        blah.append(f'unable to issue \'{hostname}\'. dapartment for \'{email}\' and \'{hostname}\' are different')
        return blah

def preDeviceIssueStatus(cursor, hostname):
    mainList=[]
    subList1=[]
    subList2=[]
    subList1.append(f'systems record before issue:')
    systemsString=mysqlSearch(cursor, 'systems', 'hostname', hostname)
    for i in systemsString:
        subList1.append(i)
    mainList.append(subList1)
    subList2.append(f'current owner record before issue:')
    currownString=mysqlSearch(cursor, 'currown', 'hostname', hostname)
    if currownString:
        for i in currownString:
            subList2.append(i)
    mainList.append(subList2)  
    return mainList


def deviceIssue(cursor, hostname, email, date):
    try:
        cursor.execute(f'insert into currown values(\'{date}\', \'{hostname}\', \'{email}\')')
        cursor.execute(f'update systems set site=null, status=\'deployed\' where hostname=\'{hostname}\'')
    except:
        return False
    return True

def postDeviceIssueStatus(cursor, hostname):
    mainList=[]
    subList1=[]
    subList2=[]
    subList1.append(f'systems record after issue:')
    systemsString=mysqlSearch(cursor, 'systems', 'hostname', hostname)
    for i in systemsString:
        subList1.append(i)
    mainList.append(subList1)
    subList2.append(f'current owner record after issue:')
    currownString=mysqlSearch(cursor, 'currown', 'hostname', hostname)
    if currownString:
        for i in currownString:
            subList2.append(i)
    mainList.append(subList2)  
    return mainList

def deviceIssueConsolidation(cursor, hostname, email, date):
        blahFinal=[]
        blahFinal.append(False)
        blahFinal[0]=deviceIssueChecks(hostname, email)
        if blahFinal[0]:
            try:
                blahFinal.append(preDeviceIssueStatus(cursor, hostname))
                deviceIssue(cursor, hostname, email, date)
                blahFinal.append(postDeviceIssueStatus(cursor, hostname))
            except:
                blahFinal[0]=False
        return blahFinal

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

def preDeviceReturnStatus(cursor, hostname):
    mainList=[]
    subList1=[]
    subList2=[]
    subList3=[]
    subList1.append(f'systems record before return:')
    systemsString=mysqlSearch(cursor, 'systems', 'hostname', hostname)
    for i in systemsString:
        subList1.append(i)
    mainList.append(subList1)
    subList2.append(f'current owner record before return:')
    currownString=mysqlSearch(cursor, 'currown', 'hostname', hostname)
    if currownString:
        for i in currownString:
            subList2.append(i)
    mainList.append(subList2)
    subList3.append(f'previous owner record before return:')
    prevownString=mysqlSearch(cursor, 'prevown', 'hostname', hostname)
    if prevownString:
        for i in prevownString:
            subList3.append(i)
    mainList.append(subList3)
    return mainList

def deviceReturn(cursor, hostname, email, site, date):
    try:
        cursor.execute(f'insert into prevown select * from currown where hostname=\'{hostname}\' and user=\'{email}\'')
        cursor.execute(f'update prevown set date=\'{date}\' where hostname=\'{hostname}\' and user=\'{email}\'')
        cursor.execute(f'delete from currown where hostname=\'{hostname}\' and user=\'{email}\'')
        cursor.execute(f'update systems set site=\'{site}\', status=\'pending_deployment\' where hostname=\'{hostname}\'')
    except:
        return False
    return True

def postDeviceReturnStatus(cursor, hostname):
    mainList=[]
    subList1=[]
    subList2=[]
    subList3=[]
    subList1.append(f'systems record after return:')
    systemsString=mysqlSearch(cursor, 'systems', 'hostname', hostname)
    for i in systemsString:
        subList1.append(i)
    mainList.append(subList1)
    subList2.append(f'current owner record after return:')
    currownString=mysqlSearch(cursor, 'currown', 'hostname', hostname)
    if currownString:
        for i in currownString:
            subList2.append(i)
    mainList.append(subList2)
    subList3.append(f'previous owner record after return:')
    prevownString=mysqlSearch(cursor, 'prevown', 'hostname', hostname)
    if prevownString:
        for i in prevownString:
            subList3.append(i)
    mainList.append(subList3)
    return mainList

def deviceReturnConsolidation(cursor, hostname, email, site, date):
        blahFinal=[]
        blahFinal.append(False)
        blahFinal[0]=deviceReturnChecks(hostname, email)
        if blahFinal[0]:
            try:
                blahFinal.append(preDeviceReturnStatus(cursor, hostname))
                deviceReturn(cursor, hostname, email, site, date)
                blahFinal.append(postDeviceReturnStatus(cursor, hostname))
            except:
                blahFinal[0]=False
        return blahFinal

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
                conn, cursor=mysqlConn()
                hostname=getDetailsSearch()
                print()
                x=mysqlSearch(cursor, hostname)
                if x:
                    for i in x:
                        for j in i:
                            print(j)
                        print()
                        print()
                        print()
                else:
                    print(f'\'{hostname}\' not found in database')
                connClose(conn, cursor)
            case 'i':
                conn, cursor=mysqlConn()
                hostnameIssue, email, date=getDetailsIssue()
                blah=deviceIssueConsolidation(cursor, hostnameIssue, email, date)
                if blah:
                    conn.commit()
                    for i in blah:
                        print(i)
                connClose(conn, cursor)
            case 'r':
                conn, cursor=mysqlConn()
                hostnameReturn, email, site, date=getDetailsReturn()
                blah=deviceReturnConsolidation(cursor, hostnameReturn, email, site, date)
                if blah:
                    conn.commit()
                    for i in blah:
                        print(i)
                connClose(conn, cursor)
            case 's':
                conn, cursor=mysqlConn()
                hostnameReturn, hostnameIssue, email, site, date=getDetailsSwap()
                blah1=deviceReturnConsolidation(cursor, hostnameReturn, email, site, date)
                if blah1:
                    blah2=deviceIssueConsolidation(cursor, hostnameIssue, email, date)
                if blah2:
                    conn.commit()
                for i in blah1:
                    print(i)
                print()
                print()
                print()
                for i in blah2:
                    print(i)
                connClose(conn, cursor)

            case 'a':
                conn, cursor=mysqlConn()
                email, department=getDetailsAddDeleteUser()
                x=preAddUser(cursor, email)
                myString=[]
                myString.append(f'\nusers record for \'{email}\' after insertion:')
                myString2=mysqlSearch(cursor, 'users', 'user', email)
                if myString2:
                    for i in myString2:
                        myString.append(i)
                return myString
                if len(x)!=0:
                    dfsd
                else:
                    connClose(conn, cursor)
                    print(f'{email} already exists in database')

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
                conn, cursor=mysqlConn()
                x=preAddSystem(cursor, hostname)
                if not x:
                    addSystem(cursor, brand, model, serial, hostname, deviceType, shipdate, warrexp, site, department)
                    print()
                    print(x)
                    print()
                    print(postAddSystem(cursor, hostname))
                else:
                    print(f'{hostname} already exists in database: {x}')
                conn.commit()
                connClose(conn, cursor)
            case 'ds':
                hostname=getDetailsDelSystem()
                conn, cursor=mysqlConn()
                x=preDelSystem(cursor, hostname)
                if x:
                    print()
                    print(preDelSystem(cursor, hostname))
                    print()
                    delSystem(cursor, hostname)
                    print()
                    print(postDelSystem(cursor, hostname))
                    print()
                else:
                    print(f'{hostname} does not exist in database')
                conn.commit()
                connClose(conn, cursor)
            case 'l':
                date, hostname, user, remarks=getDetailsLogs()
                addLogs(date, hostname, user, remarks)
            case 'x':
                return table
            case _:
                print('wrong choice, only s, h, p, c or x allowed. ')