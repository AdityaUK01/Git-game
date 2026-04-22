"""
Git Commander Game - Flask Backend
Run: python app.py
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import pymysql
from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, redirect, session

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'gitcommander_secret_key_2024_change_in_prod')
CORS(app, supports_credentials=True)


DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),     # 
    'db':       'git_game',
    'charset':  'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

LEVEL_NAMES = {1:'Git Rookie',2:'Staging Apprentice',3:'Branch Cadet',4:'Diff Detective',
               5:'Merge Warrior',6:'Stash Master',7:'Time Traveler',8:'Rebase Ninja',
               9:'Release Engineer',10:'Git Grandmaster'}
LEVEL_COLORS = {1:'#3b82f6',2:'#8b5cf6',3:'#ec4899',4:'#f59e0b',5:'#ef4444',
                6:'#10b981',7:'#06b6d4',8:'#f97316',9:'#a855f7',10:'#eab308'}

def db():
    return pymysql.connect(**DB_CONFIG)

def normalize(cmd):
    return ' '.join(cmd.strip().lower().split())

def check_answer(user_input, answers):
    n = normalize(user_input)
    return any(normalize(a) == n for a in answers)

def uid():
    return session.get('user_id')

def require_auth(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not uid():
            return jsonify({'error': 'Not logged in', 'redirect': '/login'}), 401
        return f(*args, **kwargs)
    return wrapper

# ── Pages ─────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    if not uid():
        return render_template('login.html')
    return render_template('game.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

# ── Auth ──────────────────────────────────────────────────────────────────────
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json or {}
    username = (data.get('username') or '').strip()
    password = (data.get('password') or '').strip()

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    if len(username) < 3 or len(username) > 20:
        return jsonify({'error': 'Username must be 3–20 characters'}), 400
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return jsonify({'error': 'Username can only contain letters, numbers, underscores'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    con = db()
    try:
        with con.cursor() as c:
            c.execute("SELECT id FROM users WHERE LOWER(username) = LOWER(%s)", (username,))
            if c.fetchone():
                return jsonify({'error': 'Username already taken. Pick another one!'}), 409
            pw_hash = generate_password_hash(password)
            c.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, pw_hash))
            user_id = c.lastrowid
            c.execute("INSERT INTO user_profile (user_id) VALUES (%s)", (user_id,))
            con.commit()
            session['user_id'] = user_id
            session['username'] = username
            return jsonify({'ok': True, 'username': username})
    finally:
        con.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json or {}
    username = (data.get('username') or '').strip()
    password = (data.get('password') or '').strip()
    if not username or not password:
        return jsonify({'error': 'Fill in both fields'}), 400
    con = db()
    try:
        with con.cursor() as c:
            c.execute("SELECT * FROM users WHERE LOWER(username) = LOWER(%s)", (username,))
            user = c.fetchone()
            if not user or not check_password_hash(user['password_hash'], password):
                return jsonify({'error': 'Wrong username or password'}), 401
            session['user_id'] = user['id']
            session['username'] = user['username']
            return jsonify({'ok': True, 'username': user['username']})
    finally:
        con.close()

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'ok': True})

@app.route('/api/me')
def me():
    if not uid():
        return jsonify({'logged_in': False})
    return jsonify({'logged_in': True, 'username': session.get('username'), 'user_id': uid()})

# ── Profile ───────────────────────────────────────────────────────────────────
@app.route('/api/profile')
@require_auth
def get_profile():
    con = db()
    try:
        with con.cursor() as c:
            c.execute("SELECT * FROM user_profile WHERE user_id = %s", (uid(),))
            p = c.fetchone()
            if not p:
                c.execute("INSERT INTO user_profile (user_id) VALUES (%s)", (uid(),))
                con.commit()
                c.execute("SELECT * FROM user_profile WHERE user_id = %s", (uid(),))
                p = c.fetchone()
            for k in ('last_active',):
                if p.get(k): p[k] = p[k].isoformat()
            p['level_name']  = LEVEL_NAMES.get(p['current_level'], 'Unknown')
            p['level_color'] = LEVEL_COLORS.get(p['current_level'], '#6366f1')
            p['username']    = session.get('username')
            return jsonify(p)
    finally:
        con.close()

# ── Challenge ─────────────────────────────────────────────────────────────────
@app.route('/api/challenge')
@require_auth
def get_challenge():
    con = db()
    try:
        with con.cursor() as c:
            c.execute("SELECT current_level FROM user_profile WHERE user_id = %s", (uid(),))
            row = c.fetchone()
            level = row['current_level'] if row else 1
            c.execute("""
                SELECT c.id, c.level, c.category, c.difficulty, c.points, c.scenario, c.hint
                FROM challenges c
                WHERE c.level <= %s
                  AND c.id NOT IN (
                    SELECT DISTINCT challenge_id FROM attempt_history
                    WHERE user_id = %s AND is_correct = 1
                  )
                ORDER BY c.level ASC, RAND() LIMIT 1
            """, (level + 1, uid()))
            ch = c.fetchone()
            if not ch:
                c.execute("SELECT c.id,c.level,c.category,c.difficulty,c.points,c.scenario,c.hint FROM challenges c ORDER BY RAND() LIMIT 1")
                ch = c.fetchone()
            if ch:
                ch['level_name']  = LEVEL_NAMES.get(ch['level'], '')
                ch['level_color'] = LEVEL_COLORS.get(ch['level'], '#6366f1')
            return jsonify(ch or {})
    finally:
        con.close()

# ── Submit ────────────────────────────────────────────────────────────────────
@app.route('/api/submit', methods=['POST'])
@require_auth
def submit():
    data = request.json or {}
    cid        = data.get('challenge_id')
    user_input = data.get('command', '').strip()
    hint_used  = bool(data.get('hint_used', False))
    con = db()
    try:
        with con.cursor() as c:
            c.execute("SELECT answer FROM challenge_answers WHERE challenge_id = %s", (cid,))
            answers = [r['answer'] for r in c.fetchall()]
            c.execute("SELECT * FROM challenges WHERE id = %s", (cid,))
            ch = c.fetchone()
            c.execute("SELECT * FROM user_profile WHERE user_id = %s", (uid(),))
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
                c.execute("SELECT SUM(points) as total FROM challenges")
                max_pts = (c.fetchone()['total'] or 500)
                new_rank = min(100.0, round(new_score / max_pts * 100, 2))
                c.execute("SELECT COUNT(*) as tot FROM challenges WHERE level = %s", (prof['current_level'],))
                tot = c.fetchone()['tot']
                c.execute("""
                    SELECT COUNT(DISTINCT ah.challenge_id) as done
                    FROM attempt_history ah JOIN challenges ch ON ah.challenge_id = ch.id
                    WHERE ch.level = %s AND ah.is_correct = 1 AND ah.user_id = %s
                """, (prof['current_level'], uid()))
                done = c.fetchone()['done']
                new_level = prof['current_level']
                if done + 1 >= tot and prof['current_level'] < 10:
                    new_level = prof['current_level'] + 1
                    leveled_up = True
                c.execute("""
                    UPDATE user_profile
                    SET total_score=%s,rank_percentage=%s,streak=%s,max_streak=%s,
                        challenges_completed=%s,challenges_attempted=challenges_attempted+1,
                        hints_used=%s,current_level=%s
                    WHERE user_id=%s
                """, (new_score,new_rank,new_streak,new_max_str,new_completed,new_hints,new_level,uid()))
            else:
                new_rank = float(prof['rank_percentage'])
                new_level = prof['current_level']
                c.execute("UPDATE user_profile SET streak=0,challenges_attempted=challenges_attempted+1 WHERE user_id=%s",(uid(),))
            c.execute("INSERT INTO attempt_history (user_id,challenge_id,user_input,is_correct,points_earned,hint_used) VALUES (%s,%s,%s,%s,%s,%s)",
                      (uid(),cid,user_input,correct,pts,hint_used))
            con.commit()
            return jsonify({
                'correct': correct, 'points_earned': pts,
                'explanation': ch['explanation'],
                'correct_cmd': answers[0] if answers else '',
                'all_answers': answers,
                'leveled_up': leveled_up,
                'new_level': new_level,
                'new_level_name': LEVEL_NAMES.get(new_level, ''),
                'new_rank': new_rank,
            })
    finally:
        con.close()

# ── Hint ──────────────────────────────────────────────────────────────────────
@app.route('/api/hint/<int:cid>')
@require_auth
def hint(cid):
    con = db()
    try:
        with con.cursor() as c:
            c.execute("SELECT hint FROM challenges WHERE id = %s", (cid,))
            row = c.fetchone()
            return jsonify({'hint': row['hint'] if row else 'No hint available.'})
    finally:
        con.close()

# ── Leaderboard ───────────────────────────────────────────────────────────────
@app.route('/api/leaderboard')
def leaderboard():
    con = db()
    try:
        with con.cursor() as c:
            c.execute("""
                SELECT u.username, p.total_score, p.rank_percentage,
                       p.current_level, p.challenges_completed, p.max_streak,
                       p.challenges_attempted,
                       LEVEL_NAME.lname as level_name
                FROM user_profile p
                JOIN users u ON p.user_id = u.id
                CROSS JOIN (SELECT %s as lname) LEVEL_NAME
                ORDER BY p.total_score DESC, p.challenges_completed DESC
                LIMIT 50
            """, ('{level}',))
            rows = c.fetchall()
            # Fix level names
            c.execute("""
                SELECT u.username, p.total_score, p.rank_percentage,
                       p.current_level, p.challenges_completed, p.max_streak,
                       p.challenges_attempted
                FROM user_profile p
                JOIN users u ON p.user_id = u.id
                ORDER BY p.total_score DESC, p.challenges_completed DESC
                LIMIT 50
            """)
            rows = c.fetchall()
            for i, r in enumerate(rows):
                r['rank']        = i + 1
                r['level_name']  = LEVEL_NAMES.get(r['current_level'], 'Rookie')
                r['level_color'] = LEVEL_COLORS.get(r['current_level'], '#6366f1')
                r['accuracy']    = round(r['challenges_completed'] / max(r['challenges_attempted'], 1) * 100)
                for k in list(r.keys()):
                    if hasattr(r[k], 'isoformat'): r[k] = r[k].isoformat()
            current_user = session.get('username')
            my_rank = next((r['rank'] for r in rows if r['username'] == current_user), None)
            return jsonify({'leaderboard': rows, 'my_rank': my_rank})
    finally:
        con.close()

# ── Progress ──────────────────────────────────────────────────────────────────
@app.route('/api/progress')
@require_auth
def progress():
    con = db()
    try:
        with con.cursor() as c:
            c.execute("""
                SELECT c.level,
                    COUNT(DISTINCT c.id) AS total,
                    COUNT(DISTINCT CASE WHEN ah.is_correct=1 THEN ah.challenge_id END) AS completed
                FROM challenges c
                LEFT JOIN attempt_history ah ON c.id=ah.challenge_id AND ah.user_id=%s
                GROUP BY c.level ORDER BY c.level
            """, (uid(),))
            levels = c.fetchall()
            for lv in levels:
                lv['name']  = LEVEL_NAMES.get(lv['level'], '')
                lv['color'] = LEVEL_COLORS.get(lv['level'], '#6366f1')
            c.execute("""
                SELECT ah.user_input, ah.is_correct, ah.points_earned,
                       ah.attempted_at, c.scenario, c.level
                FROM attempt_history ah
                JOIN challenges c ON ah.challenge_id=c.id
                WHERE ah.user_id=%s
                ORDER BY ah.attempted_at DESC LIMIT 15
            """, (uid(),))
            history = c.fetchall()
            for h in history:
                if h.get('attempted_at'): h['attempted_at'] = h['attempted_at'].isoformat()
            c.execute("""
                SELECT c.category,
                       COUNT(*) as attempts,
                       SUM(ah.is_correct) as correct
                FROM attempt_history ah
                JOIN challenges c ON ah.challenge_id=c.id
                WHERE ah.user_id=%s
                GROUP BY c.category ORDER BY correct DESC
            """, (uid(),))
            by_cat = c.fetchall()
            return jsonify({'levels': levels, 'history': history, 'by_category': by_cat})
    finally:
        con.close()

# ── Error Challenges ──────────────────────────────────────────────────────────
@app.route('/api/error-challenges')
def error_challenges():
    con = db()
    try:
        with con.cursor() as c:
            c.execute("SELECT * FROM error_challenges ORDER BY id")
            return jsonify(c.fetchall())
    finally:
        con.close()

# ── Reset ─────────────────────────────────────────────────────────────────────
@app.route('/api/reset', methods=['POST'])
@require_auth
def reset():
    con = db()
    try:
        with con.cursor() as c:
            c.execute("DELETE FROM attempt_history WHERE user_id=%s", (uid(),))
            c.execute("""UPDATE user_profile SET total_score=0,rank_percentage=0,current_level=1,
                streak=0,max_streak=0,challenges_completed=0,challenges_attempted=0,hints_used=0
                WHERE user_id=%s""", (uid(),))
            con.commit()
        return jsonify({'ok': True})
    finally:
        con.close()

if __name__ == '__main__':
    print("🎮 Git Commander starting on http://localhost:5000")
    app.run(debug=True, port=5000)
