# app.py

from flask import Flask, request, render_template
from utils.mmr_medals import mmr_medals

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', result=None, mmr_medals=mmr_medals)

@app.route('/calculate', methods=['POST'])
def calculate():
    current_mmr = int(request.form['current_mmr'])
    goal_medal = request.form['goal_medal']
    goal_mmr = mmr_medals[goal_medal]

    mmr_diff = goal_mmr - current_mmr
    approximate_wins = max(round(mmr_diff / 25), 0)  # Approximate wins needed

    next_medal, mmr_to_next = next_medal_in(current_mmr)

    result = {
        'current_mmr': current_mmr,
        'goal_medal': goal_medal,
        'goal_mmr': goal_mmr,
        'mmr_diff': mmr_diff,
        'approximate_wins': approximate_wins,
        'next_medal': next_medal,
        'mmr_to_next': mmr_to_next
    }

    return render_template('index.html', result=result, mmr_medals=mmr_medals)

def next_medal_in(current_mmr):
    for medal, mmr in mmr_medals.items():
        if current_mmr < mmr:
            return medal, mmr - current_mmr
    return "Immortal", 0

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)