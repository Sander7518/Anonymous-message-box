from flask import Flask, request, render_template, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form.get('message')
        timestamp = datetime.now().isoformat()

        conn = sqlite3.connect('messages.db')
        c = conn.cursor()
        c.execute('INSERT INTO messages (content, timestamp) VALUES (?, ?)', (content, timestamp))
        conn.commit()
        conn.close()
        return redirect('/thanks')

    return render_template('index.html')

@app.route('/thanks')
def thanks():
    return "Thanks for sharing your message anonymously."

@app.route('/messages')
def view_messages():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('SELECT * FROM messages ORDER BY timestamp DESC')
    messages = c.fetchall()
    conn.close()
    return render_template('messages.html', messages=messages)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
