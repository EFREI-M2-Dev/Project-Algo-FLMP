from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL()

def init_db(app):
    app.config['MYSQL_HOST'] = 'mysql'  
    app.config['MYSQL_USER'] = 'user'   
    app.config['MYSQL_PASSWORD'] = 'password'  
    app.config['MYSQL_DB'] = 'mydatabase'  
    app.config['MYSQL_PORT'] = 3306  
    mysql.init_app(app)

init_db(app)

if __name__ == "__main__":
    app.run(debug=True)
