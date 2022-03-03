from asyncio.windows_events import NULL
from typing import List, Dict
from flask import Flask
import mysql.connector
import json
from passlib.hash import sha256_crypt


mydb = mysql.connector.connect(
    user='root',
    password='root',
    host='localhost',
    port='3306',
    database='opencuisine'
)



def favorite_colors():

    connection = mysql.connector.connect(**mydb)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM recipes')
    results = [{name: color} for (name, color) in cursor]
    connection.close()
    print(results)



def test():

    # Get Form Fields
    username = 'alex3'
    password_candidate = 'alexalex3'

    # Create cursor
    cur = mydb.cursor(dictionary=True)
    # Get user by username
    result = cur.execute("Select * FROM users WHERE username = 'alex'")
    print(result)

    if result is not NULL:
        # Get stored hash
        data = cur.fetchone()
        password = data['password']
        # Compare Passwords
        if sha256_crypt.verify(password_candidate, password):
            print('PASSWORD MATCHED')
        else: 
            print('PASSWORD NOT MATCHED')
    else:
        print('NO USER')
    # Close connection
    trash = cur.fetchall()
    cur.close()


        
if __name__ == '__main__':
  
    test()

