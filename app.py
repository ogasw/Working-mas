from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import db, User, Trade
from forms import RegistrationForm, LoginForm, TradeForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    trades = Trade.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', trades=trades)

@app.route('/trade', methods=['GET', 'POST'])
@login_required
def trade():
    form = TradeForm()
    if form.validate_on_submit():
        trade = Trade(user_id=current_user.id, trade_type=form.trade_type.data, amount=form.amount.data)
        db.session.add(trade)
        db.session.commit()
        flash('Trade placed successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('trade.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
      
