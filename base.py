from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

# Define your models
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=db.func.current_timestamp())

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=db.func.current_timestamp())

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aboutme')
def about():
    return render_template('aboutme.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/beauty')
def beauty():
    return render_template('beauty.html')   

@app.route('/skincare')
def skincare():
    return render_template('skincare.html')

@app.route('/wellness')
def wellness():
    return render_template('wellness.html')

@app.route('/makeup')
def makeup():
    return render_template('makeup.html')

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if title and content:
            new_post = Post(title=title, content=content)
            db.session.add(new_post)
            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Title and Content are required.', 'danger')
    return render_template('new_post.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure this is called inside an application context
    app.run(debug=True)
