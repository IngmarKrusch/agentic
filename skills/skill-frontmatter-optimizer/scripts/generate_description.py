#!/usr/bin/env python3
"""
Description Generator - Creates optimized frontmatter descriptions for skills.

Usage:
    python generate_description.py /path/to/skill-folder

Analyzes the skill and generates an optimized description following production patterns.
"""

import sys
import re
import yaml
import json
from pathlib import Path
from typing import Optional

# Import analyzer functions
from analyze_skill import analyze_skill, extract_frontmatter, extract_body

MAX_DESCRIPTION_LENGTH = 1024

# Templates for different skill types
TEMPLATES = {
    'file_processor': (
        "{capability_phrase} for {file_types}. "
        "Use this skill when {trigger_context} for: {scenarios}. "
        "{examples_or_catchall}"
    ),
    'tool_integration': (
        "{capability_phrase}. "
        "Use this skill when {trigger_context} for: {scenarios}, "
        "or {catchall}"
    ),
    'knowledge_reference': (
        "{capability_phrase}. "
        "Use when {trigger_context}. "
        "{value_proposition}"
    ),
    'workflow_automation': (
        "{capability_phrase}. "
        "Use this skill when {trigger_context} for: {scenarios}. "
        "(examples include {examples})"
    ),
}


def classify_skill_type(analysis: dict) -> str:
    """Determine the type of skill based on analysis."""
    file_types = analysis.get('file_types', [])
    headings = [h.lower() for h in analysis.get('headings', [])]
    
    # File processor if handles specific file types
    if file_types and any(ext in ['docx', 'pdf', 'xlsx', 'pptx', 'csv'] for ext in file_types):
        return 'file_processor'
    
    # Knowledge reference if has reference-like headings
    if any(kw in ' '.join(headings) for kw in ['reference', 'documentation', 'api', 'schema']):
        return 'knowledge_reference'
    
    # Workflow if has step-based content
    if any(kw in ' '.join(headings) for kw in ['workflow', 'step', 'process', 'pipeline']):
        return 'workflow_automation'
    
    # Default to tool integration
    return 'tool_integration'


def generate_capability_phrase(analysis: dict) -> str:
    """Generate the capability summary phrase."""
    name = analysis.get('name', 'skill')
    verbs = analysis.get('action_verbs', [])[:4]
    file_types = analysis.get('file_types', [])
    
    # Convert name to readable form
    readable_name = name.replace('-', ' ').replace('_', ' ')
    
    if verbs:
        verb_phrase = ', '.join(verbs[:-1]) + f', and {verbs[-1]}' if len(verbs) > 1 else verbs[0]
        verb_phrase = verb_phrase.title()
    else:
        verb_phrase = "Processing and manipulation"
    
    if file_types:
        file_phrase = f"for {', '.join('.' + ext for ext in file_types[:3])} files"
    else:
        file_phrase = f"for {readable_name}"
    
    return f"{verb_phrase} {file_phrase}"


def generate_file_types_phrase(file_types: list) -> str:
    """Format file types for description."""
    if not file_types:
        return ""
    
    extensions = [f'.{ext}' for ext in file_types[:4]]
    if len(file_types) > 4:
        extensions.append('etc')
    
    return f"({', '.join(extensions)})"


def generate_scenarios(analysis: dict) -> str:
    """Generate enumerated scenarios."""
    scenarios = analysis.get('estimated_scenarios', [])
    verbs = analysis.get('action_verbs', [])
    
    # Use estimated scenarios if available
    if scenarios:
        formatted = []
        for i, scenario in enumerate(scenarios[:4], 1):
            # Clean up scenario text
            scenario = scenario.strip().rstrip('.')
            # Capitalize first letter, make concise
            if len(scenario) > 50:
                scenario = scenario[:47] + '...'
            formatted.append(f"({i}) {scenario}")
        return ', '.join(formatted)
    
    # Fall back to verb-based scenarios
    if verbs:
        verb_scenarios = []
        for i, verb in enumerate(verbs[:4], 1):
            verb_scenarios.append(f"({i}) {verb.capitalize()}ing content")
        return ', '.join(verb_scenarios)
    
    return "(1) Processing, (2) Analyzing, (3) Generating output"


