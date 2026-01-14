---
description: "Create, manage, and synchronize git worktrees for running parallel Claude Code sessions. Use this skill when: (1) creating isolated worktrees for parallel development, (2) checking status across all worktrees, (3) pulling changes from another branch, (4) pushing changes to main, (5) removing completed worktrees, or any git worktree operations (examples: 'create worktree', 'worktree status', 'parallel branches', 'multiple Claude sessions')."
argument-hint: "[create|status|pull|push|remove] [name]"
---

# Git Worktree Management

Manage git worktrees for parallel Claude Code sessions.

## Command Routing

{{#if $ARGUMENTS}}
Parse the command from: `$ARGUMENTS`

**Routing:**
- Starts with `create ` → Go to **Create Worktree**
- Equals `status` → Go to **Status**
- Starts with `pull ` → Go to **Pull**
- Equals `push` → Go to **Push**
- Starts with `remove ` → Go to **Remove Worktree**
- Otherwise → Show help below
{{else}}
**No command provided.** Show this help:
{{/if}}

## Help

```
/worktree - Manage git worktrees for parallel Claude Code sessions

Commands:
  create <name>    Create new worktree as sibling directory
  status           Show all worktrees and their state
  pull <source>    Pull changes from another branch into current
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
  /worktree pull main
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
5. **Report success:**
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