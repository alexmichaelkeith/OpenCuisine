from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import mysql.connector
import data


app = Flask(__name__)
  
# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'myuser'
app.config['MYSQL_PASSWORD'] = 'mypass'
app.config['MYSQL_DB'] = 'OpenCuisine'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#init MYSQL
mysql = MySQL(app)
Articles = data.Articles()

@app.route('/')
def hello_world():
    
    return render_template('home.html')


@app.route('/recipes')
def recipes():

    return render_template('articles.html', articles = Articles)


@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)



class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
         name = form.name.data
         email = form.email.data
         username = form.username.data
         password = sha256_crypt.encrypt(str(form.password.data))

         #Create Cursor
         cur = mysql.connection.cursor()

         #cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
         cur.execute("INSERT INTO recipes(name) VALUES(%s)", (name))

         # Commit to DB
         mysql.connection.commit()

         # Close connection
         cur.close()

         flash('You are now registered and can login', 'success')
         return redirect(url_for('login'))


    return render_template('register.html', form=form)

# main driver function
if __name__ == '__main__':
  
    app.secret_key='secret_key123'
    app.run(port = 5000, host="0.0.0.0", debug=True)


