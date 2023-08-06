from flask import Flask, render_template, request, flash,send_file ,jsonify
import jinja2
import json
import csv
from os import path
import mysql.connector
from mysql.connector import Error
from csv import reader

#from dbconnection import InsertDb,ReadDb,DeleteDb,SearchDb




app = Flask(__name__)
#app.secret_key = "i m the best"



######################################################################################



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


###########################################################################################################




@app.route("/")	
@app.route('/InputServlet', methods=['GET', 'POST'])
def process():
	Path = "xxx"

	fileName =  request.form.get('Filename')
	# print(fileName)
	date =  request.form.get('Date')
	# print(date)
	scanStatus =  request.form.get('ScanStatus')
	# print(scanStatus)
	isValid =  request.form.get('IsValid')
	# print(isValid)
	Path =  request.form.get('path')
	# print(Path)

	# movie_list = json.dumps(movielist)

	# if ((Path is not None)or(Path is not ""))
	if(Path):
		if (path.exists(Path)):
			InsertDb(Path)
		else :
			print('@alpha to user :Path doesnot exist')	

	
	movielist_tuple = SearchDb(fileName,date,scanStatus,isValid)
			
	# else:
	# 	movielist_tuple = ReadDb()
	
	
    
	# with open('data_1.csv') as f:
	#     reader = csv.reader(f, skipinitialspace=True)
	#     header = next(reader)
	#     movielist = [dict(zip(header, map(str, row))) for row in reader]

	# print(movielist)
	if request.method == 'POST':
		# print('post method triggered')		
		return jsonify(movielist_tuple)
		
	# return movie_list
	# print('get method triggered')
	return render_template('index.html')



@app.route('/scan', methods=['POST','GET'])
def scan():
	
	print('scan hitted')
	DeleteDb()
	return render_template('index.html')


	 





if __name__ == '__main__':
    app.run(debug=True)