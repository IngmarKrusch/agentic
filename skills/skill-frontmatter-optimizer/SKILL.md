---
name: skill-frontmatter-optimizer
description: "Analyze and optimize skill frontmatter for reliable automatic invocation. Use this skill when: (1) improving an existing skill's description for better triggering, (2) diagnosing why a skill isn't being invoked, (3) rewriting frontmatter to match production patterns, (4) validating description quality against best practices, or any task involving skill metadata optimization (examples: \"optimize frontmatter\", \"fix skill triggering\", \"improve skill description\", \"why isn't my skill invoked\")."
---

# Skill Frontmatter Optimizer

Optimize skill frontmatter descriptions for reliable automatic invocation by Claude Code.

## Core Problem

The `description` field is the **sole triggering mechanism** for skills. Claude only sees `name` + `description` (~100 words) until a skill triggers. The SKILL.md body is invisible until after the decision. Poor descriptions = unreliable invocation.

## Optimization Workflow

### Step 1: Analyze the Existing Skill

Run the analysis script to extract key information:

```bash
python scripts/analyze_skill.py /path/to/skill-folder
```

This extracts:
- Current frontmatter
- Key capabilities from the body
- File types handled
- Workflow steps mentioned
- Potential trigger phrases

### Step 2: Generate Optimized Description

Run the generator with analysis output:

```bash
python scripts/generate_description.py /path/to/skill-folder
```

Or manually construct using the pattern in `references/patterns.md`.

### Step 3: Validate

```bash
python /mnt/skills/examples/skill-creator/scripts/quick_validate.py /path/to/skill-folder
```

## Quick Manual Optimization

If not using scripts, apply this template:

```yaml
description: "[CAPABILITY_VERBS] [DOMAIN/FORMAT] [FEATURE_LIST]. Use this skill when [USER_INTENT] for: (1) [SCENARIO_1], (2) [SCENARIO_2], (3) [SCENARIO_3], or [CATCH_ALL]. (examples include [CONCRETE_TRIGGERS])"
```

### Checklist

- [ ] Starts with action verbs and key capabilities
- [ ] File extensions explicit: `(.docx files)`, `(.pdf, .xlsx)`
- [ ] Contains "Use this skill when..." or "When Claude needs to..."
- [ ] Scenarios enumerated: (1), (2), (3)...
- [ ] Catch-all phrase for edge cases
- [ ] Concrete example triggers in parentheses
- [ ] Under 1024 characters
- [ ] No angle brackets `<` or `>`

## Common Fixes

| Problem | Fix |
|---------|-----|
| Too vague | Add specific file types, actions, domains |
| No trigger signal | Add "Use this skill when..." phrase |
| Missing scenarios | Enumerate with (1), (2), (3)... |
| Body has "When to Use" | Move entirely to description |
| Over 1024 chars | Prioritize triggers over features |

## Reference

See `references/patterns.md` for production-tested patterns from Anthropic's own skills.
