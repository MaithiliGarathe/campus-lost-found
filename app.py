from flask import Flask, render_template, request, redirect
import mysql.connector
from db_config import db_config
from datetime import date

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items ORDER BY id DESC")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        location = request.form['location']
        contact_info = request.form['contact_info']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO items (name, description, category, location, date_posted, status, contact_info) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (name, description, category, location, date.today(), 'Missing', contact_info)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/')
    return render_template('post.html')

@app.route('/update/<int:item_id>')
def update(item_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET status = 'Claimed' WHERE id = %s", (item_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)