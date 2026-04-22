"""
Git Game - Database Setup Script
Run once: python setup_db.py
Edit DB_CONFIG below to match your MySQL credentials.
"""

import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Aditya12@@',        # ← set your MySQL password here
    'charset': 'utf8mb4',
}

CHALLENGES = [
    # ── LEVEL 1 · Git Basics ──────────────────────────────────────────
    {
        'level': 1, 'category': 'basics', 'difficulty': 'easy', 'points': 10,
        'scenario': 'You have a brand new project folder on your computer. You want Git to start tracking it. What is the very first command you run?',
        'hint': 'Think "initialize".',
        'explanation': '`git init` creates a hidden .git folder in your project. This is what makes a folder a Git repository. Run this once when starting any new project.',
        'answers': ['git init'],
    },
    {
        'level': 1, 'category': 'basics', 'difficulty': 'easy', 'points': 10,
        'scenario': 'You made some changes to files. Before doing anything else, you want to see which files were changed, which are new, and which are staged. What command shows you this overview?',
        'hint': 'It shows you the "state" of your working directory.',
        'explanation': '`git status` is your go-to command to see what is going on. It shows untracked files, modified files, and what is staged. Run it constantly — it costs nothing.',
        'answers': ['git status'],
    },
    {
        'level': 1, 'category': 'basics', 'difficulty': 'easy', 'points': 10,
        'scenario': 'You edited 3 files and want to stage ALL of them for your next commit at once. What command stages everything in the current directory?',
        'hint': 'Use a dot to mean "everything here".',
        'explanation': '`git add .` stages all changed and new files in the current directory. The dot means "current directory and everything inside it". Use `git add filename` to stage one specific file.',
        'answers': ['git add .', 'git add -A', 'git add --all'],
    },
    {
        'level': 1, 'category': 'basics', 'difficulty': 'easy', 'points': 10,
        'scenario': 'Your files are staged. Now you want to save a snapshot (commit) with the message "initial commit". What is the exact command?',
        'hint': 'Use the -m flag for inline messages.',
        'explanation': '`git commit -m "initial commit"` saves a permanent snapshot. The -m flag lets you write the message inline. Without -m, Git opens a text editor. Always write a clear, descriptive message.',
        'answers': ['git commit -m "initial commit"', "git commit -m 'initial commit'"],
    },
    {
        'level': 1, 'category': 'basics', 'difficulty': 'easy', 'points': 10,
        'scenario': 'You want to see the full history of all commits in your repo — who made them, when, and the messages. What command shows this?',
        'hint': 'Think about viewing the "log" of events.',
        'explanation': '`git log` shows all commits from newest to oldest with author, date, and full message. Use `git log --oneline` for a compact one-line-per-commit view. Very useful for reviewing history.',
        'answers': ['git log', 'git log --oneline', 'git log --oneline --graph'],
    },

    # ── LEVEL 2 · Remote & Clone ──────────────────────────────────────
    {
        'level': 2, 'category': 'remote', 'difficulty': 'easy', 'points': 12,
        'scenario': 'Your team has a repo on GitHub at https://github.com/team/project.git and you want to download a full copy to your computer. What command do you use?',
        'hint': 'It "copies" or "clones" the remote repo locally.',
        'explanation': '`git clone <url>` downloads the entire repository including all commits, branches, and history. It automatically sets up the remote connection called "origin". This is how you start working on an existing project.',
        'answers': ['git clone https://github.com/team/project.git'],
    },
    {
        'level': 2, 'category': 'remote', 'difficulty': 'easy', 'points': 12,
        'scenario': 'You ran `git init` locally and now want to connect it to a GitHub repo. The GitHub URL is https://github.com/you/myapp.git. Connect it with the name "origin".',
        'hint': 'You are "adding" a "remote" connection.',
        'explanation': '`git remote add origin <url>` links your local repo to a remote one. "origin" is just a name — you could call it anything, but "origin" is the universal convention. Run `git remote -v` to verify.',
        'answers': ['git remote add origin https://github.com/you/myapp.git'],
    },
    {
        'level': 2, 'category': 'remote', 'difficulty': 'easy', 'points': 12,
        'scenario': 'You committed your work and now want to upload (push) your main branch to GitHub so your team can see it.',
        'hint': 'You are "pushing" to "origin" on branch "main".',
        'explanation': '`git push origin main` uploads your local main branch to the remote called origin. The first time, use `git push -u origin main` to set up tracking so future pushes just need `git push`.',
        'answers': ['git push origin main', 'git push -u origin main'],
    },
    {
        'level': 2, 'category': 'remote', 'difficulty': 'easy', 'points': 12,
        'scenario': 'Your teammate just merged a PR. You want to download their latest changes from the main branch on GitHub into your local main branch.',
        'hint': 'You are "pulling" from "origin" the "main" branch.',
        'explanation': '`git pull origin main` fetches AND merges changes from the remote main branch into your current branch. Always pull before starting work to avoid conflicts later. It is fetch + merge in one command.',
        'answers': ['git pull origin main', 'git pull'],
    },
    {
        'level': 2, 'category': 'remote', 'difficulty': 'easy', 'points': 12,
        'scenario': 'You want to check all remote connections your repo has — their names and the exact URLs they point to.',
        'hint': 'The flag -v means "verbose".',
        'explanation': '`git remote -v` lists all remotes with their fetch and push URLs. This is how you verify your remote is set up correctly. If you see the right URL next to "origin", you are connected.',
        'answers': ['git remote -v'],
    },

    # ── LEVEL 3 · Branching ───────────────────────────────────────────
    {
        'level': 3, 'category': 'branching', 'difficulty': 'easy', 'points': 15,
        'scenario': 'You want to see the list of all branches in your local repository. What command shows them, with a star on the current one?',
        'hint': 'Just the word "branch" is enough.',
        'explanation': '`git branch` lists all local branches. The one with * is where you currently are. Use `git branch -r` for remote branches, or `git branch -a` to see both local and remote.',
        'answers': ['git branch'],
    },
    {
        'level': 3, 'category': 'branching', 'difficulty': 'easy', 'points': 15,
        'scenario': 'You need to start working on a new login feature. You want to create a branch called "feature/login" AND switch to it in a single command.',
        'hint': 'Use checkout with -b flag, or the newer switch -c.',
        'explanation': '`git checkout -b feature/login` creates a new branch and immediately switches to it. The -b flag means "create". Newer Git also supports `git switch -c feature/login`. Always create a new branch for every piece of work.',
        'answers': ['git checkout -b feature/login', 'git switch -c feature/login'],
    },
    {
        'level': 3, 'category': 'branching', 'difficulty': 'easy', 'points': 15,
        'scenario': 'You want to switch to an existing branch called "develop". What command moves you there?',
        'hint': 'The branch already exists — no need to create it.',
        'explanation': '`git checkout develop` switches your working directory to the develop branch. Use `git switch develop` in newer Git versions. Always check `git status` first to make sure you have no uncommitted changes.',
        'answers': ['git checkout develop', 'git switch develop'],
    },
    {
        'level': 3, 'category': 'branching', 'difficulty': 'easy', 'points': 15,
        'scenario': 'Your branch "feature/old-navbar" was merged into main months ago. You want to delete it locally.',
        'hint': 'Use the -d flag (lowercase = safe delete).',
        'explanation': '`git branch -d feature/old-navbar` deletes a branch that has already been merged. Git will refuse if it has unmerged changes (protection). Use `-D` (capital) to force-delete unmerged branches — dangerous, use carefully.',
        'answers': ['git branch -d feature/old-navbar'],
    },
    {
        'level': 3, 'category': 'branching', 'difficulty': 'easy', 'points': 15,
        'scenario': 'You want to see every branch — both the ones on your computer AND the ones on GitHub (remote tracking branches).',
        'hint': 'The flag -a means "all".',
        'explanation': '`git branch -a` shows local and remote branches. Remote branches appear as "remotes/origin/branchname". This is how you see what others are working on without pulling everything.',
        'answers': ['git branch -a'],
    },

    # ── LEVEL 4 · Staging & Diff ──────────────────────────────────────
    {
        'level': 4, 'category': 'staging', 'difficulty': 'medium', 'points': 18,
        'scenario': 'You changed some files but have NOT staged them yet. You want to see the exact line-by-line differences of what changed.',
        'hint': 'Just "diff" — no extra flags needed for unstaged changes.',
        'explanation': '`git diff` shows changes in your working directory that are NOT yet staged. Red lines were removed, green lines were added. Use this before `git add` to review your changes.',
        'answers': ['git diff'],
    },
    {
        'level': 4, 'category': 'staging', 'difficulty': 'medium', 'points': 18,
        'scenario': 'You already ran `git add`. Now you want to see what is staged and will be included in your next commit.',
        'hint': 'Add --staged or --cached flag to diff.',
        'explanation': '`git diff --staged` shows changes between your last commit and what is currently staged. Use this to review exactly what you are about to commit. `--cached` is an alias that does the same thing.',
        'answers': ['git diff --staged', 'git diff --cached'],
    },
    {
        'level': 4, 'category': 'staging', 'difficulty': 'medium', 'points': 18,
        'scenario': 'You only want to stage one specific file — "src/pipeline.py" — and leave all other changed files unstaged.',
        'hint': 'Provide the specific file path after `git add`.',
        'explanation': '`git add src/pipeline.py` stages only that one file. This is the professional approach — stage files intentionally, not blindly. Lets you split work into logical commits rather than one huge messy commit.',
        'answers': ['git add src/pipeline.py'],
    },
    {
        'level': 4, 'category': 'staging', 'difficulty': 'medium', 'points': 18,
        'scenario': 'You staged "config.py" by mistake. You want to UNSTAGE it (remove from staging area) without losing the changes in the file.',
        'hint': 'Think "restore" the staged state.',
        'explanation': '`git restore --staged config.py` removes the file from the staging area but leaves your edits in place. The file still shows as "modified" — just no longer staged. In older Git: `git reset HEAD config.py`.',
        'answers': ['git restore --staged config.py', 'git reset HEAD config.py'],
    },
    {
        'level': 4, 'category': 'staging', 'difficulty': 'medium', 'points': 18,
        'scenario': 'You made a mess of "pipeline.py" and want to throw away ALL your changes to it and go back to the last committed version. This action is permanent.',
        'hint': 'Use restore without the --staged flag.',
        'explanation': '`git restore pipeline.py` discards all uncommitted changes to that file and restores the last committed version. WARNING: This cannot be undone — your changes are gone. In older Git: `git checkout -- pipeline.py`.',
        'answers': ['git restore pipeline.py', 'git checkout -- pipeline.py'],
    },

    # ── LEVEL 5 · Merging ─────────────────────────────────────────────
    {
        'level': 5, 'category': 'merging', 'difficulty': 'medium', 'points': 20,
        'scenario': 'You are on the main branch. You want to merge the completed work from "feature/payment" into main.',
        'hint': 'You merge INTO your current branch.',
        'explanation': '`git merge feature/payment` merges the specified branch into whichever branch you are currently on. If there are no conflicts, Git auto-completes. If there are conflicts, you must resolve them manually then commit.',
        'answers': ['git merge feature/payment'],
    },
    {
        'level': 5, 'category': 'merging', 'difficulty': 'medium', 'points': 20,
        'scenario': 'You started a merge but it is getting complicated and you just want to cancel it and go back to before you started merging.',
        'hint': 'Abort the merge operation entirely.',
        'explanation': '`git merge --abort` cancels an in-progress merge and restores your branch to the state before the merge started. Only works while a merge is in progress (while conflicts exist unresolved). Safe to use when things go wrong.',
        'answers': ['git merge --abort'],
    },
    {
        'level': 5, 'category': 'merging', 'difficulty': 'medium', 'points': 20,
        'scenario': 'You are in the middle of a merge conflict. Which command shows you ONLY the names of files that have conflicts right now?',
        'hint': 'git diff with --name-only flag.',
        'explanation': '`git diff --name-only` shows just filenames with differences, not the full diff. During a merge this is useful to quickly see which files need your attention without being overwhelmed by all the conflict markers.',
        'answers': ['git diff --name-only'],
    },
    {
        'level': 5, 'category': 'merging', 'difficulty': 'medium', 'points': 20,
        'scenario': 'You want to see your commit history displayed as a visual ASCII graph showing branches and merges.',
        'hint': 'Combine log with --oneline and --graph flags.',
        'explanation': '`git log --oneline --graph` shows a compact visual representation of branch/merge history. Add `--decorate` to also show branch and tag names. This is the best way to understand the structure of your repo history.',
        'answers': ['git log --oneline --graph', 'git log --oneline --graph --decorate', 'git log --graph --oneline'],
    },
    {
        'level': 5, 'category': 'merging', 'difficulty': 'medium', 'points': 20,
        'scenario': 'After manually fixing a merge conflict in a file, what is the next step to tell Git the conflict is resolved and finalize the merge?',
        'hint': 'Stage the resolved file first.',
        'explanation': 'After resolving conflicts (removing the <<<, ===, >>> markers and keeping the right code), run `git add .` to tell Git the conflicts are fixed, then `git commit` to finalize the merge. Git creates a "merge commit" automatically.',
        'answers': ['git add .', 'git add . && git commit'],
    },

    # ── LEVEL 6 · Stash ───────────────────────────────────────────────
    {
        'level': 6, 'category': 'stash', 'difficulty': 'medium', 'points': 20,
        'scenario': 'You are in the middle of coding and your manager asks you to urgently fix a bug on another branch. You have unfinished changes you are NOT ready to commit. How do you temporarily save them?',
        'hint': 'Think of "stashing" valuables temporarily.',
        'explanation': '`git stash` saves your uncommitted changes (both staged and unstaged) to a temporary storage stack and reverts your working directory to the last commit. You can then switch branches freely and come back to your work later.',
        'answers': ['git stash', 'git stash push'],
    },
    {
        'level': 6, 'category': 'stash', 'difficulty': 'medium', 'points': 20,
        'scenario': 'You want to stash your changes and add a label "WIP: S3 connection refactor" so you remember what the stash is about.',
        'hint': 'Use push -m to add a message.',
        'explanation': '`git stash push -m "WIP: S3 connection refactor"` saves your work with a descriptive label. This is the professional approach — when you have multiple stashes, clear names are essential. The label shows in `git stash list`.',
        'answers': ['git stash push -m "WIP: S3 connection refactor"', "git stash push -m 'WIP: S3 connection refactor'"],
    },
    {
        'level': 6, 'category': 'stash', 'difficulty': 'medium', 'points': 20,
        'scenario': 'You stashed work multiple times. Now you want to see a list of all your saved stashes.',
        'hint': 'Add "list" after git stash.',
        'explanation': '`git stash list` shows all stashes with their index numbers (stash@{0}, stash@{1}...). The most recent is always stash@{0}. Each entry shows the branch it was saved from and the message if you provided one.',
        'answers': ['git stash list'],
    },
    {
        'level': 6, 'category': 'stash', 'difficulty': 'medium', 'points': 20,
        'scenario': 'You want to bring back your most recently stashed work AND remove it from the stash list at the same time.',
        'hint': '"Pop" removes from the stack after applying.',
        'explanation': '`git stash pop` applies the most recent stash (stash@{0}) to your working directory and removes it from the stash list. If you want to apply without removing, use `git stash apply`. Pop = apply + delete.',
        'answers': ['git stash pop'],
    },
    {
        'level': 6, 'category': 'stash', 'difficulty': 'medium', 'points': 20,
        'scenario': 'You have 3 stashes. You want to apply the one at index 2 (stash@{2}) without removing it from the stash list.',
        'hint': 'Use "apply" not "pop", and specify the stash index.',
        'explanation': '`git stash apply stash@{2}` applies a specific stash without removing it. Use this when you are not sure the apply will work cleanly — if something goes wrong, the stash is still saved. Use `git stash drop stash@{2}` to delete it after.',
        'answers': ['git stash apply stash@{2}'],
    },

    # ── LEVEL 7 · Undoing Changes ─────────────────────────────────────
    {
        'level': 7, 'category': 'undoing', 'difficulty': 'hard', 'points': 25,
        'scenario': 'You committed too early. You want to undo the last commit but KEEP all the changes in your working directory so you can recommit properly.',
        'hint': '--soft keeps your changes staged.',
        'explanation': '`git reset --soft HEAD~1` moves the branch pointer back by 1 commit but leaves all your changes staged. Your work is not lost — you can adjust and recommit. HEAD~1 means "one commit before HEAD". HEAD~2 means two commits back.',
        'answers': ['git reset --soft HEAD~1'],
    },
    {
        'level': 7, 'category': 'undoing', 'difficulty': 'hard', 'points': 25,
        'scenario': 'You committed broken code by mistake. You want to completely undo the last commit AND delete all those changes permanently. You accept the data is gone.',
        'hint': '--hard is destructive. It deletes changes.',
        'explanation': '`git reset --hard HEAD~1` moves the branch pointer back AND deletes all changes from that commit. WARNING: This is irreversible for local changes. Only use on commits not yet pushed to shared branches. If pushed, use `git revert` instead.',
        'answers': ['git reset --hard HEAD~1'],
    },
    {
        'level': 7, 'category': 'undoing', 'difficulty': 'hard', 'points': 25,
        'scenario': 'You pushed a bad commit to a shared branch. You cannot rewrite history. You need to safely undo it by creating a NEW commit that reverses the changes.',
        'hint': 'Revert = safe undo that adds a new commit.',
        'explanation': '`git revert HEAD` creates a new commit that is the exact opposite of the last commit — it undoes those changes safely. This is the ONLY safe way to undo changes that are already on a shared remote branch. Never use reset on shared branches.',
        'answers': ['git revert HEAD', 'git revert HEAD --no-edit'],
    },
    {
        'level': 7, 'category': 'undoing', 'difficulty': 'hard', 'points': 25,
        'scenario': 'A disaster happened — you lost commits, deleted a branch, or messed up a rebase. This emergency command shows you a log of EVERY action Git has done, including deleted history.',
        'hint': 'Think "reference log" — the ultimate recovery tool.',
        'explanation': '`git reflog` shows every operation that moved HEAD — commits, resets, checkouts, merges — for the last 90 days. Even deleted commits exist here. Copy the hash of what you want to recover and run `git checkout <hash>` or `git reset --hard <hash>`.',
        'answers': ['git reflog'],
    },
    {
        'level': 7, 'category': 'undoing', 'difficulty': 'hard', 'points': 25,
        'scenario': 'You accidentally ran `git add .` and staged everything. You want to unstage ALL files at once without losing any changes.',
        'hint': 'Restore staged state for all files using a dot.',
        'explanation': '`git restore --staged .` unstages all staged files at once. The dot means "all files". Your actual file contents are unchanged — only the staging area is cleared. Then you can carefully stage just what you want.',
        'answers': ['git restore --staged .', 'git reset HEAD'],
    },

    # ── LEVEL 8 · Rebase & Advanced ───────────────────────────────────
    {
        'level': 8, 'category': 'advanced', 'difficulty': 'hard', 'points': 30,
        'scenario': 'You have been working on "feature/api" for a week. Main has moved forward with new commits. You want to replay your feature commits on TOP of the latest main to get a clean, linear history.',
        'hint': 'You are "rebasing" your branch onto main.',
        'explanation': '`git rebase main` takes all your feature branch commits and replays them on top of the latest main commit. This creates a clean linear history without merge commits. NEVER rebase branches others are using — it rewrites history.',
        'answers': ['git rebase main'],
    },
    {
        'level': 8, 'category': 'advanced', 'difficulty': 'hard', 'points': 30,
        'scenario': 'You made 4 messy work-in-progress commits on your branch. Before opening a PR, you want to combine them into 1 clean commit and possibly reword the messages.',
        'hint': 'Interactive rebase to edit the last 4 commits.',
        'explanation': '`git rebase -i HEAD~4` opens an interactive editor showing your last 4 commits. You can squash (combine), fixup (combine silently), reword (rename), drop, or reorder commits. This is how professionals clean up messy work before code review.',
        'answers': ['git rebase -i HEAD~4'],
    },
    {
        'level': 8, 'category': 'advanced', 'difficulty': 'hard', 'points': 30,
        'scenario': 'A fix was merged to another branch last week with hash "abc1234". You need ONLY that one specific commit applied to your current branch — not the whole branch.',
        'hint': 'Pick just that one specific commit "cherry".',
        'explanation': '`git cherry-pick abc1234` applies the changes from a specific commit to your current branch as a new commit. Useful when you need a fix from one branch without merging the entire branch. The hash comes from `git log --oneline`.',
        'answers': ['git cherry-pick abc1234'],
    },
    {
        'level': 8, 'category': 'advanced', 'difficulty': 'hard', 'points': 30,
        'scenario': 'You want to download all changes from the remote (GitHub) but NOT apply them to your local branches yet. You just want to see what changed.',
        'hint': 'Fetch downloads, pull downloads + merges.',
        'explanation': '`git fetch --all` downloads all branches and commits from all remotes without modifying your local branches. Use `git diff origin/main` afterwards to see what changed. Then decide if you want to merge. Safer than `git pull` when you want to inspect first.',
        'answers': ['git fetch --all', 'git fetch', 'git fetch origin'],
    },
    {
        'level': 8, 'category': 'advanced', 'difficulty': 'hard', 'points': 30,
        'scenario': 'You created a new local branch "feature/dashboard" and want to push it to GitHub for the FIRST TIME and also set up automatic tracking so future `git push` just works.',
        'hint': 'The -u flag sets the upstream.',
        'explanation': '`git push -u origin feature/dashboard` pushes the branch AND sets the upstream tracking. After this, you only need `git push` or `git pull` without specifying the remote and branch. -u is short for --set-upstream.',
        'answers': ['git push -u origin feature/dashboard'],
    },

    # ── LEVEL 9 · Tags & Inspection ───────────────────────────────────
    {
        'level': 9, 'category': 'tags', 'difficulty': 'hard', 'points': 30,
        'scenario': 'Your code is stable and ready for deployment. You want to mark this exact commit as version "v2.0.0" with a full annotation and the message "Production release".',
        'hint': 'Annotated tags use -a flag and -m for message.',
        'explanation': '`git tag -a v2.0.0 -m "Production release"` creates an annotated tag with metadata (tagger, date, message). Annotated tags are preferred over lightweight tags for releases. They show up in `git log --decorate` and are better for tooling.',
        'answers': ['git tag -a v2.0.0 -m "Production release"', 'git tag -a v2.0.0 -m \'Production release\''],
    },
    {
        'level': 9, 'category': 'tags', 'difficulty': 'hard', 'points': 30,
        'scenario': 'You created tags locally. They are NOT on GitHub yet. Push all of them to GitHub.',
        'hint': 'Tags need to be pushed separately — a regular push does not include them.',
        'explanation': '`git push origin --tags` pushes all local tags to the remote. Regular `git push` does NOT push tags automatically. To push one specific tag: `git push origin v2.0.0`. Tags on GitHub appear in the "Releases" section.',
        'answers': ['git push origin --tags', 'git push --tags'],
    },
    {
        'level': 9, 'category': 'inspection', 'difficulty': 'hard', 'points': 30,
        'scenario': 'Someone introduced a bug in "models/etl.py" weeks ago. You want to see which developer changed each specific LINE of the file and which commit they belong to.',
        'hint': 'Git "blames" a file to show line-by-line authorship.',
        'explanation': '`git blame models/etl.py` shows each line of the file annotated with the commit hash, author, and date of the last change. This is how you find who broke something and when. Not for blame culture — for understanding context.',
        'answers': ['git blame models/etl.py'],
    },
    {
        'level': 9, 'category': 'inspection', 'difficulty': 'hard', 'points': 30,
        'scenario': 'A bug was introduced somewhere between last week (commit abc1111) and today. You want to use Git\'s automated binary search to find the exact commit that broke things.',
        'hint': 'Start the binary search session.',
        'explanation': '`git bisect start` begins an interactive binary search through your commit history. Then: `git bisect bad` (marks current as broken), `git bisect good abc1111` (marks last good commit). Git checks out the middle commit — you test it, mark good or bad, repeat until found.',
        'answers': ['git bisect start'],
    },
    {
        'level': 9, 'category': 'inspection', 'difficulty': 'hard', 'points': 30,
        'scenario': 'You want to see a compact summary of the most recent commit — just the files changed and how many lines were added/removed.',
        'hint': 'Use git show with --stat flag.',
        'explanation': '`git show --stat` shows the last commit\'s metadata and a summary of which files changed with line counts. Without --stat, `git show` shows the full diff. Add a commit hash like `git show abc1234 --stat` to inspect any specific commit.',
        'answers': ['git show --stat', 'git show --stat HEAD'],
    },

    # ── LEVEL 10 · Git Master ─────────────────────────────────────────
    {
        'level': 10, 'category': 'master', 'difficulty': 'expert', 'points': 40,
        'scenario': 'Your rebase went wrong and Git is stuck. You want to cancel the rebase completely and return to the state before you started it.',
        'hint': 'Abort the rebase — same pattern as merge abort.',
        'explanation': '`git rebase --abort` cancels an in-progress rebase and restores your branch to exactly where it was before `git rebase` was run. Always run this when a rebase gets messy rather than trying to fix it mid-flight.',
        'answers': ['git rebase --abort'],
    },
    {
        'level': 10, 'category': 'master', 'difficulty': 'expert', 'points': 40,
        'scenario': 'Your feature branch diverged from the remote after you did a rebase locally. You need to force-push but you want to do it safely — making sure nobody else pushed to the remote branch since your last fetch.',
        'hint': 'Use force-with-lease, not plain force.',
        'explanation': '`git push --force-with-lease` is a safer force push. It checks that the remote branch has not been updated since you last fetched. If someone else pushed, it refuses the force-push and protects their work. NEVER use `git push --force` on shared branches.',
        'answers': ['git push --force-with-lease'],
    },
    {
        'level': 10, 'category': 'master', 'difficulty': 'expert', 'points': 40,
        'scenario': 'Your working directory has untracked files and empty folders cluttering things up. You want to delete ALL of them permanently (not tracked files — just the new untracked ones).',
        'hint': '-f for force, -d for directories.',
        'explanation': '`git clean -fd` removes all untracked files (-f) and directories (-d) from your working tree. Run `git clean -nfd` first (dry run) to see what WOULD be deleted before actually deleting. This is permanent — deleted files do not go to trash.',
        'answers': ['git clean -fd', 'git clean -f -d'],
    },
    {
        'level': 10, 'category': 'master', 'difficulty': 'expert', 'points': 40,
        'scenario': 'You maintain a monorepo and want to add an external Git repository as a subdirectory inside your project, keeping its history separate.',
        'hint': 'Git has a feature for embedding repos inside repos.',
        'explanation': '`git submodule add <url>` adds another Git repo as a subdirectory. The parent repo tracks the submodule at a specific commit. Submodules are common in large projects with shared libraries. After cloning a project with submodules, run `git submodule update --init`.',
        'answers': ['git submodule add'],
    },
    {
        'level': 10, 'category': 'master', 'difficulty': 'expert', 'points': 40,
        'scenario': 'You want to permanently remove a file containing a secret key from ALL commit history — not just the latest commit. This is an emergency data cleanup.',
        'hint': 'This requires rewriting history with a filter.',
        'explanation': '`git filter-branch --tree-filter "rm -f secrets.txt" HEAD` or the modern `git filter-repo --path secrets.txt --invert-paths` rewrites every commit to remove the file. After this, force-push all branches and rotate your exposed credentials immediately. Prevention: always use .gitignore.',
        'answers': ['git filter-branch --tree-filter "rm -f secrets.txt" HEAD', 'git filter-repo --path secrets.txt --invert-paths'],
    },
]

