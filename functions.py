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

def mysqlRead2Params(cursor, table, column1, param1, column2, param2):
    query=f'SELECT * FROM {table} WHERE {column1}=%s and {column2}=%s'
    cursor.execute(query, (param1, param2))
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

def searchLog(cursor, hostname):
    blahMain=[]
    blahTemp=mysqlRead(cursor, 'logs', 'hostname', hostname)
    for i in blahTemp:
        blahMain.append(i)
    return blahMain

def addLog(cursor, date, hostname, user, remarks):
    try:
        cursor.execute(f'insert into logs(date, hostname, user, remarks) values("{date}", "{hostname}", "{user}", "{remarks}")')
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)
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

def delUser(cursor, email):
    try:
        cursor.execute(f'delete from users where user=\'{email}\'')
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)
    return True

def getDetailsAddDelSystem():
    brand, model, serial, hostname, devtype, shipdate, warrexp, site, department=input('enter brand, model, serial, hostname, devtype, shipdate, warrexp, site, department seperated by comma:\n').split(',')
    return brand, model, serial, hostname, devtype, shipdate, warrexp, site, department

def searchSystem(cursor, hostname):
    blahMain=[]
    blahTemp=mysqlRead(cursor, 'systems', 'hostname', hostname)
    for i in blahTemp:
        blahMain.append(i)
    return blahMain

def addSystem(cursor, brand, model, serial, hostname, devtype, shipdate, warrexp, site, department):
    try:
        cursor.execute(f'insert into systems (brand, model, serial, hostname, type, shipdate, warrexp, site, department) values("{brand}", "{model}", "{serial}", "{hostname}", "{devtype}", "{shipdate}", "{warrexp}", "{site}", "{department}")')
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)
    return True

def delSystem(cursor, hostname):
    try:
        cursor.execute(f'delete from systems where hostname=\'{hostname}\'')
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)
    return True

def searchReturnIssue(cursor, hostname, status):
    blahMain=[]
    blahTemp=mysqlRead2Params(cursor, 'systems', 'hostname', hostname, 'status', status)
    for i in blahTemp:
        blahMain.append(i)
    return blahMain

def getDetailsIssue():
    hostname=input('\nenter hostname of device to be issued to user: ').strip().lower()
    email=input('\nenter email address of user: ').strip().lower()
    date=input('\nenter date in this format: \'yyyy mmm dd\': ').strip().lower()
    return hostname, email, date

def deviceIssue(cursor, hostname, email, date):
    try:
        cursor.execute(f'insert into currown values(\'{date}\', \'{hostname}\', \'{email}\')')
        cursor.execute(f'update systems set site=null, status=\'deployed\' where hostname=\'{hostname}\'')
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)
    return True

def getDetailsReturn():
    hostname=input('\nenter hostname of device returned by user: ').strip().lower()
    email=input('\nenter email address of user: ').strip().lower()
    site=input('\nenter site to store returned device (eg. napier or toa payoh): ').strip().lower()
    date=input('\nenter date in this format: \'yyyy mmm dd\': ').strip().lower()
    return hostname, email, site, date

def deviceReturn(cursor, hostname, email, site, date):
    try:
        cursor.execute(f'delete from currown where hostname=\'{hostname}\'')
        cursor.execute(f'update systems set site=\'{site}\', status=\'pending_deployment\' where hostname=\'{hostname}\'')
        cursor.execute(f'insert into prevown values(\'{date}\', \'{hostname}\', \'{email}\')')
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)
    return True

def getDetailsSwap():
    hostnameReturn=input('\nenter hostname of device to returned by user: ').strip().lower()
    hostnameIssue=input('\nenter hostname of device to issue to user: ').strip().lower() 
    email=input('\nenter email address of user: ').strip().lower()
    site=input('\nenter site to store returned device (eg. napier or toa payoh): ').strip().lower()
    date=input('\nenter date in this format: \'yyyy mmm dd\': ').strip().lower()
    return hostnameReturn, hostnameIssue, email, site, date

def deviceSwap(cursor, hostnameReturn, hostnameIssue, email, site, date):
    x=False
    x=deviceReturn(cursor, hostnameReturn, email, site, date)
    if x==True:
        x=deviceIssue(cursor, hostnameIssue, email, date)
    return x

def searchDecom(cursor, hostname):
    blahMain=[]
    blahTemp=mysqlRead2Params(cursor, 'systems', 'hostname', hostname, 'status', 'pending_deployment')
    for i in blahTemp:
        blahMain.append(i)
    return blahMain

def decom(cursor, hostname, reason):
    try:
        cursor.execute(f'insert into decom select * from systems where hostname=\'{hostname}\'')
        cursor.execute(f'update decom set status=\'{reason}\'')
        cursor.execute(f'delete from systems where hostname=\'{hostname}\'')
        cursor.execute(f'delete from prevown where hostname=\'{hostname}\'')
        cursor.execute(f'delete from logs where hostname=\'{hostname}\'')
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)
    return True
