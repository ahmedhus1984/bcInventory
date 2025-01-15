import functions

def choiceSelectTables():
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
                conn, cursor=functions.mysqlConn()
                hostname=functions.getDetailsSearch()
                print()
                x=functions.mysqlSearch(cursor, hostname)
                if x:
                    for i in x:
                        for j in i:
                            print(j)
                        print()
                        print()
                        print()
                else:
                    print(f'\'{hostname}\' not found in database')
                functions.connClose(conn, cursor)
            case 'i':
                conn, cursor=functions.mysqlConn()
                hostnameIssue, email, date=functions.getDetailsIssue()
                blah=functions.deviceIssueConsolidation(cursor, hostnameIssue, email, date)
                if blah:
                    conn.commit()
                    for i in blah:
                        print(i)
                functions.connClose(conn, cursor)
            case 'r':
                conn, cursor=functions.mysqlConn()
                hostnameReturn, email, site, date=functions.getDetailsReturn()
                blah=functions.deviceReturnConsolidation(cursor, hostnameReturn, email, site, date)
                if blah:
                    conn.commit()
                    for i in blah:
                        print(i)
                functions.connClose(conn, cursor)
            case 's':
                conn, cursor=functions.mysqlConn()
                hostnameReturn, hostnameIssue, email, site, date=functions.getDetailsSwap()
                blah1=functions.deviceReturnConsolidation(cursor, hostnameReturn, email, site, date)
                if blah1:
                    blah2=functions.deviceIssueConsolidation(cursor, hostnameIssue, email, date)
                if blah2:
                    conn.commit()
                for i in blah1:
                    print(i)
                print()
                print()
                print()
                for i in blah2:
                    print(i)
                functions.connClose(conn, cursor)

            case 'a':
                conn, cursor=functions.mysqlConn()
                email, department=functions.getDetailsAddDeleteUser()
                x=functions.searchUser(cursor, email)
                myString=[]
                myString.append(f'\nusers record for \'{email}\' after insertion:')
                myString2=functions.mysqlSearch(cursor, 'users', 'user', email)
                if myString2:
                    for i in myString2:
                        myString.append(i)
                if len(myString)!=0:
                    print(myString)
                else:
                    functions.connClose(conn, cursor)
                    print(f'{email} already exists in database')

                print(functions.preAddUser(email))
                print()
                functions.addUser(email, department)
                print()
                print(functions.postAddUser(email))
                print()
            case 'd':
                email, department=functions.getDetailsAddDeleteUser()
                print()
                print(functions.preDelUser(email))
                print()
                functions.delUser(email, department)
                print()
                print(functions.postDelUser(email))
                print()
            case 'as':
                brand, model, serial, hostname, deviceType, shipdate, warrexp, site, department=functions.getDetailsAddSystem()
                conn, cursor=functions.mysqlConn()
                x=functions.preAddSystem(cursor, hostname)
                if not x:
                    functions.addSystem(cursor, brand, model, serial, hostname, deviceType, shipdate, warrexp, site, department)
                    print()
                    print(x)
                    print()
                    print(functions.postAddSystem(cursor, hostname))
                else:
                    print(f'{hostname} already exists in database: {x}')
                conn.commit()
                functions.connClose(conn, cursor)
            case 'ds':
                hostname=functions.getDetailsDelSystem()
                conn, cursor=functions.mysqlConn()
                x=functions.preDelSystem(cursor, hostname)
                if x:
                    print()
                    print(functions.preDelSystem(cursor, hostname))
                    print()
                    functions.delSystem(cursor, hostname)
                    print()
                    print(functions.postDelSystem(cursor, hostname))
                    print()
                else:
                    print(f'{hostname} does not exist in database')
                conn.commit()
                functions.connClose(conn, cursor)
            case 'l':
                date, hostname, user, remarks=functions.getDetailsLogs()
                functions.addLogs(date, hostname, user, remarks)
            case 'x':
                return table
            case _:
                print('wrong choice, only s, h, p, c or x allowed. ')