import os
#from forms import BillForm,RegistrationForm,LoginForm
from flask import Flask, render_template,redirect,url_for,request,session
from flask_wtf import FlaskForm,Form
from wtforms import StringField, PasswordField, DateTimeField,SubmitField,validators,TextField,IntegerField
from wtforms.validators import  Email, Length, DataRequired
from sqlalchemy import Column, Integer, String, Text, DateTime,ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import stripe

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)


app.config['SECRET_KEY'] = '36263f34f33f80bdd2571eb61f12332b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

######Stripe#########
public_key = "pk_test_mPiJ1KULgdnKKzKiowYNpDbe"
stripe.api_key = "sk_test_1eM3lfZ2EjrC0vANXd20wOAF"

db = SQLAlchemy(app)
Migrate(app,db)
#########################################################################################
################ DATABASE SECTION #######################################################
#########################################################################################
'''
class Bill(db.Model):
    __tablename__ = 'bills'
    id = db.Column(db.Integer,primary_key=True)
    fullname = db.Column(db.String(255),nullable=False)
    email = db.Column(db.String(255),nullable=False)
    address = db.Column(db.Text(),nullable=False)
    phone = db.Column(db.String(255),nullable=False)
    dob = db.Column(DateTime)
    xray = db.Column(db.Text())
    tablets = db.Column(db.Text())
    bandage = db.Column(db.Text())
    appoinments = db.Column(db.Text())

    def __init__(self,fullname,email,address,phone,dob,xray,tablets,bandage,appoinments):
        self.fullname = fullname
        self.address = address
        self.phone = phone
        self.dob = dob
        self.xray = xray
        self.tablets = tablets
        self.bandage = bandage
        self.appoinments = appoinments

    def __repr__(self):
        return '<Bills %r>' % self.fullname


class User(db.Model):
    #my choice for the table name
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    fullname = db.Column(db.String(20))
    email = db.Column(db.String(50))
    address = db.Column(db.String(100))
    phone = db.Column(db.String(20))

    password = db.Column(db.String(80))



    def __init__(self, fullname,email,address,phone,password):
       self.fullname = fullname
       self.email = email
       self.address = address
       self.phone = phone
       self.password = password


    def __repr__(self):
        return '<User %r>' % self.email

################################VALIDATION######################################

class BillForm(FlaskForm):
    fullname = StringField('FullName',validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    address = StringField('Address',validators=[DataRequired(),Length(min=3,max=30)])
    phone = IntegerField('PhoneNumber')
    dob = DateTimeField('DOB')
    xray = TextField('Xray')
    tablets = TextField('Tablets')
    bandage = TextField('Bandage')
    appoinments = TextField('Appointments')
    submit = SubmitField('Save')



class RegistrationForm(FlaskForm):
    fullname = StringField('FullName',validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    address = StringField('Address',validators=[DataRequired(),Length(min=3,max=30)])
    phone = StringField('PhoneNumber',validators=[DataRequired(),Length(min=10, max=13)])

    password = PasswordField('Password',
        validators=[DataRequired()
    ])

    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Submit')


########################VIEW FUNCTION###########################################
'''
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/bill')
def bill():
    '''
    form = BillForm(request.form)
    #dob = datetime.strptime(request.form['dob'], '%Y-%m-%d')
    if request.method =='POST' and form.validate():

        new_bill = Bill(fullname = request.form['fullname'],
        email = request.form['email'],
        address = request.form['address'],
        phone = request.form['phone'] ,
        dob = request.form['dob'] ,
        xray = request.form['xray'],
        tablets = request.form['tablets'] ,
        bandage = request.form['bandage'],
        appoinments = request.form['appoinments'])

        db.session.add(new_bill)
        db.session.commit()

        return render_template('medicare',form=form)
    else:
        '''

    return render_template('bill.html')


@app.route('/medicare')
def medicare():

    fullname = request.args.get('fullname')
    email = request.args.get('email')
    address = request.args.get('address')
    phone = request.args.get('phone')
    dob = request.args.get('dob')

    return render_template('medicare.html',fullname=fullname,email=email,address=address,phone=phone,dob=dob)


    #result = Bill.query.all()
    #return render_template("medicare.html",result = result, public_key=public_key)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        session['password'] = form.password.data
        return redirect(url_for('home',form=form))
    return render_template('login.html',form=form)



@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        new_user = User(fullname = form.fullname.data,email = form.email.data,address=form.address.data,phone=form.phone.data,password=form.password.data)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login',form=form))
        #return '<h1>' + form.fullname.data + ' ' + form.email.data + form.address.data + form.phone.data +  form.password.data + '</h1>'
    return render_template('register.html',form=form)

@app.route('/payment',methods=['POST'])
def payment():
    #customer Info
    customer = stripe.Customer.create(email=request.form['stripeEmail'],source=request.form['stripeToken'])
    #payment info
    charge = stripe.Charge.create(customer=customer.id ,
                                   amount=2000 ,
                                   currency='USD',
                                   description='Pay your bills.' )
    return redirect(url_for('home'))




if __name__ == '__main__':
    app.run(debug=True)
