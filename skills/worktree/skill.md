---
description: "Create, manage, and synchronize git worktrees for running parallel Claude Code sessions. Use this skill when: (1) creating isolated worktrees for parallel development, (2) checking status across all worktrees, (3) pulling changes from another branch, (4) pushing changes to main, (5) removing completed worktrees, or any git worktree operations (examples: 'create worktree', 'worktree status', 'parallel branches', 'multiple Claude sessions')."
argument-hint: "[create|status|pull|pull-all|push|remove] [name]"
---

# Git Worktree Management

Manage git worktrees for parallel Claude Code sessions.

## Command Routing

**Arguments received:** `$ARGUMENTS`

**Route based on arguments (check in order):**
1. If empty/blank → Show **Help** section
2. If `create <name>` → Execute **Create Worktree** section
3. If `status` → Execute **Status** section
4. If `pull-all` → Execute **Pull All** section
5. If `pull` (no argument) → Execute **Pull Interactive** section
6. If `pull <branch>` → Execute **Pull** section
7. If `push` → Execute **Push** section
8. If `remove <name>` → Execute **Remove Worktree** section
9. Otherwise → Show **Help** section with "Unknown command" note

## Help

```
/worktree - Manage git worktrees for parallel Claude Code sessions

Commands:
  create <name>    Create new worktree as sibling directory
  status           Show all worktrees and their state
  pull             Interactive: choose which branch(es) to pull
  pull <source>    Pull changes from a specific branch into current
  pull-all         Pull changes from ALL other worktrees into current
  push             Push current branch changes into main
  remove <name>    Remove worktree (optionally delete branch)

Mental model:
  "pull" brings changes INTO your current branch (git merge <source>)
  "push" sends your changes TO main (git checkout main && git merge <yours>)

Workflows:
  From ./folder (worktree main):
    /worktree pull feature-b     # pulls feature-b changes into main

  From ../folder-feature-b (worktree feature-b):
    /worktree pull main          # pulls main changes into feature-b
    /worktree push               # merges feature-b into main locally
    git push                     # pushes feature-b to GitHub

  From any worktree:
    git push --all               # pushes all worktrees to GitHub

Note: All worktrees share the same local repo.
      Commits are instantly available to pull - no git push needed between worktrees.

Examples:
  /worktree create feature-auth
  /worktree pull              # interactive selection
  /worktree pull main         # pull from specific branch
  /worktree pull-all          # merge all other worktrees
  /worktree push
  /worktree remove feature-auth
```

---

## Create Worktree

**Extract name from:** `$ARGUMENTS` (after "create ")

**Steps:**

1. **Validate name** - no spaces, valid git branch name
2. **Get project name:** `basename $(git rev-parse --show-toplevel)`
3. **Check branch doesn't exist:** `git show-ref --verify --quiet refs/heads/<name>`
4. **Create worktree:**
   ```bash
   git worktree add ../<project>-<name> -b <name>
   ```
5. **Install guardrails and pty-mcp in new worktree:**
   ```bash
   cd ../<project>-<name> && make install-guardrails && make install-pty-mcp
   ```
6. **Report success:**
   ```
   Created worktree: ../<project>-<name>
   Branch: <name>

   Next steps:
   1. Open new terminal: cd ../<project>-<name>
   2. Start Claude: claude
   3. Work independently in this worktree
   ```

---

## Status

**Steps:**

1. **List worktrees:** `git worktree list`
2. **For each worktree, gather:**
   - Path
   - Branch name
   - Uncommitted changes: `git -C <path> status --porcelain | wc -l`
3. **Present as table:**
   ```
   | Path | Branch | Changes |
   |------|--------|---------|
   | /path/to/main | main | 0 |
   | /path/to/feature | feature-x | 3 |
   ```

---

## Pull

**Extract source from:** `$ARGUMENTS` (after "pull ")

**Steps:**

1. **Validate source branch exists:** `git show-ref --verify --quiet refs/heads/<source>`
2. **Show current branch:** `git branch --show-current`
3. **Merge:**
   ```bash
   git merge <source>
   ```
4. **Report result** - success or conflicts to resolve

**Mental model:** This IS a merge - you're bringing changes FROM source INTO current.

---

## Pull Interactive

**Triggered by:** `pull` with no arguments

**Steps:**

1. **Get current branch:** `git branch --show-current`
2. **List branches with active worktrees (excluding current):**
   ```bash
   git worktree list --porcelain | grep '^branch' | sed 's|branch refs/heads/||' | grep -v <current>
   ```
3. **Build options for AskUserQuestion:**
   - First option: "All worktrees" (meta-option)
   - Then each worktree branch as individual option
4. **Use AskUserQuestion:**
   ```
   question: "Which branch(es) do you want to pull into <current>?"
   header: "Pull from"
   multiSelect: true
   options:
     - label: "All worktrees"
       description: "Merge all other worktree branches into current (sequential)"
     - label: "<branch1>"
       description: "Merge <branch1> into <current>"
     - label: "<branch2>"
       description: "Merge <branch2> into <current>"
   ```
5. **Execute based on selection:**
   - If "All worktrees" selected → Go to **Pull All** logic
   - Otherwise → Merge each selected branch sequentially

---

## Pull All

**Triggered by:** `pull-all` OR "All worktrees" selection from interactive

**Steps:**

1. **Get current branch:** `git branch --show-current`
2. **List branches with active worktrees (excluding current):**
   ```bash
   git worktree list --porcelain | grep '^branch' | sed 's|branch refs/heads/||' | grep -v <current>
   ```
3. **For each worktree branch, merge sequentially:**
   ```bash
   git merge <branch>
   ```
   - If conflict occurs, stop and report which branch caused it
4. **Ensure guardrails and pty-mcp are up-to-date:**
   ```bash
   make install-guardrails && make install-pty-mcp
   ```
5. **Report summary:**
   ```
   Pulled into <current> from other worktrees:
   ✓ main
   ✓ feature-a
   ✓ feature-b

   All worktree branches merged successfully.
   ```
   Or if conflicts:
   ```
   Pulled into <current> from other worktrees:
   ✓ main
   ✗ feature-a (conflicts - resolve before continuing)

   Resolve conflicts, then run: /worktree pull-all
   ```

---

## Push

**Steps:**

1. **Check for uncommitted changes:** `git status --porcelain`
   - If changes exist, warn user and stop
2. **Get current branch:** `git branch --show-current`
3. **Switch to main:**
   ```bash
   git checkout main
   ```
4. **Merge current branch:**
   ```bash
   git merge <current-branch>
   ```
5. **Switch back:**
   ```bash
   git checkout <current-branch>
   ```
6. **Report result**

**Mental model:** This IS a merge - you go TO main, then merge FROM your branch.

---

## Remove Worktree

**Extract name from:** `$ARGUMENTS` (after "remove ")

**Steps:**

1. **Get project name:** `basename $(git rev-parse --show-toplevel)`
2. **Check worktree exists:** `git worktree list | grep <name>`
3. **Check for uncommitted changes in worktree:**
   ```bash
   git -C ../<project>-<name> status --porcelain
   ```
   - If changes exist, warn and use AskUserQuestion to confirm
4. **Ask about branch deletion:** Use AskUserQuestion
   - "Delete the branch '<name>' as well?"
   - Options: Yes (delete branch) / No (keep branch)
5. **Remove worktree:**
   ```bash
   git worktree remove ../<project>-<name>
   ```
6. **Optionally delete branch:**
   ```bash
   git branch -d <name>
   ```
7. **Report success**
