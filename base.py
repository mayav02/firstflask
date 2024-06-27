from flask import Flask, render_template
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)

