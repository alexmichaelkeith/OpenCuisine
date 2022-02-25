# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
#import mysql-connector
from flask import Flask
import mysql.connector
import time
# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
  
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    #time.sleep(20)
    connection = mysql.connector.connect(host='localhost',database='OpenCuisine', user = 'root', password = 'root')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)


    return "Connected to MySQL Server version"

    #return 'Hello World'
  
# main driver function
if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(port = 8000, host="0.0.0.0")
