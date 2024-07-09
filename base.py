from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

# Define your models
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(150), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)

class Home(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(150), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
 
class Skincare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(150), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)

class Beauty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(150), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)

class Wellness(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(150), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/personal')
def about():
    posts = Post.query.order_by(Post.id).all()
    return render_template('personal.html', posts=posts)

@app.route('/newpersonalpost', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        date = request.form['date']
        title = request.form['title']
        content = request.form['content']
        if date and title and content:
            new_post = Post(date=date, title=title, content=content)
            db.session.add(new_post)
            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('about'))
        else:
            flash('Date, Title, and Content are required.', 'danger')
    return render_template('/newpersonalpost.html')

@app.route('/home')
def home():
    posts = Home.query.order_by(Home.id).all()
    return render_template('home.html', posts=posts)

@app.route('/newhomepost', methods=['GET', 'POST'])
def new_home_post():
    if request.method == 'POST':
        date = request.form['date']
        title = request.form['title']
        content = request.form['content']
        if date and title and content:
            new_home_post = Home(date=date, title=title, content=content)
            db.session.add(new_home_post)
            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Date, Title, and Content are required.', 'danger')
    return render_template('/newhomepost.html')

@app.route('/beauty')
def beauty():
    posts = Beauty.query.order_by(Beauty.id).all()
    return render_template('beauty.html', posts=posts)

@app.route('/newbeautypost', methods=['GET', 'POST'])
def new_beauty_post():
    if request.method == 'POST':
        date = request.form['date']
        title = request.form['title']
        content = request.form['content']
        if date and title and content:
            new_beauty_post = Beauty(date=date, title=title, content=content)
            db.session.add(new_beauty_post)
            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('beauty'))
        else:
            flash('Date, Title, and Content are required.', 'danger')
    return render_template('/newbeautypost.html')

@app.route('/skincare')
def skincare():
    posts = Skincare.query.order_by(Skincare.id).all()
    return render_template('skincare.html', posts=posts)

@app.route('/newskincarepost', methods=['GET', 'POST'])
def new_skincare_post():
    if request.method == 'POST':
        date = request.form['date']
        title = request.form['title']
        content = request.form['content']
        if date and title and content:
            new_skincare_post = Skincare(date=date, title=title, content=content)
            db.session.add(new_skincare_post)
            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('skincare'))
        else:
            flash('Date, Title, and Content are required.', 'danger')
    return render_template('/newskincarepost.html')

@app.route('/wellness')
def wellness():
    posts = Wellness.query.order_by(Wellness.id).all()
    return render_template('wellness.html', posts=posts)

@app.route('/newwellnesspost', methods=['GET', 'POST'])
def new_wellness_post():
    if request.method == 'POST':
        date = request.form['date']
        title = request.form['title']
        content = request.form['content']
        if date and title and content:
            new_wellness_post = Wellness(date=date, title=title, content=content)
            db.session.add(new_wellness_post)
            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('wellness'))
        else:
            flash('Date, Title, and Content are required.', 'danger')
    return render_template('/newwellnesspost.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)