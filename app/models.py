import os

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class User(UserMixin, BaseModel):    
    __tablename__ = 'user'
    username = db.Column(db.String(15),unique=True)
    email=db.Column(db.String(50),unique=True)
    password_hash = db.Column(db.String(80))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class ExpenseType(BaseModel):
    __tablename__= 'expensetype'
    name = db.Column(db.String(50))
    expenses = db.relationship('Expense',backref='expensetype',lazy='dynamic')
    def __repr__(self):
        return '<Expense Type: {}>'.format(self.name)

class Expense(BaseModel):
    __tablename__ = 'expense'
    expensetype_id = db.Column(db.Integer,db.ForeignKey('expensetype.id'),nullable=False)
    price = db.Column(db.Float(precision=10,asdecimal=True),nullable=False)    
    units = db.Column(db.Integer,nullable=False)    
    note = db.Column(db.String(250))
    paid_date = db.Column(db.DateTime,nullable=False)    
    def unit_price(self):
        return price/units if units>0 else price
    def __repr__(self):
        return '<Expense: {} units of {} @ {} each>'.format(self.units, ExpenseType.query.get(self.expensetype_id).name, self.price)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))