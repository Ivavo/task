from database import db

from flask_security import RoleMixin, UserMixin


roles_users = db.Table('roles_users', db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                                     db.Column('role_id', db.Integer, db.ForeignKey('role.id')))


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    description = db.Column(db.Text)

    address = db.relationship('DeliveryAddress', backref='product')
    params = db.relationship('ProductParams', backref='products')


class ProductParams(db.Model):
    __tablename__ = 'product_params'
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Integer)
    color = db.Column(db.String(64))
    price = db.Column(db.Integer)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))


class DeliveryAddress(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    street = db.Column(db.String(100))

    products_id = db.Column(db.Integer, db.ForeignKey('product.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(12))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref='users', lazy='dynamic')


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)