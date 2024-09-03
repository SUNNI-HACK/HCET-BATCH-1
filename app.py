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






@app.route("/branch",methods=["PUT","GET"])
def branch():
    if request.method == "PUT":
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
        
@app.route('/branch/<int:id>',methods=["PUT","GET","DELETE"])
def branch_update(id):
    if request.method == "PUT":
        try:
            connection = get_db_connection()
            
            data = request.json
            cursor = connection.cursor()
            query = "update branch set name = %s where id = %s;"
            cursor.execute(query,[data['name'],id ])
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"status_code":200,"message":"updated successfully"})
        except:
            return jsonify({"status_code":404,"message":"exegution error"})
        
    elif request.method == "GET":
        try :
            connection = get_db_connection()
            data =request.json
            cursor = connection.cursor(dictionary=True)
            show_users = "select * from branch WHERE id =%s;"
            cursor.execute(show_users,[id])
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify({"status_code":200,"data":result})
        except:
            return jsonify({"status_code":404,"message":"exegution error"})
        
    elif request.method == "DELETE":
        try :
            connection =get_db_connection()
            data =request.json
            cursor = connection.cursor(dictionary=True)
            delete = "delete from branch where name = %s;"
            cursor.execute(delete,[data['name']])
            cursor.close() 
            connection.commit()
            return jsonify({"status_code":200,"message":"delected sucessfully"})
        except :
            return jsonify({"status_code":404,"message":"exegution error"})


@app.route("/cource",methods=["PUT","GET"])
def cource():
    if request.method == "PUT":
        try :
            data = request.json
            cource = data["name"]
            Connection = get_db_connection()
            cursor = Connection.cursor()
            record_exists = "select * from course where name =%s;"
            cursor.execute(record_exists,[cource])
            is_exists =cursor.fetchone()
            if is_exists :
                cursor.close()
                Connection.close()
                return jsonify({"status_code":400,"message":"record already existed"})
            else :
                Q = "insert into cource (name) values (%s);"
                cursor.execute(Q,[cource])
                Connection.commit()
                Connection.close()
                cursor.close()
                Connection.close()
                return jsonify({"status code":201,"message":"successfully insected"})
        except:
            return jsonify({"status_code":404,"message":"network error"}) 
        
    elif request.method == "GET":
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            show_users = "select * from cource ;"
            cursor.execute(show_users)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify({"status_code":200,"data":result})
        except:
            return jsonify({"status_code":404,"message":"exegution error"})
        

@app.route("/course/<int:id>",methods=["PUT","GET","DELETE"])  
def course_update(id):
    if request.method == "PUT":
        try:
            connection = get_db_connection()
            data = request.json
            cursor = connection.cursor()
            update = "update course set name = %s where id = %s;"
            cursor.execute(update,[data['name'],id])
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"status_code":200,"message":"updated sucessfully.."})
        except:
            return jsonify({"status_code":404,"message":"exegution error"})
        
    elif request.method == "GET":
        try:
            connection = get_db_connection()
            data = request.json
            cursor = connection.cursor(dictionary=True)
            show_all = "select * from course where name = %s;"
            cursor.execute(show_all,[data['name']])
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify({"status_code":200,"data":result})
        except:
            return jsonify({"status_code":404,"message":"exegution error.."})
        
    elif request.method == "DELETE":
        try:
            connection = get_db_connection()
            data = request.json
            cursor = connection.cursor()
            delete = "delete from course where id =%s;"
            cursor.execute(delete,[id])
            connection.commit()
            cursor.close()    
            connection.close()
            return jsonify ({"status_code":200,"message":"deleted successfully.."})
        except :
            return jsonify({"status0_code":404,"message":"exegution error.."})
        
@app.route("/sem",methods=["PUT","GET"])
def sem():
    if request.method == "PUT":
        try:
            data = request.json
            sem = data['name']
            connection = get_db_connection()
            cursor = connection.cursor()
            record_exits ="select * from sem where name = %s;"
            cursor.execute(record_exits,[sem])
            is_exists = cursor.fetchone()
            if is_exists :
                cursor.close()
                connection.close()
                return jsonify({"status_code":400,"message":"record already existed.."})
            else :
                insert_val = "insert into sem (name) values (%s);"
                cursor.execute(insert_val,[sem])
                connection.commit()
                cursor.close()
                connection.close()
                return jsonify({"status_code":200,"message":"inserted sucessfully.."})
        except:
            return jsonify({"status_code":404,"message":"exegution error.."})
        
    elif request .method == "GET":
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            show_all = "select * from sem;"
            cursor.execute(show_all)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify({"status_code":200,"data":result})
        except:
            return jsonify ({"status_code":404,"message":"exegution error.."})
        

