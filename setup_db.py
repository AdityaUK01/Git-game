"""
Git Game - Database Setup Script
Run once: python setup_db.py
Edit DB_CONFIG below to match your MySQL credentials.
"""

import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "db": "git_game",
    "charset": "utf8mb4"
}

CHALLENGES = [
    {'level':1,'category':'basics','difficulty':'easy','points':10,'scenario':'You have a brand new project folder. You want Git to start tracking it. What is the very first command?','hint':'Think "initialize".','answers':['git init'],'explanation':'`git init` creates a hidden .git folder — makes any folder a Git repo. Run this once per project.'},
    {'level':1,'category':'basics','difficulty':'easy','points':10,'scenario':'You made changes to files. You want a quick overview — which files changed, which are new, which are staged. One command?','hint':'Shows the "state" of your working directory.','answers':['git status'],'explanation':'`git status` is your most-used command. Run it before and after everything. It costs nothing and shows everything.'},
    {'level':1,'category':'basics','difficulty':'easy','points':10,'scenario':'You edited 3 files and want to stage ALL of them at once for your next commit.','hint':'Use a dot to mean "everything here".','answers':['git add .','git add -A','git add --all'],'explanation':'`git add .` stages all changed and new files. The dot means "everything here". Use `git add filename` to stage one file.'},
    {'level':1,'category':'basics','difficulty':'easy','points':10,'scenario':'Files are staged. Save a snapshot (commit) with the message "initial commit".','hint':'Use the -m flag for inline messages.','answers':['git commit -m "initial commit"',"git commit -m 'initial commit'"],'explanation':'`git commit -m "message"` saves a permanent snapshot. Always write clear, descriptive messages.'},
    {'level':1,'category':'basics','difficulty':'easy','points':10,'scenario':'See the full history of all commits — who made them, when, and the messages.','hint':'Think "log" of events.','answers':['git log','git log --oneline','git log --oneline --graph'],'explanation':'`git log` shows commits newest to oldest. Use `git log --oneline` for compact view.'},
    {'level':2,'category':'remote','difficulty':'easy','points':12,'scenario':'Team repo is at https://github.com/team/project.git. Download a full copy to your computer.','hint':'It "copies" the remote repo locally.','answers':['git clone https://github.com/team/project.git'],'explanation':'`git clone <url>` downloads the entire repo. Automatically sets up "origin" remote.'},
    {'level':2,'category':'remote','difficulty':'easy','points':12,'scenario':'You ran `git init` locally. Connect it to GitHub at https://github.com/you/myapp.git with the name "origin".','hint':'You are "adding" a "remote".','answers':['git remote add origin https://github.com/you/myapp.git'],'explanation':'`git remote add origin <url>` links local repo to remote. "origin" is the universal convention.'},
    {'level':2,'category':'remote','difficulty':'easy','points':12,'scenario':'Upload your main branch to GitHub so your team can see your commits.','hint':'You are "pushing" to "origin" on branch "main".','answers':['git push origin main','git push -u origin main'],'explanation':'`git push origin main` uploads your local main to remote. First time use `-u` to set tracking.'},
    {'level':2,'category':'remote','difficulty':'easy','points':12,'scenario':'Teammate merged a PR. Download their latest changes from GitHub main into your local main.','hint':'You are "pulling" the latest code.','answers':['git pull origin main','git pull'],'explanation':'`git pull origin main` fetches AND merges remote changes. Always pull before starting work.'},
    {'level':2,'category':'remote','difficulty':'easy','points':12,'scenario':'Check all remote connections — names and exact URLs — for your repo.','hint':'The flag -v means "verbose".','answers':['git remote -v'],'explanation':'`git remote -v` lists all remotes with fetch and push URLs.'},
    {'level':3,'category':'branching','difficulty':'easy','points':15,'scenario':'See all local branches with a star showing the current one.','hint':'Just the word "branch" is enough.','answers':['git branch'],'explanation':'`git branch` lists all local branches. The * shows where you are. Use `-a` for all.'},
    {'level':3,'category':'branching','difficulty':'easy','points':15,'scenario':'Create a branch called "feature/login" AND switch to it in a single command.','hint':'Use checkout with -b flag.','answers':['git checkout -b feature/login','git switch -c feature/login'],'explanation':'`git checkout -b feature/login` creates and switches in one step. Always branch — never commit to main directly.'},
    {'level':3,'category':'branching','difficulty':'easy','points':15,'scenario':'Switch to an existing branch called "develop".','hint':'The branch already exists — no need to create it.','answers':['git checkout develop','git switch develop'],'explanation':'`git checkout develop` switches to the develop branch. Check `git status` first.'},
    {'level':3,'category':'branching','difficulty':'easy','points':15,'scenario':'Delete the local branch "feature/old-navbar" that was already merged.','hint':'Use the -d flag (lowercase = safe delete).','answers':['git branch -d feature/old-navbar'],'explanation':'`git branch -d` deletes a merged branch safely. Use `-D` to force-delete unmerged ones.'},
    {'level':3,'category':'branching','difficulty':'easy','points':15,'scenario':'See every branch — both local AND remote tracking branches.','hint':'The flag -a means "all".','answers':['git branch -a'],'explanation':'`git branch -a` shows local and remote branches. Remote branches appear as "remotes/origin/branchname".'},
    {'level':4,'category':'staging','difficulty':'medium','points':18,'scenario':'You changed files but have NOT staged them. See exact line-by-line differences.','hint':'Just "diff" — no extra flags for unstaged changes.','answers':['git diff'],'explanation':'`git diff` shows unstaged changes. Red = removed, green = added. Use before `git add`.'},
    {'level':4,'category':'staging','difficulty':'medium','points':18,'scenario':'After `git add`, see what is staged and will be included in your next commit.','hint':'Add --staged or --cached flag to diff.','answers':['git diff --staged','git diff --cached'],'explanation':'`git diff --staged` shows staged changes. Review exactly what you are about to commit.'},
    {'level':4,'category':'staging','difficulty':'medium','points':18,'scenario':'Stage only "src/pipeline.py" and leave all other changed files unstaged.','hint':'Provide the specific file path after `git add`.','answers':['git add src/pipeline.py'],'explanation':'`git add src/pipeline.py` stages only that file. Stage intentionally, not blindly.'},
    {'level':4,'category':'staging','difficulty':'medium','points':18,'scenario':'You staged "config.py" by mistake. UNSTAGE it without losing the changes in the file.','hint':'Think "restore" the staged state.','answers':['git restore --staged config.py','git reset HEAD config.py'],'explanation':'`git restore --staged config.py` removes from staging but leaves your edits in place.'},
    {'level':4,'category':'staging','difficulty':'medium','points':18,'scenario':'You made a mess of "pipeline.py". Throw away ALL your changes. Go back to last committed version. Permanent.','hint':'Use restore without the --staged flag.','answers':['git restore pipeline.py','git checkout -- pipeline.py'],'explanation':'`git restore pipeline.py` discards uncommitted changes permanently. Cannot be undone.'},
    {'level':5,'category':'merging','difficulty':'medium','points':20,'scenario':'You are on main branch. Merge the completed work from "feature/payment" into main.','hint':'You merge INTO your current branch.','answers':['git merge feature/payment'],'explanation':'`git merge feature/payment` merges into your current branch. Auto-completes if no conflicts.'},
    {'level':5,'category':'merging','difficulty':'medium','points':20,'scenario':'You started a merge but it is getting complicated. Cancel it and go back to before you started.','hint':'Abort the merge operation entirely.','answers':['git merge --abort'],'explanation':'`git merge --abort` cancels in-progress merge and restores pre-merge state.'},
    {'level':5,'category':'merging','difficulty':'medium','points':20,'scenario':'See commit history as a visual ASCII graph showing branches and merges.','hint':'Combine log with --oneline and --graph.','answers':['git log --oneline --graph','git log --oneline --graph --decorate'],'explanation':'`git log --oneline --graph` shows visual branch/merge history. Best way to understand repo structure.'},
    {'level':5,'category':'merging','difficulty':'medium','points':20,'scenario':'After manually fixing a merge conflict in a file, what do you run to tell Git it is resolved?','hint':'Stage the resolved file first.','answers':['git add .'],'explanation':'After fixing conflict markers, run `git add .` to mark resolved, then `git commit` to finalize.'},
    {'level':5,'category':'merging','difficulty':'medium','points':20,'scenario':'During a merge conflict — show ONLY the names of conflicted files, not the full diff.','hint':'git diff with --name-only flag.','answers':['git diff --name-only'],'explanation':'`git diff --name-only` lists just filenames. Useful to see which files need fixing without being overwhelmed.'},
    {'level':6,'category':'stash','difficulty':'medium','points':20,'scenario':'You are mid-coding. Manager wants an urgent fix on another branch. NOT ready to commit. Temporarily save your work.','hint':'Think of "stashing" valuables temporarily.','answers':['git stash','git stash push'],'explanation':'`git stash` saves uncommitted changes to a stack and reverts to last commit. Switch branches freely, come back later.'},
    {'level':6,'category':'stash','difficulty':'medium','points':20,'scenario':'Stash your changes with the label "WIP: S3 connection refactor".','hint':'Use push -m to add a message.','answers':['git stash push -m "WIP: S3 connection refactor"',"git stash push -m 'WIP: S3 connection refactor'"],'explanation':'`git stash push -m "message"` saves with a label. When you have multiple stashes, clear names are essential.'},
    {'level':6,'category':'stash','difficulty':'medium','points':20,'scenario':'See a list of all saved stashes.','hint':'Add "list" after git stash.','answers':['git stash list'],'explanation':'`git stash list` shows all stashes as stash@{0}, stash@{1}... Most recent is stash@{0}.'},
    {'level':6,'category':'stash','difficulty':'medium','points':20,'scenario':'Bring back your most recent stash AND remove it from the stash list at once.','hint':'"Pop" removes from the stack after applying.','answers':['git stash pop'],'explanation':'`git stash pop` applies the most recent stash and removes it. Pop = apply + delete.'},
    {'level':6,'category':'stash','difficulty':'medium','points':20,'scenario':'You have 3 stashes. Apply stash@{2} WITHOUT removing it from the list.','hint':'Use "apply" not "pop", specify the stash index.','answers':['git stash apply stash@{2}'],'explanation':'`git stash apply stash@{2}` applies without removing. Safer when unsure it will work cleanly.'},
    {'level':7,'category':'undoing','difficulty':'hard','points':25,'scenario':'You committed too early. Undo the last commit but KEEP all changes in your working directory.','hint':'--soft keeps your changes staged.','answers':['git reset --soft HEAD~1'],'explanation':'`git reset --soft HEAD~1` moves branch back 1 commit but leaves changes staged. Work is safe.'},
    {'level':7,'category':'undoing','difficulty':'hard','points':25,'scenario':'Completely undo the last commit AND delete all those changes permanently.','hint':'--hard is destructive. It deletes changes.','answers':['git reset --hard HEAD~1'],'explanation':'`git reset --hard HEAD~1` moves branch back AND deletes changes. Irreversible. Only use on unpushed commits.'},
    {'level':7,'category':'undoing','difficulty':'hard','points':25,'scenario':'You pushed a bad commit to a shared branch. Safely undo it by creating a new commit that reverses the changes.','hint':'Revert = safe undo that adds a new commit.','answers':['git revert HEAD','git revert HEAD --no-edit'],'explanation':'`git revert HEAD` creates a commit that is the exact opposite. ONLY safe way to undo on shared branches.'},
    {'level':7,'category':'undoing','difficulty':'hard','points':25,'scenario':'A disaster happened — lost commits or messed up a rebase. Show a log of EVERY action Git has done including deleted history.','hint':'Think "reference log" — the ultimate recovery tool.','answers':['git reflog'],'explanation':'`git reflog` shows every HEAD operation for 90 days. Even deleted commits exist here. The ultimate recovery tool.'},
    {'level':7,'category':'undoing','difficulty':'hard','points':25,'scenario':'You ran `git add .` and staged everything by accident. Unstage ALL files at once without losing changes.','hint':'Restore staged state for all files using a dot.','answers':['git restore --staged .','git reset HEAD'],'explanation':'`git restore --staged .` unstages all files at once. File contents unchanged.'},
    {'level':8,'category':'advanced','difficulty':'hard','points':30,'scenario':'Your feature branch is a week behind main. Replay your commits ON TOP of the latest main for clean linear history.','hint':'You are "rebasing" your branch onto main.','answers':['git rebase main'],'explanation':'`git rebase main` replays your commits on top of latest main. Clean linear history. NEVER rebase shared branches.'},
    {'level':8,'category':'advanced','difficulty':'hard','points':30,'scenario':'You made 4 messy WIP commits. Combine them into 1 clean commit before opening a PR.','hint':'Interactive rebase to edit the last 4 commits.','answers':['git rebase -i HEAD~4'],'explanation':'`git rebase -i HEAD~4` opens interactive editor to squash, reword, or drop commits. How pros clean up before review.'},
    {'level':8,'category':'advanced','difficulty':'hard','points':30,'scenario':'A fix was merged last week with hash "abc1234". Apply ONLY that one specific commit to your current branch.','hint':'Pick just that one specific commit "cherry".','answers':['git cherry-pick abc1234'],'explanation':'`git cherry-pick abc1234` applies one specific commit. Useful when you need a fix without merging the whole branch.'},
    {'level':8,'category':'advanced','difficulty':'hard','points':30,'scenario':'Download all remote changes but do NOT apply them yet. Just see what changed.','hint':'Fetch downloads, pull downloads + merges.','answers':['git fetch --all','git fetch','git fetch origin'],'explanation':'`git fetch --all` downloads without modifying local branches. Then `git diff origin/main` to inspect first.'},
    {'level':8,'category':'advanced','difficulty':'hard','points':30,'scenario':'Push new local branch "feature/dashboard" to GitHub first time and set up automatic tracking.','hint':'The -u flag sets the upstream.','answers':['git push -u origin feature/dashboard'],'explanation':'`git push -u origin feature/dashboard` pushes AND sets upstream tracking. After this, just `git push` works.'},
    {'level':9,'category':'tags','difficulty':'hard','points':30,'scenario':'Mark this commit as version "v2.0.0" with annotation and message "Production release".','hint':'Annotated tags use -a flag and -m for message.','answers':['git tag -a v2.0.0 -m "Production release"',"git tag -a v2.0.0 -m 'Production release'"],'explanation':'`git tag -a v2.0.0 -m "..."` creates an annotated tag with metadata. Preferred for releases.'},
    {'level':9,'category':'tags','difficulty':'hard','points':30,'scenario':'You created tags locally. They are NOT on GitHub yet. Push ALL of them.','hint':'Tags need separate pushing — regular push skips them.','answers':['git push origin --tags','git push --tags'],'explanation':'`git push origin --tags` pushes all local tags. Regular `git push` skips tags.'},
    {'level':9,'category':'inspection','difficulty':'hard','points':30,'scenario':'See which developer changed each specific LINE of "models/etl.py" and which commit it belongs to.','hint':'Git "blames" a file to show line-by-line authorship.','answers':['git blame models/etl.py'],'explanation':'`git blame models/etl.py` annotates each line with commit hash, author, and date.'},
    {'level':9,'category':'inspection','difficulty':'hard','points':30,'scenario':'A bug exists between last week (abc1111) and today. Use Git binary search to find the exact commit that broke things.','hint':'Start the binary search session.','answers':['git bisect start'],'explanation':'`git bisect start` begins binary search. Mark bad/good commits and Git checks out the middle each time.'},
    {'level':9,'category':'inspection','difficulty':'hard','points':30,'scenario':'See a compact summary of the last commit — just files changed and how many lines added/removed.','hint':'Use git show with --stat flag.','answers':['git show --stat','git show --stat HEAD'],'explanation':'`git show --stat` shows last commit metadata and file change summary.'},
    {'level':10,'category':'master','difficulty':'expert','points':40,'scenario':'Your rebase went wrong and Git is stuck. Cancel the rebase and return to the state before you started.','hint':'Abort the rebase.','answers':['git rebase --abort'],'explanation':'`git rebase --abort` cancels in-progress rebase. Always use this over trying to fix mid-flight.'},
    {'level':10,'category':'master','difficulty':'expert','points':40,'scenario':'You rebased locally and need to force-push. Do it safely — ensuring nobody else pushed to the remote branch since your last fetch.','hint':'Use force-with-lease, not plain force.','answers':['git push --force-with-lease'],'explanation':'`git push --force-with-lease` refuses if remote was updated since your last fetch. NEVER use --force on shared branches.'},
    {'level':10,'category':'master','difficulty':'expert','points':40,'scenario':'Your working directory has untracked files and empty folders cluttering things up. Delete ALL of them permanently.','hint':'-f for force, -d for directories.','answers':['git clean -fd','git clean -f -d'],'explanation':'`git clean -fd` removes all untracked files and directories. Run `git clean -nfd` first for dry run.'},
    {'level':10,'category':'master','difficulty':'expert','points':40,'scenario':'Permanently remove a secret key file from ALL commit history — not just the latest commit. Emergency cleanup.','hint':'This requires rewriting history with a filter.','answers':['git filter-branch --tree-filter "rm -f secrets.txt" HEAD','git filter-repo --path secrets.txt --invert-paths'],'explanation':'Filter-branch rewrites every commit to remove the file. Force-push all branches after and rotate credentials immediately.'},
    {'level':10,'category':'master','difficulty':'expert','points':40,'scenario':'Add an external Git repo as a subdirectory inside your project, keeping its history separate.','hint':'Git has a feature for embedding repos inside repos.','answers':['git submodule add'],'explanation':'`git submodule add <url>` embeds another repo as a subdirectory. After cloning: `git submodule update --init`.'},
]

