import flask
DB_HOST = "ec2-184-73-198-174.compute-1.amazonaws.com"
DB_NAME = "d778unuru7gl7t"
DB_USER = "zkuqfpwfurgbxe"
DB_PASS = "dc2b34408de61a5baab4805577fcff6b49301b27d376887f10bc4ca643e4e669"
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import psycopg2
import psycopg2.extras
import json
from flask import Flask, redirect, url_for, request, jsonify
app = Flask(__name__)

@app.route('/')
def success():    
    return flask.render_template("index.html",token="hello")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      with open(f.filename) as json_data:
        # use load() rather than loads() for JSON files
        record_list = json.load(json_data)
      conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
      print("connected")
      cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
      #cur.execute("CREATE TABLE student (id SERIAL PRIMARY KEY, userId VARCHAR, title VARCHAR, body VARCHAR);")
      for i in record_list:
        cur.execute("INSERT INTO student (userId, title, body) VALUES(%s, %s, %s)", (i['userId'], i['title'], i['body']))
      conn.commit()
      cur.execute("SELECT * FROM student;")

      result_list = cur.fetchall()      #return sql result
      print("fetch result-->",type(result_list))  #is s list type, need to be a dict

      fields_list = cur.description   # sql key name
      print("fields result -->",type(fields_list))
        #print("header--->",fields)
      column_list = []
      for i in fields_list:
        column_list.append(i[0])
      print("print final colume_list",column_list)

      jsonData_list = []
      for row in result_list:
        data_dict = {}
        for i in range(len(column_list)):
            data_dict[column_list[i]] = row[i]
        jsonData_list.append(data_dict)

      #s = cur.fetchall()
      cur.close()
      conn.close()
      return jsonify({'space': jsonData_list})

if __name__ == '__main__':
   app.run(debug = True)
