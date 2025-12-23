from flask import Flask
from flask import render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="AbhiJothi_143",
    database="bloodbank"
)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        blood_group = request.form['blood_group']
        phone = request.form['phone']
        location = request.form['location']

        cursor = db.cursor()
        query = """
        INSERT INTO donors (name, blood_group, phone, location, availability)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (name, blood_group, phone, location, "Yes")
        cursor.execute(query, values)
        db.commit()

        return "Donor Registered Successfully"

    return render_template('register.html')
@app.route('/donors/<blood_group>')
def donors(blood_group):
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT name, phone, location FROM donors WHERE blood_group = %s",
        (blood_group,)
    )
    donors = cursor.fetchall()
    return render_template(
        'donors.html',
        blood_group=blood_group,
        donors=donors
    )

if __name__ == "__main__":
    app.run(debug=True)