from flask import Flask, render_template, request, flash,send_file ,jsonify
import jinja2
import json
import csv
from os import path


from dbconnection import InsertDb,ReadDb,DeleteDb,SearchDb




app = Flask(__name__)
#app.secret_key = "i m the best"

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