def generate_trigger_context(analysis: dict) -> str:
    """Generate the trigger context phrase."""
    file_types = analysis.get('file_types', [])
    name = analysis.get('name', 'this task')
    
    if file_types:
        ext_list = ', '.join(f'.{ext}' for ext in file_types[:3])
        return f"working with {ext_list} files"
    
    readable_name = name.replace('-', ' ').replace('_', ' ')
    return f"handling {readable_name} tasks"


def generate_catchall(analysis: dict) -> str:
    """Generate a catch-all phrase."""
    name = analysis.get('name', 'related')
    readable_name = name.replace('-', ' ').replace('_', ' ')
    return f"or any other {readable_name} task"


def generate_examples(analysis: dict) -> str:
    """Generate example triggers."""
    headings = analysis.get('headings', [])
    
    # Extract actionable headings
    examples = []
    for h in headings[:6]:
        h_lower = h.lower()
        if any(kw in h_lower for kw in ['creating', 'editing', 'reading', 'converting', 'processing', 'building']):
            examples.append(h.lower().strip())
    
    if examples:
        return ', '.join(examples[:4])
    
    # Default examples based on file types
    file_types = analysis.get('file_types', [])
    if file_types:
        return f"creating, editing, or analyzing .{file_types[0]} files"
    
    return "processing, transforming, or generating content"


def generate_optimized_description(analysis: dict) -> str:
    """Generate an optimized description based on analysis."""
    skill_type = classify_skill_type(analysis)
    
    # Build components
    capability = generate_capability_phrase(analysis)
    file_types = generate_file_types_phrase(analysis.get('file_types', []))
    scenarios = generate_scenarios(analysis)
    trigger = generate_trigger_context(analysis)
    catchall = generate_catchall(analysis)
    examples = generate_examples(analysis)
    
    # Select and fill template
    if skill_type == 'file_processor':
        description = (
            f"{capability}. "
            f"Use this skill when {trigger} for: {scenarios}, "
            f"{catchall}"
        )
    elif skill_type == 'knowledge_reference':
        description = (
            f"{capability}. "
            f"Use when users ask about {trigger}. "
            f"Provides authoritative guidance for {examples}."
        )
    elif skill_type == 'workflow_automation':
        description = (
            f"{capability}. "
            f"Use this skill when {trigger} for: {scenarios}. "
            f"(examples include {examples})"
        )
    else:  # tool_integration
        description = (
            f"{capability}. "
            f"Use this skill when {trigger} for: {scenarios}, "
            f"{catchall}"
        )
    
    # Ensure under limit
    if len(description) > MAX_DESCRIPTION_LENGTH:
        # Truncate examples first
        description = re.sub(r'\(examples include[^)]+\)', '', description)
        description = description.strip()
    
    if len(description) > MAX_DESCRIPTION_LENGTH:
        # Reduce scenarios
        description = re.sub(r'\(\d+\)[^,]+,?\s*', '', description, count=2)
    
    # Final cleanup
    description = re.sub(r'\s+', ' ', description).strip()
    description = description.rstrip(',.')
    
    return description


def suggest_improvements(current: str, generated: str, analysis: dict) -> list:
    """Suggest specific improvements to make."""
    suggestions = []
    
    # Check for missing elements
    if not re.search(r'use (this skill )?when', current.lower()):
        suggestions.append("ADD trigger phrase: 'Use this skill when...'")
    
    if not re.search(r'\(\d+\)', current):
        suggestions.append("ADD enumerated scenarios: (1) Creating, (2) Editing, etc.")
    
    file_types = analysis.get('file_types', [])
    if file_types:
        missing_exts = [ext for ext in file_types if f'.{ext}' not in current.lower()]
        if missing_exts:
            suggestions.append(f"ADD file extensions: {', '.join('.' + e for e in missing_exts[:3])}")
    
    if len(current) < 100:
        suggestions.append("EXPAND: Description is too short for reliable matching")
    
    if len(current) > 900:
        suggestions.append("TRIM: Near character limit, prioritize triggers over features")
    
    # Check for anti-patterns
    if re.search(r'see skill\.md|refer to|see below', current.lower()):
        suggestions.append("REMOVE: References to body content (body is invisible before triggering)")
    
    return suggestions


