from flask import *
import pymysql

#initialize the application
app = Flask(__name__)

#define connection to database
connection = pymysql.connect(host="mysql-titusmodcom.alwaysdata.net", user="titusmodcom", password="modcom2026", database="titusmodcom_mary")

#define your cursor
cursor = connection.cursor(pymysql.cursors.DictCursor)

#define your route/endpoint
@app.route("/api/signup" ,methods=["POST"])
#define your function
def  signup():
    #get user inputs coming from the form
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    phone = request.form["phone"]

    #define sql to insert users
    sql = "insert into users(username, password, email, phone) values (%s, %s, %s, %s)"

    #define your data
    data = (username, password, email, phone)

    #execute/run query
    cursor.execute(sql, data)

    #connit/save change
    connection.commit()

    #return response to user
    return jsonify({"message": "user saved successful"})





#members signin/login
#define the route/endpoint
@app.route("/api/signin" ,methods=["POST"])

#define the function
def sigin():


    #get the user inputs from the form
    email = request.form["email"]
    password = request.form["password"]

    #define the sql to retrieve the users
    sql = "select * from users where email =%s and password = %s"

    #define our data
    data = (email,password)

    #excute/run query 
    cursor.execute(sql,data)

    if cursor.rowcount == 1 :
        #fetch user information
        userinfo = cursor.fetchone()
        return jsonify({

            "message" : "login sucess" ,
            "user" : userinfo
        })
    
    else:
        return jsonify({

            "message" : "login failed"
        })


#define your route/endpoint
@app.route("/api/addproduct" ,methods = ["POST"])

#define your function
def addproduct():
    

    #GET products inputs coming from the form
    product_name = request.form["product_name"]
    product_decription = request.form["product_description"]
    product_cost = request.form["product_cost"]
    product_photo = request.files["product_photo"]

    #define sql
    sql = "insert into product_details(product_name,product_description,product_cost,product_photo) values (%s,%s,%s,%s)"

    #define your data
    data = (product_name,product_decription,product_cost,product_photo)

    #execute/run query
    cursor.execute(sql,data)

    #commit/save changes
    connection.commit()

    #return response to user
    return jsonify({
        "message" : "product added successfully"
    })

#define the route/endpoint
@app.route("/getproducts" ,methods = ["GET"])

#define the function
def getproducts():

    #define sql to select products
    sql = "select * from product_details"

    #execute/run the query
    cursor.execute(sql)

    #fetch all the products
    allproducts = cursor.fetchall()
    return jsonify(allproducts)



# Mpesa Payment Route 
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

@app.route('/api/mpesa_payment', methods=['POST'])
def mpesa_payment():
        if request.method == 'POST':
            # Extract POST Values sent
            amount = request.form['amount']
            phone = request.form['phone']

            # Provide consumer_key and consumer_secret provided by safaricom
            consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
            consumer_secret = "amFbAoUByPV2rM5A"

            # Authenticate Yourself using above credentials to Safaricom Services, and Bearer Token this is used by safaricom for security identification purposes - Your are given Access
            api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
            # Provide your consumer_key and consumer_secret 
            response = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
            # Get response as Dictionary
            data = response.json()
            # Retrieve the Provide Token
            # Token allows you to proceed with the transaction
            access_token = "Bearer" + ' ' + data['access_token']

            #  GETTING THE PASSWORD
            timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')  # Current Time
            passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'  # Passkey(Safaricom Provided)
            business_short_code = "174379"  # Test Paybile (Safaricom Provided)
            # Combine above 3 Strings to get data variable
            data = business_short_code + passkey + timestamp
            # Encode to Base64
            encoded = base64.b64encode(data.encode())
            password = encoded.decode()

            # BODY OR PAYLOAD
            payload = {
                "BusinessShortCode": "174379",
                "Password":password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,  # use 1 when testing
                "PartyA": phone,  # change to your number
                "PartyB": "174379",
                "PhoneNumber": phone,
                "CallBackURL": "https://coding.co.ke/api/confirm.php",
                "AccountReference": "SokoGarden Online",
                "TransactionDesc": "Payments for Products"
            }

            # POPULAING THE HTTP HEADER, PROVIDE THE TOKEN ISSUED EARLIER
            headers = {
                "Authorization": access_token,
                "Content-Type": "application/json"
            }

            # Specify STK Push  Trigger URL
            url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  
            # Create a POST Request to above url, providing headers, payload 
            # Below triggers an STK Push to the phone number indicated in the payload and the amount.
            response = requests.post(url, json=payload, headers=headers)
            print(response.text) # 
            # Give a Response
            return jsonify({"message": "An MPESA Prompt has been sent to Your Phone, Please Check & Complete Payment"})













































#run the application
app.run(debug=True)