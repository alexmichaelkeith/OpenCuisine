from email.mime import image
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from pkg_resources import yield_lines
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import mysql.connector
from functools import wraps
import time

# Wait 15 seconds for mySQL to initialize when inside of Docker
#time.sleep(15)

mydb = mysql.connector.connect(
    user='root',
    password='root',
    host='localhost',
    port='3306',
    database='opencuisine'
)

app = Flask(__name__)

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

# Add Form Class
class AddForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    total_time = StringField('Total Time', [validators.Length(min=1, max=50)])
    yields = StringField('Yields', [validators.Length(min=1, max=50)])
    ingredients = StringField('Ingredients', [validators.Length(min=1, max=50)])
    instructions = StringField('Instructions', [validators.Length(min=1, max=50)])
    image = StringField('Image', [validators.Length(min=1, max=50)])
    host = StringField('Host', [validators.Length(min=1, max=50)])
    links = StringField('Links', [validators.Length(min=1, max=50)])
    nutrients = StringField('Nutrients', [validators.Length(min=1, max=50)])

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


def Recipes():
    cur = mydb.cursor(dictionary=True)
    sql = "SELECT * FROM recipes"
    cur.execute(sql)
    results = cur.fetchall()
    cur.close()
    return results


@app.route('/')
def home():
    return render_template('home.html')


# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursor
    cur = mydb.cursor(dictionary=True)

    # Get recipes
    #result = cur.execute("SELECT * FROM recipes")
    # Show recipes only from the user logged in 
    result = cur.execute("SELECT * FROM recipes")

    recipes = cur.fetchall()
    for recipe in recipes:
        print(recipe)
    #try:
    return render_template('dashboard.html', recipes=recipes)
      
    #except:
        #msg = 'No Recipes Found'
        #return render_template('dashboard.html', msg=msg)
    # Close connection
    cur.close()


@app.route('/recipes')
@is_logged_in
def recipes():
    return render_template('recipes.html', recipes = Recipes())


@app.route('/recipe/<string:title>/')
@is_logged_in
def recipe(title):
    return render_template('recipe.html', title=title)


@app.route('/add', methods=['GET', 'POST'])
@is_logged_in
def add():
    form = AddForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        total_time = form.total_time.data
        yields = form.yields.data
        ingredients = form.ingredients.data
        instructions = form.instructions.data
        image = form.image.data
        host = form.host.data
        links = form.links.data
        nutrients = form.nutrients.data

        # Create Cursor
        cur = mydb.cursor()

        # Execute
        cur.execute("INSERT INTO recipes(title, total_time, yields, ingredients, instructions, image, host, links, nutrients) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",(title, total_time, yields, ingredients, instructions, image, host, links, nutrients))

        # Commit to DB
        mydb.commit()

        #Close connection
        cur.close()

        flash('Recipe Created', 'success')

        return redirect(url_for('recipes'))

    return render_template('add.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
         name = form.name.data
         email = form.email.data
         username = form.username.data
         password = sha256_crypt.hash(str(form.password.data))

         cur = mydb.cursor(dictionary=True)
         sql = "INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)"
         val = (name, email, username, password)
         cur.execute(sql, val)
         mydb.commit()
         cur.close()

         flash('You are now registered and can login', 'success')
         return redirect(url_for('login'))


    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mydb.cursor(dictionary=True)
        # Get user by username
        result = cur.execute("Select * FROM users WHERE username = %s", [username])

        try:
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('recipes'))
            else: 
                error = 'Invalid Login'
                return render_template('login.html', error=error)
        except:
            error = 'Username not found'
            return render_template('login.html', error=error)

        trash = cur.fetchall() 
        cur.close()
    return render_template('login.html')


@app.route('/logout')
@is_logged_in
def logout():
    flash('You are now logged out', 'success')
    session.clear()
    return redirect(url_for('login'))



# Delete Recipe
@app.route('/delete/<string:id>', methods=['POST'])
@is_logged_in
def delete(id):
    # Create cursor
    cur = mydb.cursor()

    # Execute
    cur.execute("DELETE FROM articles WHERE id = %s", [id])

    # Commit to DB
    mydb.commit()

    #Close connection
    cur.close()

    flash('Recipe Deleted', 'success')

    return redirect(url_for('dashboard'))


# main driver function
if __name__ == '__main__':
  
    app.secret_key='secret_key123'
    app.run(port = 5000, host="0.0.0.0", debug=True)
