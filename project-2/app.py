from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Config SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Feedback model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Create the database and tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/feedback')
def feedback_form():
    return render_template('feedback.html')

@app.route('/submit', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    feedback = Feedback(name=name, email=email, message=message)
    db.session.add(feedback)
    db.session.commit()

    return redirect(url_for('all_feedback'))

@app.route('/all-feedback')
def all_feedback():
    all_feedbacks = Feedback.query.all()
    return render_template('all_feedback.html', feedbacks=all_feedbacks)

if __name__ == '__main__':
    app.run(debug=True)

