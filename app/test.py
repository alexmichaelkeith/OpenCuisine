from typing import List, Dict
from flask import Flask
import mysql.connector
import json

recipesDB = mysql.connector.connect(
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

    cur = recipesDB.cursor()
    sql = "SELECT * FROM recipes"
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    for x in result:
        print(x)


        
if __name__ == '__main__':
  
    test()

