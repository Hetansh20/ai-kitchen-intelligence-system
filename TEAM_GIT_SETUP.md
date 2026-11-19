# Team Git & GitHub Authentication Guide

This document defines the team branch ownership, local Git identity configuration, and GitHub authentication rules for the **AI-Powered Kitchen Intelligence System**.

---

## 1. Team Roster & Assigned Branches

| Team Member | GitHub Username | Commit Email | Assigned Branch | Primary Responsibility |
| :--- | :--- | :--- | :--- | :--- |
| **Hetansh** (Owner) | `Hetansh20` | `hetanshshah2111@gmail.com` | `hetansh` | Flask backend, REST APIs, database models & schema, calculations |
| **Viraj** | `Viraj1811` | `virajvaghasiya1811@gmail.com` | `viraj` | ML model training, preprocessing, Random Forest regressor, XAI |
| **Bhavin** | `bhavin9631` | `muchhalabhavin@gmail.com` | `bhavin` | React frontend, UI/UX dashboard, Tailwind CSS, charts, theme engine |

---

## 2. Repository Owner Setup: Adding Collaborators

Because `Hetansh20` is the repository owner, team members need **Write permission** to push to their respective branches.

1. Go to: **[https://github.com/Hetansh20/ai-kitchen-intelligence-system/settings/access](https://github.com/Hetansh20/ai-kitchen-intelligence-system/settings/access)**
2. Click **Add people**.
3. Enter `Viraj1811` and click **Add Viraj1811 to this repository**.
4. Enter `bhavin9631` and click **Add bhavin9631 to this repository**.
5. Viraj and Bhavin must accept the invitation via their GitHub email or notification.

---

## 3. Team Member Machine Setup

Each team member works on their own computer with their own authenticated account.

### Step A: Clone the Repository
```bash
git clone https://github.com/Hetansh20/ai-kitchen-intelligence-system.git
cd ai-kitchen-intelligence-system
```

### Step B: Checkout Your Branch & Set Local Identity
Run the commands corresponding to your identity (**never overwrite global config**):

#### For Hetansh:
```bash
git checkout hetansh
git config --local user.name "Hetansh20"
git config --local user.email "hetanshshah2111@gmail.com"
```

#### For Viraj:
```bash
git checkout viraj
git config --local user.name "Viraj1811"
git config --local user.email "virajvaghasiya1811@gmail.com"
```

#### For Bhavin:
```bash
git checkout bhavin
git config --local user.name "bhavin9631"
git config --local user.email "muchhalabhavin@gmail.com"
```

---

## 4. GitHub Authentication vs Git Identity

> [!IMPORTANT]
> `git config user.name` sets the **author label** on commits.  
> It does **NOT** authenticate you to push to GitHub. GitHub authentication controls whether GitHub accepts your push.

### How to Authenticate on Your Computer

#### Option 1: Git Credential Manager (Default on Windows/macOS)
When you run `git push origin <your-branch>` for the first time, a browser window will open asking you to sign in to GitHub:
- Log in with your **own** GitHub account.
- Once authenticated, Windows Credential Manager securely caches your token.

#### Option 2: Switching Accounts in Git Credential Manager
If a different account is already cached on your machine:
```bash
# On Windows, clear cached GitHub credentials:
cmdkey /delete:LegacyGeneric:target=git:https://github.com
```
Then run `git push origin <your-branch>` to trigger a fresh login prompt.

#### Option 3: Using Personal Access Token (PAT)
1. Go to **GitHub Settings → Developer Settings → Personal access tokens → Tokens (classic)**.
2. Generate token with `repo` scope.
3. Use your GitHub username and the PAT as the password when prompted.

---

## 5. Pre-Push Verification Checklist

Before pushing any commit, run this quick check:

```bash
# 1. Verify current branch is YOUR branch (not main)
git branch --show-current

# 2. Verify local author name and email
git config --local user.name
git config --local user.email

# 3. Check what commits are about to be pushed
git status
git log -n 1 --oneline

# 4. Push ONLY to your assigned branch
git push origin <your-branch>
```

---

## 6. Submitting Work to `main`
When a feature or task is complete and verified:
1. Push all commits to your personal branch (`viraj`, `bhavin`, or `hetansh`).
2. Go to **https://github.com/Hetansh20/ai-kitchen-intelligence-system/pulls**.
3. Click **New pull request**.
4. Set base: `main` ← compare: `your-branch`.
5. Submit the PR for review and merging into `main`.
