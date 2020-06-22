import mysql.connector
import json
from flask import render_template,jsonify
from mysql.connector import Error
from flask import Flask     
from flask import request
import pymysql
from flask_cors import CORS,cross_origin
from tictactoe import *

def connection():
  conn = pymysql.connect(host = "localhost",db='tictactoe',user='root',passwd='91847')
  c = conn.cursor()

  return c,conn

app = Flask(__name__) 
CORS(app,support_credentials=True)  # Flask constructor 
ALLOWED_EXTENSIONS=set(['txt'])
@cross_origin(support_credentials=True)
# A decorator used to tells the application 
# which URL is associated function 


@app.route('/index.html') 
def index():
  return render_template('index.html')


@app.route('/')       
def hello(): 
  return render_template('index.html')

@app.route('/com')       
def send_data(): 
  try:
    connection = mysql.connector.connect(host='localhost',
                             database='tictactoe',
                             user='root',
                             password='91847')
    if connection.is_connected():
           db_Info = connection.get_server_info()
           print("Connected to MySQL database... MySQL Server version on ",db_Info)
           cursor = connection.cursor()
           cursor.execute("select * from nmove;")
           record = cursor.fetchall()
           print ("You're connected")
           return jsonify(data=record)
  except Error as e :
    print ("Error while connecting to MySQL", e)
  finally:

    if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


@app.route('/com.html', methods=['GET', 'POST'])
def com():
  return render_template('com.html')

@app.route('/game.html', methods=['GET', 'POST'])
def game():
	return render_template('game.html')
    

@app.route('/expert.html', methods=['GET', 'POST'])
def expert():
  return render_template('expert.html')

@app.route('/expert', methods=['GET', 'POST'])
def expert_two():
  json_data=json.loads(request.data)
  x=json_data["key"]
  c,conn = connection()
  query = "insert into nmove(id,move) values(%s,%s)"
  args = (x[0],x[1])
  c.execute(query,args)
  conn.commit()
  conn.close()  
  return "sucess"

@app.route('/findbestmove', methods=['GET', 'POST'])
def background_process_test():
  json_data=json.loads(request.data)
  x=json_data["key"]
  move=findBestMove(x)
 
  print(move,"\nhi\n")
  return jsonify(data=move)


# @app.route('/background_process_test')
# def background_process_test():
#   print ("Hello")
#   return "nothing"

if __name__=='__main__': 
   app.run(debug=True) 