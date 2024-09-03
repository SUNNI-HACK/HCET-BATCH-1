from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import mysql.connector
from database import db_config,JWT_SECRET_KEY

app = Flask(__name__)

# Configure the Flask app with a secret key for JWT
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY  # Change this to a secure random key

# Initialize JWT manager
jwt = JWTManager(app) 
def get_db_connection():
    return mysql.connector.connect(**db_config)

# @app.route('/register', methods=['POST'])
# def register():
#     data = request.json
#     username = data['username']
#     password = data['password']  # In a real app, hash the password before storing it

#     connection = get_db_connection()
#     cursor = connection.cursor()
    
#     try:
#         cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
#         connection.commit()
#         return jsonify(message="User registered successfully"), 201
#     except mysql.connector.Error as err:
#         return jsonify(message=f"Error: {err}"), 500
#     finally:
#         cursor.close()
#         connection.close()

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     username = data['username']
#     password = data['password']

#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)
    
#     cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
#     user = cursor.fetchone()
    
#     cursor.close()
#     connection.close()

#     if user:
#         access_token = create_access_token(identity={'username': username})
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify(message="Invalid credentials"), 401

# @app.route('/protected', methods=['GET'])
# @jwt_required()
# def protected():
#     current_user = get_jwt_identity()
#     a=1
#     return jsonify(logged_in_as=current_user), 200






@app.route("/branch",methods=["POST","GET"])
def branch():
    if request.method == "POST":
        try:
            data = request.json
            branch = data["name"]
            connection = get_db_connection()
            cursor = connection.cursor()
            record_exists = "select * from branch where name=%s;"
            cursor.execute(record_exists,[branch])
            is_exists=cursor.fetchone()

            if is_exists :
                cursor.close()
                connection.close()
                return jsonify ({"status_code":400 , "message":"record already exists"})
            else:
                Q = "insert into branch (name) values (%s);"
                cursor.execute(Q,[branch])
                connection.commit()
                cursor.close()
                connection.close()
                return jsonify({"status code":201,"message":"successfully insected"})
    
        except:
            return jsonify({"status_code":404,"message":"network error"})
        
    elif request.method == "GET":
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            show_users = "select * from branch ;"
            cursor.execute(show_users)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify({"status_code":200,"data":result})
        except:
            return jsonify({"status_code":404,"message":"exegution error"})
        
@app.route('/branch/<string:name>',methods=["POST","GET","DELECT"])
def branch():
    if request.method == "POST":
        try:
            connection = get_db_connection()
            request.args.get("name")
            data = request.json
            cursor = connection.cursor()
            query = "update branch set name = %s where id = %s;"
            cursor.execute(query,[data['name']])
            connection.commit()
            return jsonify({"status_code":200,"message":"updated successfully"})
        except:
            return jsonify({"status_code":404,"message":"exegution error"})
        
    elif request.method == "GET":
        try :
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            show_users = "select * from branch ;"
            cursor.execute(show_users)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify({"status_code":200,"data":result})
        except:
            return jsonify({"status_code":404,"message":"exegution error"})
        
    elif request.method == "DELECT":
        try :
            connection =get_db_connection()
            cursor = connection.cursor(dictionary=True)
            delect = "delect from branch where name = %s;"
            cursor.execute(delect,data['name'])
            cursor.close() 
            connection.commit()
            return jsonify({"status_code":200,"message":"delected sucessfully"})
        except :
            return jsonify({"status_code":404,"message":"exegution error"}) 
        
        
        
          


    
            





        

        
        
        






        
if __name__ == '__main__':
    app.run(debug=True)
