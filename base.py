from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        
        if existing_user_username:
            raise ValidationError(
                "That username is already taken. Please chooose a different one")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

@app.route('/login' , methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('dashboard'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/mayavateva')
def index():
    return render_template('index.html')

@app.route('/personal')
def personal():
    posts = Post.query.order_by(Post.id).all()
    return render_template('personal.html', posts=posts)

@app.route('/newpersonalpost', methods=['GET', 'POST'])
def new_personal_post():
    if request.method == 'POST':
        date = request.form['date']
        title = request.form['title']
        content = request.form['content']
        if date and title and content:
            new_post = Post(date=date, title=title, content=content)
            db.session.add(new_post)
            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('personal'))
        else:
            flash('Date, Title, and Content are required.', 'danger')
    return render_template('newpersonalpost.html')

@app.route('/editpersonalpost/<int:post_id>', methods=['GET', 'POST'])
def edit_personal_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.date = request.form['date']
        post.title = request.form['title']
        post.content = request.form['content']
        if post.date and post.title and post.content:
            db.session.commit()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('personal'))
        else:
            flash('Date, Title, and Content are required.', 'danger')
    return render_template('editpersonalpost.html', post=post)

@app.route('/deletepersonalpost/<int:post_id>', methods=['GET', 'POST'])
def delete_personal_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', 'success')
        return redirect(url_for('personal'))
    return render_template('deletepersonalpost.html', post=post)


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

@app.route('/edithomepost/<int:post_id>', methods=['GET', 'POST'])
def edit_home_post(post_id):
    post = Home.query.get_or_404(post_id)
    if request.method == 'POST':
        post.date = request.form['date']
        post.title = request.form['title']
        post.content = request.form['content']
        if post.date and post.title and post.content:
            db.session.commit()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Date, Title, and Content are required.', 'danger')
    return render_template('edithomepost.html', post=post)

@app.route('/deletehomepost/<int:post_id>', methods=['GET', 'POST'])
def delete_home_post(post_id):
    post = Home.query.get_or_404(post_id)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('deletehomepost.html', post=post)

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

@app.route('/editbeautypost/<int:post_id>', methods=['GET', 'POST'])
def edit_beauty_post(post_id):
    post = Beauty.query.get_or_404(post_id)
    if request.method == 'POST':
        post.date = request.form['date']
        post.title = request.form['title']
        post.content = request.form['content']
        if post.date and post.title and post.content:
            db.session.commit()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('beauty'))
        else:
            flash('Date, Title, and Content are required.', 'danger')
    return render_template('editbeautypost.html', post=post)

@app.route('/deletebeautypost/<int:post_id>', methods=['GET', 'POST'])
def delete_beauty_post(post_id):
    post = Beauty.query.get_or_404(post_id)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', 'success')
        return redirect(url_for('beauty'))
    return render_template('deletebeautypost.html', post=post)

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

@app.route('/editskincarepost/<int:post_id>', methods=['GET', 'POST'])
def edit_skincare_post(post_id):
    post = Skincare.query.get_or_404(post_id)
    if request.method == 'POST':
        post.date = request.form['date']
        post.title = request.form['title']
        post.content = request.form['content']
        if post.date and post.title and post.content:
            db.session.commit()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('skincare'))
        else:
            flash('Date, Title, and Content are required.', 'danger')
    return render_template('editpersonalpost.html', post=post)

@app.route('/deleteskincarepost/<int:post_id>', methods=['GET', 'POST'])
def delete_skincare_post(post_id):
    post = Skincare.query.get_or_404(post_id)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.comclmit()
        flash('Post deleted successfully!', 'success')
        return redirect(url_for('skincare'))
    return render_template('deleteskincarepost.html', post=post)

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

@app.route('/wellnesspost/<int:post_id>', methods=['GET', 'POST'])
def edit_wellness_post(post_id):
    post = Wellness.query.get_or_404(post_id)
    if request.method == 'POST':
        post.date = request.form['date']
        post.title = request.form['title']
        post.content = request.form['content']
        if post.date and post.title and post.content:
            db.session.commit()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('wellness'))
        else:
            flash('Date, Title, and Content are required.', 'danger')
    return render_template('editwellnesspost.html', post=post)

@app.route('/deletewellnesspost/<int:post_id>', methods=['GET', 'POST'])
def delete_wellness_post(post_id):
    post = Wellness.query.get_or_404(post_id)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', 'success')
        return redirect(url_for('wellness'))
    return render_template('deletewellnesspost.html', post=post)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)