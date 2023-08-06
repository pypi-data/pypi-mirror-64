import mysql.connector
from mysql.connector import Error
from csv import reader

key = ['id','UserId', 'ScannedFiles', 'RiskFiles', 'ScanStatus', 'Time', 'Date', 'Filename', 'IsValid']

def get_list_of_dict(keys, list_of_tuples):
     """
     This function will accept keys and list_of_tuples as args and return list of dicts
     """
     list_of_dict = [dict(zip(keys, values)) for values in list_of_tuples]
     return list_of_dict






def InsertDb(path):

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='scan',
                                             user='root',
                                             password='root')
        if connection.is_connected():
            print("@lpha to user :DB Connection succesfull")
            print("@lpha to user :Executing Querries")
            # db_Info = connection.get_server_info()
            # print("Connected to MySQL Server version ", db_Info)
            # cursor = connection.cursor()
            # cursor.execute("select database();")
            # record = cursor.fetchone()
            # print("You're connected to database: ", record)
            with open(path, 'r') as read_obj:
                csv_reader = reader(read_obj)

                list_of_values = list(map(tuple, csv_reader))
                list_of_values = list_of_values[1:]
                # print(list_of_values)
            mySql_insert_query = """INSERT INTO ScannedFiles (AccId,ScannedFiles,RiskFiles,ScanStatus,ScanTime,ScanDate,Filename,IsValid)VALUES (%s,%s,%s,%s,%s,STR_TO_DATE(%s,'%d-%m-%y'),%s,%s) """
            cursor = connection.cursor()
            cursor.executemany(mySql_insert_query, list_of_values)
            connection.commit()
            print("@lpha to user :",cursor.rowcount,"Record inserted successfully into Laptop table")
                

    except Error as e:
        print("@lpha to user :Error while connecting to MySQL", e)
        
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("@lpha to user :MySQL connection is closed")



def ReadDb():
    try:
        print("@lpha to user :DB Connection succesfull")
        print("@lpha to user :Executing Querries")
        connection = mysql.connector.connect(host='localhost',
                                             database='scan',
                                             user='root',
                                             password='root')
        if connection.is_connected():
            sql_select_Query = "select * from scannedfiles"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
            # print(records)
            global key
            records_dict = get_list_of_dict(key, records)


                

    except Error as e:
        print("Error while connecting to MySQL", e)
        return None
        
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("@lpha to user :MySQL connection is closed") 
            return records_dict   


def DeleteDb():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='scan',
                                             user='root',
                                             password='root')
        if connection.is_connected():
            print("@lpha to user :DB Connection succesfull")
            print("@lpha to user :Executing Querries")
            sql_select_Query1 = "DELETE FROM scannedfiles"
            sql_select_Query2 = "ALTER TABLE scannedfiles AUTO_INCREMENT = 1;"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query1)
            print("@lpha to user :",cursor.rowcount,"Records deleted successfully")
            cursor.execute(sql_select_Query2)
            print("@lpha to user : Index reset completed")


                

    except Error as e:
        print("Error while connecting to MySQL", e)
        
        
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("@lpha to user :MySQL connection is closed") 



def SearchDb(fileName,date,scanStatus,isValid):
    list_fields = []
    list_values = []
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='scan',
                                             user='root',
                                             password='root')
        
        if connection.is_connected():
            print("@lpha to user :DB Connection succesfull")
            print("@lpha to user :Executing Querries")
            if(fileName):
                print('wewe')
                list_fields.append("Filename")
                list_values.append(fileName)


            if(date): 
                list_fields.append("ScanDate")
                list_values.append(date)



            if(scanStatus): 
                list_fields.append("ScanStatus")
                list_values.append(scanStatus)


            if(isValid):
                list_fields.append("IsValid")
                list_values.append(isValid) 

   
            list_values_tuples = tuple(list_values)
            # print(list_values_tuples)    


             
            sql_select_Query = "SELECT * FROM scannedfiles"
            for i in range(len(list_fields)):
                if(i==0):
                    sql_select_Query = sql_select_Query+" WHERE "+list_fields[i]+" = ? "
                else:
                    sql_select_Query = sql_select_Query+"AND "+list_fields[i]+" = ? "
                    
                  
            
            
            print("@lpha to user : Generated querry ---> "+sql_select_Query)        

            cursor = connection.cursor(prepared = True)
            cursor.execute(sql_select_Query,list_values_tuples)
            records = cursor.fetchall()
            # print(records)
            print("@lpha to user :",cursor.rowcount,"Matching Records fetched successfully")
            # records = cursor.fetchall()
            records_dict = {}
            global key
            records_dict = get_list_of_dict(key, records)


                

    except Error as e:
        print("Error while connecting to MySQL", e)
        return None
        
        
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("@lpha to user :MySQL connection is closed") 
            return records_dict