ERROR_CHALLENGES = [
    {
        'error_type': 'push_rejected',
        'error_message': "error: failed to push some refs — Updates were rejected because the remote contains work that you do not have locally",
        'scenario': 'You tried to push but got "rejected" because GitHub has commits you do not have. What is the SAFE way to resolve this before pushing?',
        'correct_command': 'git pull --rebase origin main',
        'explanation': '`git pull --rebase origin main` downloads the remote commits and replays YOUR commits on top of them, keeping a clean linear history. Alternatively use `git pull origin main` (merge approach). Then you can push normally.',
    },
    {
        'error_type': 'detached_head',
        'error_message': "You are in 'detached HEAD' state. You can look around, make experimental changes and commit them, but they will be lost if you do not create a branch.",
        'scenario': 'Git says you are in "detached HEAD" state. You want to get back to the main branch safely.',
        'correct_command': 'git switch main',
        'explanation': '"Detached HEAD" means you checked out a specific commit instead of a branch. Any commits you make here are orphaned. Run `git switch main` or `git checkout main` to return to the branch. If you made commits in detached state that you want to keep, run `git switch -c new-branch-name` FIRST.',
    },
    {
        'error_type': 'merge_conflict',
        'error_message': "CONFLICT (content): Merge conflict in src/pipeline.py — Automatic merge failed; fix conflicts and then commit the result.",
        'scenario': 'You hit a merge conflict in "src/pipeline.py". After you manually fix the conflict markers in the file, what do you run to finalize the merge?',
        'correct_command': 'git add src/pipeline.py',
        'explanation': 'After opening the file, removing the <<<, ===, >>> markers, and keeping the correct code — run `git add src/pipeline.py` to tell Git it is resolved, then `git commit` to create the merge commit. Never commit conflict markers in the file.',
    },
    {
        'error_type': 'not_a_repo',
        'error_message': "fatal: not a git repository (or any of the parent directories): .git",
        'scenario': 'You ran a git command and got "fatal: not a git repository". What do you do to fix this (assuming you want to start a new repo here)?',
        'correct_command': 'git init',
        'explanation': 'This error means you are in a directory that Git is not tracking. Either you need to `cd` into the right directory, or you need to `git init` to create a new repo here. Always check you are in the right folder with `pwd` before running Git commands.',
    },
    {
        'error_type': 'nothing_to_commit',
        'error_message': "nothing to commit, working tree clean",
        'scenario': 'Git says "nothing to commit, working tree clean." You forgot to stage your files before trying to commit. What should you have run first?',
        'correct_command': 'git add .',
        'explanation': 'You must stage files with `git add` before committing. "Nothing to commit" means either: nothing changed, or you forgot `git add`. Run `git status` first to see the state of your files, then `git add .` or `git add filename` to stage them.',
    },
    {
        'error_type': 'already_up_to_date',
        'error_message': "Already up to date. — But your push still gets rejected.",
        'scenario': 'git pull says "Already up to date" but you still cannot push. This usually means you are on the wrong branch. What command shows you which branch you are on?',
        'correct_command': 'git branch',
        'explanation': 'Run `git branch` to see which branch you are on (starred). You might be on a local branch that is not tracking the remote one correctly. Check `git remote -v` and `git branch -vv` to see tracking configuration.',
    },
]

