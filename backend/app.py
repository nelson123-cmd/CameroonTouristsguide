import os
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend (Vercel) to send requests

# Store submissions in memory
bookings = []
messages = []

# === HOME ===
@app.route('/')
def home():
    return render_template('index.html')

# === CONTACT FORM HANDLING ===
@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    messages.append({
        'name': name,
        'email': email,
        'subject': subject,
        'message': message
    })

    print(f"📨 New Contact Message: {name} ({email})")

    return '''
    <html>

    <body style="font-family: Arial; text-align: center; padding-top: 50px;">
        <h2>THANK YOU FOR CONTACTING US.</h2>
        <h3>We have received your message.</h3>
    <a href="https://www.cameroontouristsguide.vercel.app">
            <button>Back to Home</button>
    </a>
    </body>
    </html>
    '''

# === VIEW CONTACT MESSAGES ===
@app.route('/messages', methods=['GET'])
def show_messages():
    html = "<h2>Contact Messages</h2><table border='1'><tr><th>Name</th><th>Email</th><th>Subject</th><th>Message</th></tr>"
    for msg in messages:
        html += f"<tr><td>{msg['name']}</td><td>{msg['email']}</td><td>{msg['subject']}</td><td>{msg['message']}</td></tr>"
    html += "</table>"
    return html

# === BOOKING FORM HANDLING ===
@app.route('/booking', methods=['POST'])
def handle_booking():
    name = request.form.get('name')
    email = request.form.get('email')
    date = request.form.get('date')
    time = request.form.get('time')
    destination = request.form.get('destination')
    special = request.form.get('special_request')

    booking = {
        'name': name,
        'email': email,
        'date': date,
        'time': time,
        'destination': destination,
        'special_request': special
    }

    bookings.append(booking)
    print(f"📌 New Booking: {booking}")

    return '''
  <html>
    <body style="font-family: Arial; text-align: center; padding-top: 50px;">
        <h2>THANK YOU FOR BOOKING YOUR TOUR WITH US.</h2>
        <h3>We will contact you via email.</h3>
        <a href="https://www.cameroontouristsguide.vercel.app">
            <button>Back to Homepage</button>
        </a>
    </body>
    </html>
    '''

# === VIEW BOOKINGS ===
@app.route('/bookings', methods=['GET'])
def show_bookings():
    html = "<h2>Bookings</h2><table border='1'><tr><th>Name</th><th>Email</th><th>Date</th><th>Time</th><th>Destination</th><th>Special Request</th></tr>"
    for b in bookings:
        html += f"<tr><td>{b['name']}</td><td>{b['email']}</td><td>{b['date']}</td><td>{b['time']}</td><td>{b['destination']}</td><td>{b['special_request']}</td></tr>"
        html += "</table>"
    return html

# === RUN APP ===
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
