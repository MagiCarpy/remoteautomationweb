from flask import Flask, render_template, request, redirect, url_for, session
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from datetime import timedelta

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
app.permanent_session_lifetime = timedelta(minutes=5) # keeps session active for 5 minutes

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretKeyTest'

# API -------------------------------------- #
api = Api(app) 
'''
https://www.youtube.com/watch?v=GMppyAPbLYk
https://www.youtube.com/watch?v=K60ACu4j2Kw
'''

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deviceName = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(10), nullable=False)

class devices(Resource):
    def get(self):
        devicesJSON = [
          {
            "id": Devices.query.get(1).id, 
            "deviceName": Devices.query.get(1).deviceName, 
            "status": Devices.query.get(1).status
          },
          {
            "id": Devices.query.get(2).id, 
            "deviceName": Devices.query.get(2).deviceName, 
            "status": Devices.query.get(2).status
          }
        ]
        return devicesJSON
api.add_resource(devices, "/devices") # how to access helloworld

# make a function for more readability later?

# API -------------------------------------- #

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), 
    Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    password = StringField(validators=[InputRequired(), 
    Length(min=4, max=20)], render_kw={"placeholder":"Password"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists.")
        
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), 
    Length(min=4, max=20)], render_kw={"placeholder":"Username"})

    password = PasswordField(validators=[InputRequired(), 
    Length(min=4, max=20)], render_kw={"placeholder":"Password"})

    submit = SubmitField("Login")
        

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        if int(Devices.query.get(1).status) == 0:
            Devices.query.get(1).status = '1'
            db.session.commit()
        elif int(Devices.query.get(1).status) == 1:
            Devices.query.get(1).status = '0'
            db.session.commit()
    return render_template("index.html")
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                session['username'] = request.form['username']
                print(session['username'])
                login_user(user)
                return redirect(url_for("index"))

    return render_template('login.html', form=form)

@app.route("/logout", methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

def addAuthorizedUser(user, passwd):
    hashed_password = bcrypt.generate_password_hash(passwd)
    new_user = User(username=user, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

#addAuthorizedUser('admin1', 'password1')

if __name__ == "__main__":
    app.run(debug=True)
    