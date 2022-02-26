from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import data

app = Flask(__name__)
  
# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'myuser'
app.config['MYSQL_PASSWORD'] = 'mypass'
app.config['MYSQL_DB'] = 'opencuisine'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#init MYSQL
mysql = MySQL(app)


def GetArticles():

    cur = mysql.connection.cursor()

    #cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
    cur.execute("use opencuisine")
    cur.execute("Select * FROM sys.Tables")

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()

    # Close connection
    cur.close()

Articles = data.Articles()

#GetArticles()

@app.route('/')
def hello_world():
    
    return render_template('home.html')


@app.route('/recipes')
def recipes():

    return render_template('articles.html', articles = Articles)


@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)

class AddForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
         name = form.name.data

         #Create Cursor
         cur = mysql.connection.cursor()

         #cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
         cur.execute("INSERT INTO recipes(name) VALUES(%s)", (name))

         # Commit to DB
         mysql.connection.commit()

         # Close connection
         cur.close()

         flash('Recipe has been added', 'success')
         return redirect(url_for('recipes'))


    return render_template('add.html', form=form)


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
         cur.execute("INSERT INTO recipes(name) VALUES(%s)", [name])

         # Commit to DB
         mysql.connection.commit()

         # Close connection
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
        result = cur.execute("Select * FROM users WHERE username = %s", [username])

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


