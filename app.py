from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from data import Articles
from flaskext.mysql import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = "b_5#y2LF4Q8z]/"

# Init MySQL
app.config['MYSQL_DATABASE_HOST']       = '127.0.0.1'
app.config['MYSQL_DATABASE_USER']       = 'root'
app.config['MYSQL_DATABASE_PASSWORD']   = 'root'
app.config['MYSQL_DATABASE_DB']         = 'myflask_app'

mysql = MySQL()
mysql.init_app(app)
# Init MySQL

Articles = Articles()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id = id)

# Register Form Class
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
        name        = form.name.data
        email       = form.email.data
        username    = form.username.data
        password    = sha256_crypt.encrypt(str(form.password.data))

        # Create Cursor
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user(name, email, username, password) VALUES (%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        conn.commit()

        # Close connection
        conn.close()

        flash("You are now registered and can login", 'success')
        return redirect(url_for('index'))

    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
