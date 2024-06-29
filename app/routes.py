from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user

from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User, Stock


# @app.route('/')
# def home():
#     stocks = Stock.query.all()
#     return render_template('index.html', stocks=stocks)

# @app.route('/')
# def index():
#     try:
#         stocks = Stock.query.all()
#         return render_template('index.html', stocks=stocks)
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return f"An error occurred: {str(e)}", 500
@app.route('/')
def index():
    stocks = Stock.query.limit(20).all()  # 获取前20条股票数据
    return render_template('index.html', stocks=stocks)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # 更改为 index
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # 更改为 index
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))  # 更改为 index
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))  # 更改为 index

@app.route('/stock/<int:stock_code>')
def stock_detail(stock_code):
    # 查询数据库获取特定的股票
    stock = Stock.query.get_or_404(stock_code)  # 使用 get_or_404 确保股票存在
    return render_template('stock_detail.html', stock=stock)
