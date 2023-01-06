from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(30), nullable=False)

    def __init__(self, employee_id, name, email, image_file, password, role):
        self.employee_id = employee_id
        self.name = name
        self.email = email
        self.image_file = image_file
        self.password = password
        self.role = role

    def __repr__(self):
        return f"Student('{self.employee_id}', '{self.name}', '{self.email}', '{self.image_file}', {self.role})"
