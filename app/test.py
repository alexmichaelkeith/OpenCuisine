from typing import List, Dict
from flask import Flask
import mysql.connector
import json


def favorite_colors():
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'port': '3306',
        'database': 'opencuisine'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM recipes')
    results = [{name: color} for (name, color) in cursor]
    connection.close()
    print(results)




        
if __name__ == '__main__':
  
    favorite_colors()

