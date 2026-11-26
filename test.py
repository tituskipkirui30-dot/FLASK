from flask import *

#initialize the application 
app = Flask(__name__)

#define your route/endpoint
@app.route("/api/home")

#define your function
def home():
    return "Welcome home"


#define your route/endpoint
@app.route("/api/services")
#define your function
def services():
    return "Welcome to our services"

#define your route/endpoint
@app.route("/api/about")
#define your function
def about():
    return "Welcome to about"

#define your route/endpoint
@app.route("/api/contact")
#define your function
def contact():
    return "Contact  our school"

#define your route/endpoint
@app.route("/api/doctors")
#define your function
def doctors():
    return "Meet our doctors"

#define your route/endpoint
@app.route("/api/patients")
#define your function
def patients():
    return "Welcome our patients"

#define your route/endpoint
@app.route("/api/menu")
#define your function
def menu():
    return "Here is our food menu"

#define your route/endpoint
@app.route("/api/orders")
#define your function
def orders():
    return "Place your food orders here"











#running the application
app.run(debug = True)