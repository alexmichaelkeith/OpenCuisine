# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
#import mysql-connector
from flask import Flask, render_template
import mysql.connector
import time
# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
  
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.



@app.route('/')
def hello_world():
    
    return render_template('home.html')

  
@app.route('/recipes')
def recipes():

    return render_template('recipes.html')
# main driver function
if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(port = 5000, host="0.0.0.0", debug=True)
