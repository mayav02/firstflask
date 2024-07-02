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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aboutme')
def about():
    posts = Post.query.order_by(Post.id).all()
    return render_template('aboutme.html', posts=posts)

@app.route('/newaboutmepost')
@app.route('/newaboutmepost', methods=['GET', 'POST'])
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
    return render_template('/newaboutmepost.html')

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

if __name__ == '__main__':
    app.run(debug=True)