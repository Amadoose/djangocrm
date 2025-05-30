import mysql.connector

# Connect without specifying the database to create it if it doesn't exist
init_db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123456"
)

# Create a cursor to execute SQL commands
init_cursor = init_db.cursor()
init_cursor.execute("CREATE DATABASE IF NOT EXISTS dcrm_db")
init_db.close()

# Now connect to the newly created database
dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123456",
    database="dcrm_db",
)

cursorObject = dataBase.cursor()
def create_table():
    cursorObject.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))")
    dataBase.commit()
    print("Table created successfully.")
    # Call the create_table function to ensure the table is created when the script runs
    if __name__ == "__main__":
        create_table()