ERROR_CHALLENGES = [
    {'error_type':'push_rejected','error_message':"error: failed to push some refs — Updates were rejected because the remote contains work that you do not have locally",'scenario':'You tried to push but GitHub rejected it. Remote has commits you do not have. What is the SAFE way to resolve before pushing?','correct_command':'git pull --rebase origin main','explanation':'`git pull --rebase origin main` downloads remote commits and replays yours on top. Then push normally.'},
    {'error_type':'detached_head','error_message':"You are in 'detached HEAD' state. Changes made here may be lost.",'scenario':'Git says you are in "detached HEAD" state. Get back to the main branch safely.','correct_command':'git switch main','explanation':'"Detached HEAD" means you checked out a commit instead of a branch. Run `git switch main` to return.'},
    {'error_type':'merge_conflict','error_message':"CONFLICT (content): Merge conflict in src/pipeline.py — Automatic merge failed; fix conflicts and then commit.",'scenario':'Merge conflict in "src/pipeline.py". After fixing the conflict markers in the file, what do you run?','correct_command':'git add src/pipeline.py','explanation':'After removing the <<<, ===, >>> markers — run `git add` to mark resolved, then `git commit` to finalize.'},
    {'error_type':'not_a_repo','error_message':"fatal: not a git repository (or any of the parent directories): .git",'scenario':'You got "fatal: not a git repository". Fix this assuming you want to start a new repo here.','correct_command':'git init','explanation':'This means Git is not tracking this folder. Either `cd` into the right directory, or `git init` to create a new repo.'},
    {'error_type':'nothing_to_commit','error_message':"nothing to commit, working tree clean",'scenario':'Git says "nothing to commit, working tree clean." You forgot to stage files before committing. What should you have run first?','correct_command':'git add .','explanation':'You must stage files with `git add` before committing. Run `git status` first, then `git add .` to stage.'},
    {'error_type':'already_up_to_date','error_message':"Already up to date. — But your push still gets rejected.",'scenario':'`git pull` says "Already up to date" but push still fails. You might be on the wrong branch. What shows which branch you are on?','correct_command':'git branch','explanation':'Run `git branch` to see your current branch (starred). Check `git remote -v` and `git branch -vv` for tracking config.'},
]

