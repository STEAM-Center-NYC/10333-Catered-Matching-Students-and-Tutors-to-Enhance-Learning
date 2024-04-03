from flask import Flask, render_template, request, redirect
import pymysql
import pymysql.cursors
from pprint import pprint as print




app = Flask(__name__)

@app.route("/index", methods= ["GET", 'POST'])
def home():
    
    return render_template("index-page.html.jinja")


@app.route("/land", methods= ["GET", 'POST'])
def landing():
    return render_template("landing-page.html.jinja")





@app.route("/dm", methods= ["GET", 'POST'])
def dm():
    return render_template("dm-page.html.jinja")

def send_message(student_id, tutor_id, message_text):
    connection = pymysql.connect(host='10.100.33.60',
                                 user='jedouard',
                                 password='224449553',
                                 database='tutoria')
    cursor = connection.cursor()
    sql = "INSERT INTO dm (student_id, tutor_id, message_text) VALUES (%s, %s, %s)"
    cursor.execute(sql, (student_id, tutor_id, message_text))
    connection.commit()
    connection.close()

# Sample data
student_id = 1  # Assuming sender's user ID
tutor_id = 2  # Assuming recipient's user ID
message_text = "Hello, how are you?"

# Call the function to send the message
send_message(student_id, tutor_id, message_text)





# Database connection settings
db_host = '10.100.33.60'
db_user = 'jedouard'
db_password = '224449553'
db_name = 'tutoria'

# Function to retrieve messages for a user from the database
def view_messages(user_id):
    connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    cursor = connection.cursor()
    sql = "SELECT * FROM dm WHERE student_id = %s OR tutor_id = %s"
    cursor.execute(sql, (user_id, user_id))
    messages = cursor.fetchall()
    connection.close()
    return messages

# Route for sender's messages
@app.route('/student')
def student_messages():
    student_id = 1  # Assuming sender's(student) user ID
    messages = view_messages(student_id)
    return render_template('message.html.jinja', messages=messages)

# Route for recipient's messages
@app.route('/tutor')
def tutor_messages():
    tutor_id = 2  # Assuming recipient's(tutor) user ID
    messages = view_messages(tutor_id)
    return render_template('message.html.jinja', messages=messages)

if __name__ == '__main__':
    app.run(debug=True) 

 



# Route for recipient's messages
@app.route('/tutor')
def recipient_messages():
    recipient_id = 2  # Assuming recipient's user ID
    messages = view_messages(recipient_id)
    return render_template('messages.html', messages=messages, tutor_id=tutor_id)

# Route for sending messages
@app.route('/send_message', methods=['POST'])
def send_message():
    tutor_id = request.form['tutor_id']
    message_text = request.form['message_text']
    connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    cursor = connection.cursor()
    sql = "INSERT INTO dm (student_id, tutor_id, message_text) VALUES (%s, %s, %s)"
    cursor.execute(sql, (tutor_id, 1, message_text))  # Assuming the sender(student) is always user ID 1
    connection.commit()
    connection.close()
    return redirect(url_for('tutor_messages'))

if __name__ == '__main__':
    app.run(debug=True)