def score_description(description: str, analysis: dict) -> int:
    """Score a description based on best practices (0-100)."""
    if not description:
        return 0
    
    score = 0
    
    # Length check (10 points)
    if 100 <= len(description) <= 800:
        score += 10
    elif 50 <= len(description) <= 1000:
        score += 5
    
    # Has trigger phrase (20 points)
    if re.search(r'use (this skill )?when|when claude needs', description.lower()):
        score += 20
    
    # Has enumerated scenarios (20 points)
    enum_count = len(re.findall(r'\(\d+\)', description))
    if enum_count >= 3:
        score += 20
    elif enum_count >= 1:
        score += 10
    
    # Has file types if skill handles files (15 points)
    file_types = analysis.get('file_types', [])
    if file_types:
        mentioned = sum(1 for ext in file_types if f'.{ext}' in description.lower())
        if mentioned > 0:
            score += 15
    else:
        score += 15  # No file types to check
    
    # Has catch-all phrase (10 points)
    if re.search(r'or any other|or other', description.lower()):
        score += 10
    
    # Has examples (10 points)
    if re.search(r'examples? include|such as|e\.g\.|including', description.lower()):
        score += 10
    
    # No anti-patterns (15 points)
    has_antipattern = False
    if re.search(r'see skill\.md|refer to|see below', description.lower()):
        has_antipattern = True
    if '<' in description or '>' in description:
        has_antipattern = True
    if not has_antipattern:
        score += 15
    
    return score


def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_description.py /path/to/skill-folder")
        sys.exit(1)
    
    skill_path = Path(sys.argv[1]).resolve()
    
    if not skill_path.exists():
        print(f"❌ Path not found: {skill_path}")
        sys.exit(1)
    
    # Analyze the skill
    analysis = analyze_skill(skill_path)
    
    if 'error' in analysis:
        print(f"❌ {analysis['error']}")
        sys.exit(1)
    
    current = analysis.get('current_description', '')
    generated = generate_optimized_description(analysis)
    suggestions = suggest_improvements(current, generated, analysis)
    
    current_score = score_description(current, analysis)
    generated_score = score_description(generated, analysis)
    
    print(f"\n{'='*60}")
    print(f"DESCRIPTION OPTIMIZATION: {analysis['name']}")
    print(f"{'='*60}\n")
    
    print("📋 CURRENT DESCRIPTION:")
    print(f"   ({len(current)} chars, score: {current_score}/100)")
    if current:
        for i in range(0, len(current), 70):
            print(f"   {current[i:i+70]}")
    else:
        print("   (empty)")
    
    print(f"\n✨ GENERATED DESCRIPTION:")
    print(f"   ({len(generated)} chars, score: {generated_score}/100)")
    for i in range(0, len(generated), 70):
        print(f"   {generated[i:i+70]}")
    
    # Recommendation
    print(f"\n📊 RECOMMENDATION:")
    if current_score >= 80:
        print("   ✅ Current description is strong. Minor tweaks only.")
    elif generated_score > current_score + 10:
        print("   🔄 Consider replacing with generated version.")
    else:
        print("   ⚙️  Apply specific improvements to current description.")
    
    print(f"\n💡 SPECIFIC IMPROVEMENTS:")
    if suggestions:
        for s in suggestions:
            print(f"   → {s}")
    else:
        print("   ✅ Current description follows best practices")
    
    print(f"\n📝 READY-TO-USE FRONTMATTER:")
    print("---")
    print(f"name: {analysis['name']}")
    
    # Use the better description
    best = generated if generated_score > current_score else current
    print(f'description: "{best}"')
    print("---")
    
    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    main()
