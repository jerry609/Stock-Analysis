from datetime import datetime

from flask_login import UserMixin

from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    transactions = db.relationship('Transaction', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Stock(db.Model):
    __tablename__ = 'stock_data'

    stock_code = db.Column(db.BigInteger, primary_key=True)
    change_amount = db.Column(db.Text)
    change_rate = db.Column(db.Text)
    current_price = db.Column(db.Float)
    price_limit_up = db.Column(db.Text)
    price_limit_down = db.Column(db.Text)
    open_price = db.Column(db.Text)
    highest_price = db.Column(db.Text)
    lowest_price = db.Column(db.Text)
    previous_close = db.Column(db.Text)
    volume = db.Column(db.Text)
    turnover = db.Column(db.Text)
    amplitude = db.Column(db.Text)
    turnover_rate = db.Column(db.Text)
    pb_ratio = db.Column(db.Text)
    pe_ratio = db.Column(db.Float)
    market_cap = db.Column(db.Text)
    circulating_market_cap = db.Column(db.Text)
    total_shares = db.Column(db.Text)
    circulating_shares = db.Column(db.Text)

    def __repr__(self):
        return f'<Stock {self.stock_code}>'


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stock_id = db.Column(db.BigInteger, db.ForeignKey('stock_data.stock_code'), nullable=False)  # 修改这里
    transaction_type = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    stock = db.relationship('Stock', backref='transactions')  # 添加这行来建立关系

    def __repr__(self):
        return f'<Transaction {self.transaction_type} {self.quantity}@{self.price}>'