@app.route("/sem/<int:id>",methods=["PUT","GET","DELETE"])
def sem_update(id):
    if request.method == "PUT":
        try :
            connection = get_db_connection()
            data = request.json
            cursor = connection.cursor()
            update = "update sem set name = %s where id = %s;"
            cursor.execute(update,[data['name'],id])
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"status_code":200,"message":"updated sucessfully.."})
        except:
            return jsonify({"status_code":404,"message":"exegution error"})
        
    elif request.method == "GET":
        try:
            connection = get_db_connection()
            data = request.json
            cursor = connection.cursor(dictionary=True)
            show_all = "select * from sem where name = %s;"
            cursor.execute(show_all,[data['name']])
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify({"status_code":200,"data":result})
        except:
            return jsonify({"status_code":404,"message":"exegution error.."})
        
    elif request.method == "DELETE":
        try:
            connection = get_db_connection()
            data = request.json
            cursor = connection.cursor()
            delete = "delete from sem where id =%s;"
            cursor.execute(delete,[id])
            connection.commit()
            cursor.close()    
            connection.close()
            return jsonify ({"status_code":200,"message":"deleted successfully.."})
        except :
            return jsonify({"status0_code":404,"message":"exegution error.."})
        


@app.route("/year",methods=["PUT","GET"])
def year():
    if request.method == "PUT":
        try:
            data = request.json
            year = data['name']
            connection = get_db_connection()
            cursor = connection.cursor()
            record_exits ="select * from year where name = %s;"
            cursor.execute(record_exits,[year])
            is_exists = cursor.fetchone()
            if is_exists :
                cursor.close()
                connection.close()
                return jsonify({"status_code":400,"message":"record already existed.."})
            else :
                insert_val = "insert into year (name) values (%s);"
                cursor.execute(insert_val,[year])
                connection.commit()
                cursor.close()
                connection.close()
                return jsonify({"status_code":200,"message":"inserted sucessfully.."})
        except:
            return jsonify({"status_code":404,"message":"exegution error.."})
        
    elif request .method == "GET":
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            show_all = "select * from year;"
            cursor.execute(show_all)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify({"status_code":200,"data":result})
        except:
            return jsonify ({"status_code":404,"message":"exegution error.."})
        

@app.route("/year/<int:id>",methods=["PUT","GET","DELETE"])
def year_update(id):
    if request.method == "PUT":
        try :
            connection = get_db_connection()
            data = request.json
            cursor = connection.cursor()
            update = "update year set name = %s where id = %s;"
            cursor.execute(update,[data['name'],id])
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"status_code":200,"message":"updated sucessfully.."})
        except:
            return jsonify({"status_code":404,"message":"exegution error"})
        
    elif request.method == "GET":
        try:
            connection = get_db_connection()
            data = request.json
            cursor = connection.cursor(dictionary=True)
            show_all = "select * from year where name = %s;"
            cursor.execute(show_all,[data['name']])
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify({"status_code":200,"data":result})
        except:
            return jsonify({"status_code":404,"message":"exegution error.."})
        
    elif request.method == "DELETE":
        try:
            connection = get_db_connection()
            data = request.json
            cursor = connection.cursor()
            delete = "delete from year where id =%s;"
            cursor.execute(delete,[id])
            connection.commit()
            cursor.close()    
            connection.close()
            return jsonify ({"status_code":200,"message":"deleted successfully.."})
        except :
            return jsonify({"status0_code":404,"message":"exegution error.."})
        

@app.route("/gender",methods=["PUT","GET"])
def gender():
    if request.method == "PUT":
        try:
            data = request.json
            gender = data['name']
            connection = get_db_connection()
            cursor = connection.cursor()
            record_exits ="select * from gender where name = %s;"
            cursor.execute(record_exits,[gender])
            is_exists = cursor.fetchone()
            if is_exists :
                cursor.close()
                connection.close()
                return jsonify({"status_code":400,"message":"record already existed.."})
            else :
                insert_val = "insert into gender (name) values (%s);"
                cursor.execute(insert_val,[gender])
                connection.commit()
                cursor.close()
                connection.close()
                return jsonify({"status_code":200,"message":"inserted sucessfully.."})
        except:
            return jsonify({"status_code":404,"message":"exegution error.."})
        
    elif request .method == "GET":
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            show_all = "select * from gender;"
            cursor.execute(show_all)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify({"status_code":200,"data":result})
        except:
            return jsonify ({"status_code":404,"message":"exegution error.."})
        
@app.route("/gender/<int:id>",methods=["PUT","GET","DELETE"])
def gender_update(id):
    if request.method == "PUT":
        try :
            connection = get_db_connection()
            data = request.json
            cursor = connection.cursor()
            update = "update gender set name = %s where id = %s;"
            cursor.execute(update,[data['name'],id])
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"status_code":200,"message":"updated sucessfully.."})
        except:
            return jsonify({"status_code":404,"message":"exegution error"})
        
    elif request.method == "GET":
        try:
            connection = get_db_connection()
            data = request.json
            cursor = connection.cursor(dictionary=True)
            show_all = "select * from gender where name = %s;"
            cursor.execute(show_all,[data['name']])
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify({"status_code":200,"data":result})
        except:
            return jsonify({"status_code":404,"message":"exegution error.."})
        
    elif request.method == "DELETE":
        try:
            connection = get_db_connection()
            data = request.json
            cursor = connection.cursor()
            delete = "delete from gender where id =%s;"
            cursor.execute(delete,[id])
            connection.commit()
            cursor.close()    
            connection.close()
            return jsonify ({"status_code":200,"message":"deleted successfully.."})
        except :
            return jsonify({"status0_code":404,"message":"exegution error.."})








        


        



    








               
            
    



        
        
        
          


    
            





        

        
        
        






        
if __name__ == '__main__':
    app.run(debug=True)
