import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  
            database='crud_app'
        )
        if connection.is_connected():
            print("✅ Connected to MySQL database")
        return connection
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None

def close_connection(connection, cursor=None):
    if cursor:
        cursor.close()
    if connection and connection.is_connected():
        connection.close()
        print("🔒 MySQL connection closed")
