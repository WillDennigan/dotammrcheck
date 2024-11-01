# app.py

from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
from utils.mmr_medals import mmr_medals  # Import remains the same

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Connect to the database
def get_db_connection():
    conn = sqlite3.connect('mmr_database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM MMRTable ORDER BY ROWID ASC LIMIT 1')
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        user_data = dict(user_data)
        current_mmr = user_data['currentMMR']
        goal_medal = user_data['goalMedal']
        goal_mmr = mmr_medals[goal_medal]
        mmr_diff = goal_mmr - current_mmr
        approximate_wins = round(mmr_diff / 25) if mmr_diff > 0 else 0
        next_medal, mmr_to_next = next_medal_in(current_mmr)
        return render_template('index.html', user_data=user_data, approximate_wins=approximate_wins, next_medal=next_medal, mmr_to_next=mmr_to_next, mmr_medals=mmr_medals)
    
    # Pass mmr_medals even when no user data is found
    return render_template('index.html', user_data=None, mmr_medals=mmr_medals)

@app.route('/update_mmr', methods=['POST'])
def update_mmr():
    user = request.form['user']
    mmr_value = int(request.form['mmr'])
    goal_medal = request.form['goal_medal']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO MMRTable (user, currentMMR, goalMedal) VALUES (?, ?, ?)
    ''', (user, mmr_value, goal_medal))
    conn.commit()
    conn.close()

    flash(f"Updated MMR for user: {user}")
    return redirect(url_for('index'))

def next_medal_in(current_mmr):
    for medal, mmr in mmr_medals.items():
        if current_mmr < mmr:
            return medal, mmr - current_mmr
    return "Immortal", 0

if __name__ == '__main__':
    # Initialize the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MMRTable (
            user TEXT PRIMARY KEY,
            currentMMR INTEGER,
            goalMedal TEXT
        )
    ''')
    conn.commit()
    conn.close()

    app.run(host='0.0.0.0', port=80)
