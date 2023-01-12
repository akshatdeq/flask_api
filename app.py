from flask import Flask, request, jsonify
import sqlalchemy
from models import db, Employee

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@127.0.0.1:5432/employee_management"
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@127.0.0.1:5432/employee_management"
db.init_app(app)


@app.before_first_request
def create_table():
    engine = sqlalchemy.create_engine("postgresql://postgres:postgres@127.0.0.1:5432")
    # engine = sqlalchemy.create_engine("postgresql://postgres:postgres@127.0.0.1:5432")
    conn = engine.connect()
    conn.execute("commit")
    conn.execute("create database employee_management;")
    conn.close()
    db.create_all()


# Home route / Landing route
@app.route('/')
@app.route('/employee')
def home():
    return 'Welcome to the Flask server!'


# Add an employee
@app.route('/employee/add', methods=['POST'])
def new_employee():
    data = request.get_json()
    employee_id = data["employee_id"]
    name = data['name']
    email = data['email']
    image_file = data['image_file']
    password = data['password']
    role = data['role']

    employee = Employee(employee_id, name, email, image_file, password, role)
    db.session.add(employee)
    db.session.commit()

    return jsonify({
        "success": True,
        "messgae": "Employee Added Successfully"
    })


# Get a specific employee
@app.route('/employee/<int:id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.filter_by(employee_id=id).first()
    if not employee:
        return jsonify({
            "success": False,
            "message": "Employee not found!"
        })

    result = {
            "employee_id": employee.employee_id,
            "name": employee.name,
            "email": employee.email,
            "image_file": employee.image_file,
            "password": employee.password,
            "role": employee.role,
        }
    return jsonify({
        "success": True,
        "employee": result
    })


# Get all employee
@app.route('/employee/all', methods=['GET'])
def get_employees():
    employees = Employee.query.all()

    results = []
    for employee in employees:
        temp = {
            "employee_id": employee.employee_id,
            "name": employee.name,
            "email": employee.email,
            "image_file": employee.image_file,
            "password": employee.password,
            "role": employee.role,
        }
        results.append(temp)

    return jsonify({
        "success": True,
        "employees": results,
    })


# Update an employee
@app.route('/employee/update/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    employee = Employee.query.filter_by(employee_id=employee_id).first()
    if not employee:
        return "Employee not found!"

    db.session.delete(employee)
    db.session.commit()
    data = request.get_json()
    name = data['name']
    email = data['email']
    image_file = data['image_file']
    password = data['password']
    role = data['role']
    db.session.add(Employee(employee_id=employee_id, name=name, email=email, image_file=image_file, password=password, role=role))
    db.session.commit()

    return jsonify({
        "success": True,
        "messgae": "Updated Sucessfully"
    })


# Delete an employee
@app.route('/employee/delete/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    employee = Employee.query.filter_by(employee_id=employee_id).first()
    if not employee:
        return "Employee not found!"

    db.session.delete(employee)
    db.session.commit()

    return jsonify({
        "success": True,
        "messgae": "Deleted Sucessfully"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
