# 🎮 Git Commander — Interactive Git Learning Game

## What is this?
A personal web game that teaches all Git commands through interactive challenges.
- 50 challenges across 10 levels
- 0–100% ranking system based on your score
- Real error-based challenges (learn from mistakes)
- MySQL database tracks all your progress
- Streak system, hints, level-up celebrations

---

## Setup (5 minutes)

### Step 1 — Install Python dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Set your MySQL password
Open `setup_db.py` and `app.py` and set your MySQL password:
```python
'password': 'your_mysql_password_here',
```

### Step 3 — Create the database and seed challenges
```bash
python setup_db.py
```
This creates the `git_game` database and inserts all 50 challenges automatically.

### Step 4 — Run the game
```bash
python app.py
```

### Step 5 — Open your browser
Go to: **http://localhost:5000**

---

## How to Play

1. Read the scenario in the challenge card
2. Type the exact git command in the terminal input
3. Press Enter or click Submit
4. Get feedback + explanation
5. Use hints (costs -3 pts) if stuck
6. Complete all 5 challenges in a level to unlock the next
7. Your rank % grows as your score grows (max 100%)

## Levels

| Level | Name | Focus |
|-------|------|-------|
| 1 | Git Rookie | init, status, add, commit, log |
| 2 | Staging Apprentice | clone, remote, push, pull |
| 3 | Branch Cadet | branch, checkout, switch |
| 4 | Diff Detective | diff, staged, restore |
| 5 | Merge Warrior | merge, conflicts, abort |
| 6 | Stash Master | stash, pop, apply |
| 7 | Time Traveler | reset, revert, reflog |
| 8 | Rebase Ninja | rebase, cherry-pick, fetch |
| 9 | Release Engineer | tags, blame, bisect |
| 10 | Git Grandmaster | advanced mastery |

## Scoring
- Base points: 10–40 (increases per level)
- Streak bonus: +2 per consecutive correct answer (max +20)
- Hint penalty: -3 pts
- Rank % = (your score / max possible) × 100
- Max rank: 100%

## Error Challenges
The Errors tab shows 6 error challenges based on real Git errors:
- Push rejected
- Detached HEAD
- Merge conflict
- Fatal: not a git repository
- Nothing to commit
- Already up to date

---

## Reset
Click the ↺ Reset button in the app to wipe all progress and start fresh.
Challenge data is never deleted — only your attempt history.
