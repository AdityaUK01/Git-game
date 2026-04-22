"""
Git Commander Game - Flask Backend
Run: python app.py
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import pymysql
import os

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    'host':     os.getenv('DB_HOST', 'localhost'),
    'user':     os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASS', 'Aditya12@@'),       # ← set your password
    'db':       'git_game',
    'charset':  'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

LEVEL_NAMES = {
    1: 'Git Rookie', 2: 'Staging Apprentice', 3: 'Branch Cadet',
    4: 'Diff Detective', 5: 'Merge Warrior', 6: 'Stash Master',
    7: 'Time Traveler', 8: 'Rebase Ninja', 9: 'Release Engineer',
    10: 'Git Grandmaster',
}
LEVEL_COLORS = {
    1: '#3b82f6', 2: '#8b5cf6', 3: '#ec4899', 4: '#f59e0b',
    5: '#ef4444', 6: '#10b981', 7: '#06b6d4', 8: '#f97316',
    9: '#a855f7', 10: '#eab308',
}

def db():
    return pymysql.connect(**DB_CONFIG)

def normalize(cmd):
    return ' '.join(cmd.strip().lower().split())

def check_answer(user_input, answers):
    n = normalize(user_input)
    return any(normalize(a) == n for a in answers)

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/profile')
def get_profile():
    con = db()
    try:
        with con.cursor() as c:
            c.execute("SELECT * FROM user_profile WHERE id = 1")
            p = c.fetchone()
            if not p:
                c.execute("INSERT INTO user_profile (username) VALUES ('Git Commander')")
                con.commit()
                c.execute("SELECT * FROM user_profile WHERE id = 1")
                p = c.fetchone()
            # Serialize datetimes
            for k in ('created_at', 'last_active'):
                if p.get(k): p[k] = p[k].isoformat()
            p['level_name']  = LEVEL_NAMES.get(p['current_level'], 'Unknown')
            p['level_color'] = LEVEL_COLORS.get(p['current_level'], '#6366f1')
            return jsonify(p)
    finally:
        con.close()

@app.route('/api/challenge')
def get_challenge():
    """Return next unattempted challenge; fall back to random review."""
    con = db()
    try:
        with con.cursor() as c:
            c.execute("SELECT current_level FROM user_profile WHERE id = 1")
            row = c.fetchone()
            level = row['current_level'] if row else 1

            # Prefer unattempted challenges at or below current level + 1
            c.execute("""
                SELECT c.id, c.level, c.category, c.difficulty, c.points, c.scenario, c.hint
                FROM challenges c
                WHERE c.level <= %s
                  AND c.id NOT IN (
                      SELECT DISTINCT challenge_id FROM attempt_history WHERE is_correct = 1
                  )
                ORDER BY c.level ASC, RAND()
                LIMIT 1
            """, (level + 1,))
            ch = c.fetchone()

            if not ch:
                # All done — review mode: random from all
                c.execute("""
                    SELECT c.id, c.level, c.category, c.difficulty, c.points, c.scenario, c.hint
                    FROM challenges c
                    ORDER BY RAND() LIMIT 1
                """)
                ch = c.fetchone()

            if ch:
                ch['level_name']  = LEVEL_NAMES.get(ch['level'], '')
                ch['level_color'] = LEVEL_COLORS.get(ch['level'], '#6366f1')
            return jsonify(ch or {})
    finally:
        con.close()

@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.json or {}
    cid        = data.get('challenge_id')
    user_input = data.get('command', '').strip()
    hint_used  = bool(data.get('hint_used', False))

    con = db()
    try:
        with con.cursor() as c:
            # Answers
            c.execute("SELECT answer FROM challenge_answers WHERE challenge_id = %s", (cid,))
            answers = [r['answer'] for r in c.fetchall()]

            # Challenge meta
            c.execute("SELECT * FROM challenges WHERE id = %s", (cid,))
            ch = c.fetchone()

            # Profile
            c.execute("SELECT * FROM user_profile WHERE id = 1")
            prof = c.fetchone()

            correct = check_answer(user_input, answers)
            pts = 0
            leveled_up = False

            if correct:
                base = ch['points']
                streak_bonus = min(prof['streak'] * 2, 20)
                hint_penalty = 3 if hint_used else 0
                pts = max(0, base + streak_bonus - hint_penalty)

                new_streak    = prof['streak'] + 1
                new_score     = prof['total_score'] + pts
                new_completed = prof['challenges_completed'] + 1
                new_max_str   = max(prof['max_streak'], new_streak)
                new_hints     = prof['hints_used'] + (1 if hint_used else 0)

                # Rank 0-100
                c.execute("SELECT SUM(points) as total FROM challenges")
                max_pts = (c.fetchone()['total'] or 500)
                new_rank = min(100.0, round(new_score / max_pts * 100, 2))

                # Level-up check
                c.execute("SELECT COUNT(*) as tot FROM challenges WHERE level = %s", (prof['current_level'],))
                tot = c.fetchone()['tot']
                c.execute("""
                    SELECT COUNT(DISTINCT ah.challenge_id) as done
                    FROM attempt_history ah JOIN challenges ch ON ah.challenge_id = ch.id
                    WHERE ch.level = %s AND ah.is_correct = 1
                """, (prof['current_level'],))
                done = c.fetchone()['done']

                new_level = prof['current_level']
                if done + 1 >= tot and prof['current_level'] < 10:
                    new_level = prof['current_level'] + 1
                    leveled_up = True

                c.execute("""
                    UPDATE user_profile
                    SET total_score=%s, rank_percentage=%s, streak=%s, max_streak=%s,
                        challenges_completed=%s, challenges_attempted=challenges_attempted+1,
                        hints_used=%s, current_level=%s
                    WHERE id = 1
                """, (new_score, new_rank, new_streak, new_max_str, new_completed, new_hints, new_level))
            else:
                c.execute("UPDATE user_profile SET streak=0, challenges_attempted=challenges_attempted+1 WHERE id=1")
                new_rank = float(prof['rank_percentage'])
                new_level = prof['current_level']

            # Log attempt
            c.execute("""
                INSERT INTO attempt_history (challenge_id, user_input, is_correct, points_earned, hint_used)
                VALUES (%s, %s, %s, %s, %s)
            """, (cid, user_input, correct, pts, hint_used))

            con.commit()

            return jsonify({
                'correct':       correct,
                'points_earned': pts,
                'explanation':   ch['explanation'],
                'correct_cmd':   answers[0] if answers else '',
                'all_answers':   answers,
                'leveled_up':    leveled_up,
                'new_level':     new_level,
                'new_level_name': LEVEL_NAMES.get(new_level, ''),
                'new_rank':      new_rank,
            })
    finally:
        con.close()

@app.route('/api/hint/<int:cid>')
def hint(cid):
    con = db()
    try:
        with con.cursor() as c:
            c.execute("SELECT hint FROM challenges WHERE id = %s", (cid,))
            row = c.fetchone()
            return jsonify({'hint': row['hint'] if row else 'No hint available.'})
    finally:
        con.close()

@app.route('/api/progress')
def progress():
    con = db()
    try:
        with con.cursor() as c:
            c.execute("""
                SELECT c.level,
                    COUNT(DISTINCT c.id)                                           AS total,
                    COUNT(DISTINCT CASE WHEN ah.is_correct=1 THEN ah.challenge_id END) AS completed
                FROM challenges c
                LEFT JOIN attempt_history ah ON c.id = ah.challenge_id
                GROUP BY c.level ORDER BY c.level
            """)
            levels = c.fetchall()
            for lv in levels:
                lv['name']  = LEVEL_NAMES.get(lv['level'], '')
                lv['color'] = LEVEL_COLORS.get(lv['level'], '#6366f1')

            c.execute("""
                SELECT ah.user_input, ah.is_correct, ah.points_earned,
                       ah.attempted_at, c.scenario, c.level
                FROM attempt_history ah
                JOIN challenges c ON ah.challenge_id = c.id
                ORDER BY ah.attempted_at DESC LIMIT 15
            """)
            history = c.fetchall()
            for h in history:
                if h.get('attempted_at'): h['attempted_at'] = h['attempted_at'].isoformat()

            return jsonify({'levels': levels, 'history': history})
    finally:
        con.close()

@app.route('/api/stats')
def stats():
    con = db()
    try:
        with con.cursor() as c:
            c.execute("""
                SELECT COUNT(*) as total_attempts,
                       SUM(is_correct) as correct_answers,
                       SUM(points_earned) as total_points,
                       MAX(points_earned) as best_single
                FROM attempt_history
            """)
            s = c.fetchone()
            c.execute("""
                SELECT c.category,
                       COUNT(*) as attempts,
                       SUM(ah.is_correct) as correct
                FROM attempt_history ah
                JOIN challenges c ON ah.challenge_id = c.id
                GROUP BY c.category ORDER BY correct DESC
            """)
            by_cat = c.fetchall()
            return jsonify({'summary': s, 'by_category': by_cat})
    finally:
        con.close()

@app.route('/api/error-challenges')
def error_challenges():
    con = db()
    try:
        with con.cursor() as c:
            c.execute("SELECT * FROM error_challenges ORDER BY times_encountered DESC")
            rows = c.fetchall()
            return jsonify(rows)
    finally:
        con.close()

@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset all progress — for personal use."""
    con = db()
    try:
        with con.cursor() as c:
            c.execute("DELETE FROM attempt_history")
            c.execute("""
                UPDATE user_profile SET
                    total_score=0, rank_percentage=0, current_level=1,
                    streak=0, max_streak=0, challenges_completed=0,
                    challenges_attempted=0, hints_used=0
                WHERE id=1
            """)
            c.execute("UPDATE error_challenges SET unlocked=0, times_encountered=0")
            con.commit()
        return jsonify({'ok': True})
    finally:
        con.close()

if __name__ == '__main__':
    print("🎮 Git Commander starting on http://localhost:5000")
    app.run(debug=True, port=5000)
