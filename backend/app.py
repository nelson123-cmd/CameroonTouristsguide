import os
from flask import Flask, request
from flask import Flask, request

app = Flask(__name__)

# Store all booking submissions
bookings = []  

#temporary message storage
messages = []

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

    messages.append({
        'name': name,
        'email': email,
        'subject': subject,
        'message': message
    })

    # Return confirmation + a button to go back
    return '''
    <html>
    <head><title>Thank You</title></head>
    <body style="font-family: Arial; text-align: center; padding-top: 50px;">
        <h2>THANK YOU FOR CONTACTING US.</h2>
        <h3>We have received your message.</h3>
        <h4>you will recieve a message in your Email with more details.</h4>
        <h5>our whatsapp: +237672706075.</h5>
        <a href="https://www.cameroontouristsguide.vercel.app">
        </a>
        <br><br>
        <a href="/">
            <button style="padding: 10px 20px; font-size: 16px;">Go to Home Page</button>
        </a>
    </body>
    </html>
    '''
#GET route for the contact page form (display)
@app.route('/contact', methods=['POST'])
def contact_form():
    return '''
    <html>
    <head><title>Contact Form</title></head>
    <body style="font-family: Arial;">
        <h2>Contact Us</h2>
        <form action="/contact" method="POST">
            <input type="text" name="name" placeholder="Your Name" required><br><br>
            <input type="email" name="email" placeholder="Your Email" required><br><br>
            <input type="text" name="subject" placeholder="Subject" required><br><br>
            <textarea name="message" rows="4" placeholder="Message" required></textarea><br><br>
            <button type="submit">Send Message</button>
        </form>
    </body>
    </html>
    '''


    return "<h2>Thank you for contacting us.</h2>"

# ADMIN VIEW OF ALL MESSAGES
@app.route('/messages')
def show_messages():
    html = "<h2>Submitted Contact Messages</h2><table border='1' cellpadding='8'>"
    html += "<tr><th>Name</th><th>Email</th><th>Subject</th><th>Message</th></tr>"

    for msg in messages:
        html += f"<tr><td>{msg['name']}</td><td>{msg['email']}</td><td>{msg['subject']}</td><td>{msg['message']}</td></tr>"

    html += "</table>"
    return html

#BOOKING FORM EXCLUSIVELY
@app.route('/booking', methods=['POST'])
def handle_bookings():
    name = request.form['name']
    email = request.form['email']
    date = request.form['date']
    time = request.form['time']

    destination = request.form['destination']
    special = request.form['special_request']

    booking = {
        'name': name,
        'email': email,
        'date': date,
        'time': time,
        'destination': destination,
        'special_request': special
    }

    bookings.append(booking)
    print(f"📌 New Booking Received:\n{booking}")

    return '''
    <html>
    <head><title>Thank You</title></head>
    <body style="font-family: Arial; text-align: center; padding-top: 50px;">
x   <h2>THANK YOU FOR BOOKING YOUR TOUR WITH US.</h2>
    <h3>we will get back to you with more details, through your Email</h3>
    <h4>our whatssapp contact: +237672706075.</h4>
    <a href="https://www.cameroontouristsguide.vercel.app">
        <button>Back to Homepage</button>
    </a>
    '''
#admin view table for bookings 
@app.route('/booking', methods=['POST'])
def view_bookings():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, email, date, time, destination, special request')
    rows = cursor.fetchall()
    conn.close()

    table_rows = ''
    for row in rows:
        table_rows += f'''
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
            <td>{row[3]}</td>
            <td>{row[4]}</td>
        </tr>
        '''

    return f'''
    <html>
    <head>
        <title>Booking Records</title>
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
                font-family: Arial;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h2>Customer Bookings</h2>
        <table>
            <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Date & Time</th>
                <th>Designation</th>
                <th>Special Request</th>
            </tr>
            {table_rows}
        </table>
        <br>
        <a href="/">Back to Home</a>
    </body>
    </html>
    '''


#Admin Route to View 
@app.route('/booking')
def show_bookings():
    html = "<h2>Submitted Booking</h2><table border='1' cellpadding='8'>"
    html += "<tr><th>Name</th><th>Email</th><th>Date</th><th>Time</th><th>destination</th><th>Special Request</th></tr>"

    for b in bookings:
        html += f"<tr><td>{b['name']}</td><td>{b['email']}</td><td>{b['date']}</td><td>{b['time']}</td><td>{b['destination']}</td><td>{b['special_request']}</td></tr>"

    html += "</table>"
    return html

        
#start sever
if __name__ == '__main__':
    import os

port = int(os.environ.get("PORT", 5000))  # Default to 5000 for local
app.run(host="0.0.0.0", port=port)

