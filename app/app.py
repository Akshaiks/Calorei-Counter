from flask  import Flask,jsonify,request
import json 
from flask_cors import CORS
import mysql.connector
import random
import string
import os


app = Flask(__name__)
CORS(app)
    


@app.route('/root',methods =['GET'])
def root():
    return jsonify({
        "statusCode" :"SC0000",  
        "statusDesc" :"success",
        "name" : "akshai",
    })

#new user registration
   
@app.route('/authAdapter',methods =['POST'])
def authAdapter():
    try:
        data = request.get_json()

        fullname = data.get("full_name")
        email = data.get("e_mail")
        pword = data.get("p_word")

        if(fullname and email and pword and fullname != "" and email !="" and pword !="" and fullname != "NA" and email !="NA" and pword !="NA"):
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*)FROM customerdetails WHERE E_mail = %s",[email])
            row=cursor.fetchone()
            connection.close()

            if row and row[0] > 0:
                 return jsonify({
                             "statusDesc": "Failure",
                             "statusCode": {
        	                 "code": "F005"
                            	},
	                         "message": "user already exist"                       
                             }),400
            else:
                business_id = generate_business_id(email)
                status=1

                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute("INSERT INTO customerdetails (Full_name,E_mail,Password,Bussiness_id,Status) VALUES (%s,%s,%s,%s,%s)",[fullname,email,pword,business_id,status])
                connection.commit()
                connection.close()
                return jsonify({
                            "statusDesc": "success",
                            "statusCode":{
                                "code":"SC0000"
                               },
                            "message":"new user created successfull",
                            "param":{
                                "business_id":business_id,
                                "status":status
                            }
                        })
        else:
            return jsonify({
                             "statusDesc": "Failure",
                             "statusCode": {
        	                 "code": "F005"
                            	},
	                         "message": "some mandatory fields to be filled"                       
                             }),400
        




    except Exception as e:
        return jsonify({"error": str(e)}),500

db_config={
    'host':'localhost',
    'user':'root',
    'password':'',
    'database':'iproject'
}
def get_db_connection():
    return mysql.connector.connect(**db_config)

def generate_business_id(email):
    email_prefix = email.split('0')[0]
    random_number = ''.join(random.choices(string.digits,k=5))
    return f"{email_prefix}_{random_number}"

if __name__== '__main__':
    app.run(host = "0.0.0.0", port = 5080 , debug = True)