def setup():
    print("Connecting to MySQL...")
    conn = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
    c = conn.cursor()

    print("Creating database git_game...")
    c.execute("CREATE DATABASE IF NOT EXISTS git_game CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    c.execute("USE git_game")

    print("Creating tables...")
    c.execute("""
        CREATE TABLE IF NOT EXISTS challenges (
            id INT AUTO_INCREMENT PRIMARY KEY,
            level INT NOT NULL,
            category VARCHAR(50),
            difficulty VARCHAR(20),
            points INT DEFAULT 10,
            scenario TEXT NOT NULL,
            hint TEXT,
            explanation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS challenge_answers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            challenge_id INT NOT NULL,
            answer TEXT NOT NULL,
            is_primary BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (challenge_id) REFERENCES challenges(id) ON DELETE CASCADE
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) DEFAULT 'Git Commander',
            total_score INT DEFAULT 0,
            rank_percentage DECIMAL(5,2) DEFAULT 0.00,
            current_level INT DEFAULT 1,
            streak INT DEFAULT 0,
            max_streak INT DEFAULT 0,
            challenges_completed INT DEFAULT 0,
            challenges_attempted INT DEFAULT 0,
            hints_used INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS attempt_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            challenge_id INT NOT NULL,
            user_input TEXT,
            is_correct TINYINT(1) DEFAULT 0,
            points_earned INT DEFAULT 0,
            hint_used TINYINT(1) DEFAULT 0,
            attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (challenge_id) REFERENCES challenges(id)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS error_challenges (
            id INT AUTO_INCREMENT PRIMARY KEY,
            error_type VARCHAR(100) UNIQUE,
            error_message TEXT,
            scenario TEXT,
            correct_command TEXT,
            explanation TEXT,
            unlocked TINYINT(1) DEFAULT 0,
            times_encountered INT DEFAULT 0
        )
    """)

    # Seed challenges
    c.execute("SELECT COUNT(*) as cnt FROM challenges")
    if c.fetchone()['cnt'] == 0:
        print(f"Seeding {len(CHALLENGES)} challenges...")
        for ch in CHALLENGES:
            c.execute("""
                INSERT INTO challenges (level, category, difficulty, points, scenario, hint, explanation)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (ch['level'], ch['category'], ch['difficulty'], ch['points'],
                  ch['scenario'], ch['hint'], ch['explanation']))
            cid = c.lastrowid
            for i, ans in enumerate(ch['answers']):
                c.execute("INSERT INTO challenge_answers (challenge_id, answer, is_primary) VALUES (%s, %s, %s)",
                          (cid, ans, i == 0))
    else:
        print("Challenges already seeded. Skipping.")

    # Seed error challenges
    c.execute("SELECT COUNT(*) as cnt FROM error_challenges")
    if c.fetchone()['cnt'] == 0:
        print(f"Seeding {len(ERROR_CHALLENGES)} error challenges...")
        for ec in ERROR_CHALLENGES:
            c.execute("""
                INSERT INTO error_challenges (error_type, error_message, scenario, correct_command, explanation)
                VALUES (%s, %s, %s, %s, %s)
            """, (ec['error_type'], ec['error_message'], ec['scenario'],
                  ec['correct_command'], ec['explanation']))
    else:
        print("Error challenges already seeded. Skipping.")

    # Create default user profile
    c.execute("SELECT COUNT(*) as cnt FROM user_profile")
    if c.fetchone()['cnt'] == 0:
        c.execute("INSERT INTO user_profile (username) VALUES ('Git Commander')")
        print("Created user profile.")

    conn.commit()
    conn.close()
    print("\n✅ Database setup complete!")
    print("Now run: python app.py")
    print("Then open: http://localhost:5000")

if __name__ == '__main__':
    setup()
