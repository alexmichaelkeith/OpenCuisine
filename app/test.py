import mysql.connector

def test():
    connection = mysql.connector.connect(host='localhost',database='opencuisine', user = 'root', password = 'root', port=3306)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        #print("Failed")
        
if __name__ == '__main__':
  
    test()
