from flask  import Flask,jsonify,request
import json 
from flask_cors import CORS


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
   
@app.route('/authAdapter',methods =['Post'])
def authAdapter():
    try:
        data = request.get_json()

        fullname = data.get("full_name")
        email = data.get("e_mail")
        pword = data.get("p_word")

        if(fullname and email and pword and fullname != "" and email !="" and pword !="" and fullname != "NA" and email !="NA" and pword !="NA"):
            new = 0
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



if __name__== '__main__':
    app.run(host = "0.0.0.0", port = 5080 , debug = True)