def setup():
    print("🔌 Connecting to MySQL...")
    conn = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
    c = conn.cursor()
    c.execute("CREATE DATABASE IF NOT EXISTS git_game CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    c.execute("USE git_game")
    print("📋 Creating tables...")
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS user_profile (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL UNIQUE,
        total_score INT DEFAULT 0,
        rank_percentage DECIMAL(5,2) DEFAULT 0.00,
        current_level INT DEFAULT 1,
        streak INT DEFAULT 0,
        max_streak INT DEFAULT 0,
        challenges_completed INT DEFAULT 0,
        challenges_attempted INT DEFAULT 0,
        hints_used INT DEFAULT 0,
        last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS challenges (
        id INT AUTO_INCREMENT PRIMARY KEY,
        level INT NOT NULL,
        category VARCHAR(50),
        difficulty VARCHAR(20),
        points INT DEFAULT 10,
        scenario TEXT NOT NULL,
        hint TEXT,
        explanation TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS challenge_answers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        challenge_id INT NOT NULL,
        answer TEXT NOT NULL,
        is_primary BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (challenge_id) REFERENCES challenges(id) ON DELETE CASCADE
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS attempt_history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        challenge_id INT NOT NULL,
        user_input TEXT,
        is_correct TINYINT(1) DEFAULT 0,
        points_earned INT DEFAULT 0,
        hint_used TINYINT(1) DEFAULT 0,
        attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (challenge_id) REFERENCES challenges(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS error_challenges (
        id INT AUTO_INCREMENT PRIMARY KEY,
        error_type VARCHAR(100) UNIQUE,
        error_message TEXT,
        scenario TEXT,
        correct_command TEXT,
        explanation TEXT
    )""")
    c.execute("SELECT COUNT(*) as cnt FROM challenges")
    if c.fetchone()['cnt'] == 0:
        print(f"🌱 Seeding {len(CHALLENGES)} challenges...")
        for ch in CHALLENGES:
            c.execute("INSERT INTO challenges (level,category,difficulty,points,scenario,hint,explanation) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (ch['level'],ch['category'],ch['difficulty'],ch['points'],ch['scenario'],ch['hint'],ch['explanation']))
            cid = c.lastrowid
            for i, ans in enumerate(ch['answers']):
                c.execute("INSERT INTO challenge_answers (challenge_id,answer,is_primary) VALUES (%s,%s,%s)",(cid,ans,i==0))
    c.execute("SELECT COUNT(*) as cnt FROM error_challenges")
    if c.fetchone()['cnt'] == 0:
        print(f"⚠️  Seeding {len(ERROR_CHALLENGES)} error challenges...")
        for ec in ERROR_CHALLENGES:
            c.execute("INSERT INTO error_challenges (error_type,error_message,scenario,correct_command,explanation) VALUES (%s,%s,%s,%s,%s)",
                (ec['error_type'],ec['error_message'],ec['scenario'],ec['correct_command'],ec['explanation']))
    conn.commit()
    conn.close()
    print("\n✅ Done! Now run: python app.py")
    print("🌐 Open: http://localhost:5000")

if __name__ == '__main__':
    setup()
