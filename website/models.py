from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin

class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    main_email = db.Column(db.String(150), unique=True, nullable=False)
    address = db.Column(db.String(800))
    city = db.Column(db.String(100))
    state = db.Column(db.String(5))
    zipcode = db.Column(db.Integer)
    billing_email = db.Column(db.String(150), nullable=False)
    billing_address = db.Column(db.String(800))
    billing_city = db.Column(db.String(100))
    billing_state = db.Column(db.String(5))
    billing_zipcode = db.Column(db.Integer)
    phone_number = db.Column(db.Integer)
    note = db.Column(db.String(10000))
    students = db.relationship("Student")
    credit_cards = db.relationship("Creditcard")
    payments = db.relationship("Payment")
    balance = db.Column(db.Numeric)
    archived = db.Column(db.String(10))

    def __repl__(self):
        return f"Parent {self.first_name} {self.last_name}"

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    main_email = db.Column(db.String(150), unique=True, nullable=False)
    phone_number = db.Column(db.Integer)
    note = db.Column(db.String(10000))
    parent_id = db.Column(db.Integer, db.ForeignKey("parent.id"), nullable=False)
    archived = db.Column(db.String(10))

    def __repl__(self):
        return f"Student {self.first_name} {self.last_name}"

class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    main_email = db.Column(db.String(150), unique=True, nullable=False)
    phone_number = db.Column(db.Integer)
    address = db.Column(db.String(800))
    city = db.Column(db.String(100))
    state = db.Column(db.String(5))
    zipcode = db.Column(db.Integer)
    note = db.Column(db.String(10000))
    is_admin = db.Column(db.String(10))
    wage_payments = db.relationship("Wagepayment")
    archived = db.Column(db.String(10))
    
    def __repl__(self):
        return f"Tutor {self.first_name} {self.last_name}"

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    start_time = db.Column(db.String(50), nullable=False)
    end_time = db.Column(db.String(50))
    duration = db.Column(db.Numeric(scale=2), nullable=False)
    note = db.Column(db.String(10000))
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey("tutor.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    hourly_rate = db.Column(db.Numeric(scale=2), nullable=False)
    pay_rate = db.Column(db.Numeric(scale=2), nullable=False)
    address = db.Column(db.String(800))
    city = db.Column(db.String(100))
    state = db.Column(db.String(5))
    zipcode = db.Column(db.Integer)
    note = db.Column(db.String(10000))
    archived = db.Column(db.String(10))

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("parent.id"))
    type = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    amount = db.Column(db.Numeric(scale=2))
    cc_id = db.Column(db.Integer, db.ForeignKey("creditcard.id"))
    note = db.Column(db.String(500))

class Creditcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("parent.id"))
    type = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    cc_number = db.Column(db.Numeric)
    note = db.Column(db.String(500))
    

class Wagepayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey("tutor.id"))
    type = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    amount = db.Column(db.Numeric(scale=2))
    note = db.Column(db.String(500))    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))

