from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import mysql.connector


mydb = mysql.connector.connect(
    user='root',
    password='root',
    host='localhost',
    port='3306',
    database='opencuisine'
)


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

class AddForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    color = StringField('Color', [validators.Length(min=1, max=50)])


def Recipes():
    cur = mydb.cursor(dictionary=True)
    sql = "SELECT * FROM recipes"
    cur.execute(sql)
    results = cur.fetchall()
    cur.close()
    return results


app = Flask(__name__)

@app.route('/')
def home():
    
    return render_template('home.html')


@app.route('/recipes')
def recipes():

    return render_template('recipes.html', recipes = Recipes())


@app.route('/recipe/<string:name>/')
def recipe(name):

    return render_template('recipe.html', name=name)


@app.route('/add', methods=['GET', 'POST'])
def add():
    
    form = AddForm(request.form)
    if request.method == 'POST' and form.validate():
         name = form.name.data
         color = form.color.data

         cur = mydb.cursor(dictionary=True)
         sql = "INSERT INTO recipes (name, color) VALUES (%s, %s)"
         val = (name, color)
         cur.execute(sql, val)
         mydb.commit()
         cur.close()

         flash('Recipe has been added', 'success')
         return redirect(url_for('recipes'))

    return render_template('add.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
         name = form.name.data
         email = form.email.data
         username = form.username.data
         password = sha256_crypt.encrypt(str(form.password.data))

         cur = mydb.cursor(dictionary=True)
         sql = "INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)"
         val = (name, email, username, password)
         cur.execute(sql, val)
         mydb.commit()
         cur.close()

         flash('You are now registered and can login', 'success')
         return redirect(url_for('login'))


    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POSR'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        cur = mydb.cursor(dictionary=True)
        results = cur.fetchall()
        result = cur.execute("Select * FROM users WHERE username = %s", [username])
        cur.close()
        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                app.logger.info('PASSWORD MATCHED')
            else: 
                app.logger.info('PASSWORD NOT MATCHED')
        else:
            app.logger.info('NO USER')

    return render_template('login.html')


# main driver function
if __name__ == '__main__':
  
    app.secret_key='secret_key123'
    app.run(port = 5000, host="0.0.0.0", debug=True)
