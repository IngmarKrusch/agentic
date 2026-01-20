#!/usr/bin/env python3
"""
Skill Analyzer - Extracts key information from a skill for description optimization.

Usage:
    python analyze_skill.py /path/to/skill-folder

Outputs structured analysis to inform description optimization.
"""

import sys
import re
import yaml
from pathlib import Path
from collections import Counter

# Keywords that suggest trigger scenarios
ACTION_VERBS = {
    'create', 'build', 'generate', 'make', 'write', 'produce',
    'edit', 'modify', 'update', 'change', 'fix', 'revise',
    'analyze', 'extract', 'process', 'parse', 'read', 'examine',
    'convert', 'transform', 'merge', 'split', 'combine',
    'fill', 'complete', 'validate', 'verify', 'check',
    'format', 'style', 'design', 'layout', 'render'
}

# Primary file extension patterns (what the skill processes, not code/doc files)
PRIMARY_EXTENSIONS = re.compile(r'\.(docx|xlsx|pdf|pptx|csv|tsv|json|xml|html)\b', re.IGNORECASE)

# All file extensions for reference
ALL_EXTENSIONS = re.compile(r'\.(docx|xlsx|pdf|pptx|csv|tsv|json|xml|html|md|txt|py|js|ts|jsx|tsx|yaml|yml|png|jpg|jpeg|gif|svg)\b', re.IGNORECASE)

# Heading patterns that suggest use cases
USE_CASE_PATTERNS = [
    r'##\s*(creating|editing|reading|analyzing|converting|processing)',
    r'##\s*(how to|workflow|usage|use case)',
    r'##\s*(when to use|getting started|quick start)',
]


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from SKILL.md content."""
    if not content.startswith('---'):
        return {}
    
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def extract_body(content: str) -> str:
    """Extract markdown body (after frontmatter)."""
    match = re.match(r'^---\n.*?\n---\n?(.*)', content, re.DOTALL)
    return match.group(1) if match else content


def find_file_types(content: str) -> list:
    """Find primary file extensions mentioned in the content."""
    # First try primary extensions (actual document formats)
    primary_matches = PRIMARY_EXTENSIONS.findall(content)
    if primary_matches:
        extensions = list(set(ext.lower() for ext in primary_matches))
        return sorted(extensions)
    
    # Fall back to all extensions
    all_matches = ALL_EXTENSIONS.findall(content)
    extensions = list(set(ext.lower() for ext in all_matches))
    # Filter out code/config files unless that's all there is
    doc_exts = [e for e in extensions if e not in ['py', 'js', 'ts', 'jsx', 'tsx', 'yaml', 'yml', 'md', 'txt']]
    return sorted(doc_exts) if doc_exts else sorted(extensions)


def find_action_verbs(content: str) -> list:
    """Find action verbs used in the content."""
    words = re.findall(r'\b[a-z]+\b', content.lower())
    found = [w for w in words if w in ACTION_VERBS]
    # Return by frequency
    counter = Counter(found)
    return [verb for verb, _ in counter.most_common(10)]


def extract_headings(content: str) -> list:
    """Extract markdown headings that might indicate use cases."""
    headings = re.findall(r'^#{1,3}\s+(.+)$', content, re.MULTILINE)
    return headings


def find_code_patterns(content: str) -> dict:
    """Analyze code blocks for technology indicators."""
    patterns = {
        'python': bool(re.search(r'```python|import \w+|def \w+\(', content)),
        'javascript': bool(re.search(r'```javascript|```js|require\(|import .+ from', content)),
        'bash': bool(re.search(r'```bash|```sh|\$ [a-z]', content)),
        'has_scripts': bool(re.search(r'scripts/\w+\.py|scripts/\w+\.sh', content)),
    }
    return {k: v for k, v in patterns.items() if v}


def estimate_scenarios(headings: list, body: str) -> list:
    """Estimate likely usage scenarios from content analysis."""
    scenarios = []
    
    # Skip meta-headings that describe the doc, not use cases
    skip_patterns = ['overview', 'guide', 'introduction', 'quick start', 'getting started', 
                     'reference', 'installation', 'setup', 'requirements', 'prerequisites',
                     'python', 'javascript', 'bash', 'example', 'output']
    
    # Check headings for workflow indicators
    workflow_keywords = ['creating', 'editing', 'reading', 'analyzing', 'converting', 
                         'processing', 'filling', 'generating', 'building', 'extracting',
                         'merging', 'splitting', 'validating', 'formatting']
    
    for heading in headings:
        heading_lower = heading.lower()
        # Skip meta-headings and code-like content
        if any(skip in heading_lower for skip in skip_patterns):
            continue
        # Skip if looks like code (has special chars)
        if re.search(r'[(){}\[\]"\'=<>]', heading):
            continue
        for keyword in workflow_keywords:
            if keyword in heading_lower:
                clean = heading.strip().rstrip(':')
                if 5 < len(clean) < 50:
                    scenarios.append(clean)
                break
    
    # If not enough scenarios from headings, generate generic ones from verbs
    if len(scenarios) < 3:
        verbs_found = set()
        for verb in ['creat', 'edit', 'extract', 'merg', 'split', 'fill', 'generat', 'convert', 'read', 'analyz']:
            if verb in body.lower():
                verbs_found.add(verb)
        
        verb_to_scenario = {
            'creat': 'Creating new content',
            'edit': 'Editing existing content', 
            'extract': 'Extracting data',
            'merg': 'Merging files',
            'split': 'Splitting documents',
            'fill': 'Filling forms',
            'generat': 'Generating output',
            'convert': 'Converting formats',
            'read': 'Reading content',
            'analyz': 'Analyzing data'
        }
        
        for verb in list(verbs_found)[:5 - len(scenarios)]:
            if verb in verb_to_scenario:
                scenarios.append(verb_to_scenario[verb])
    
    return scenarios[:5]


def analyze_skill(skill_path: Path) -> dict:
    """Analyze a skill and return structured information."""
    skill_md = skill_path / 'SKILL.md'
    
    if not skill_md.exists():
        return {'error': f'SKILL.md not found in {skill_path}'}
    
    content = skill_md.read_text()
    frontmatter = extract_frontmatter(content)
    body = extract_body(content)
    headings = extract_headings(body)
    
    # Check for bundled resources
    has_scripts = (skill_path / 'scripts').exists()
    has_references = (skill_path / 'references').exists()
    has_assets = (skill_path / 'assets').exists()
    
    analysis = {
        'name': frontmatter.get('name', skill_path.name),
        'current_description': frontmatter.get('description', ''),
        'description_length': len(frontmatter.get('description', '')),
        'file_types': find_file_types(content),
        'action_verbs': find_action_verbs(body),
        'headings': headings,
        'estimated_scenarios': estimate_scenarios(headings, body),
        'technologies': find_code_patterns(content),
        'resources': {
            'scripts': has_scripts,
            'references': has_references,
            'assets': has_assets,
        },
        'body_lines': len(body.splitlines()),
    }
    
    # Quality checks on current description
    desc = analysis['current_description']
    analysis['quality_issues'] = []
    
    if len(desc) < 50:
        analysis['quality_issues'].append('Description too short (< 50 chars)')
    if len(desc) > 1024:
        analysis['quality_issues'].append(f'Description too long ({len(desc)} > 1024 chars)')
    if '<' in desc or '>' in desc:
        analysis['quality_issues'].append('Contains forbidden angle brackets')
    if not re.search(r'(use this skill when|when claude needs|use when)', desc.lower()):
        analysis['quality_issues'].append('Missing trigger phrase (Use this skill when...)')
    if not re.search(r'\(\d+\)', desc):
        analysis['quality_issues'].append('No enumerated scenarios (1), (2), (3)...')
    if not analysis['file_types'] or not any(ext in desc.lower() for ext in analysis['file_types']):
        if analysis['file_types']:
            analysis['quality_issues'].append(f'File types {analysis["file_types"]} not in description')
    
    return analysis


def print_analysis(analysis: dict):
    """Print analysis in a readable format."""
    if 'error' in analysis:
        print(f"❌ Error: {analysis['error']}")
        return
    
    print(f"\n{'='*60}")
    print(f"SKILL ANALYSIS: {analysis['name']}")
    print(f"{'='*60}\n")
    
    print("📋 CURRENT DESCRIPTION:")
    print(f"   Length: {analysis['description_length']} / 1024 chars")
    if analysis['current_description']:
        # Word wrap the description
        desc = analysis['current_description']
        wrapped = [desc[i:i+70] for i in range(0, len(desc), 70)]
        for line in wrapped:
            print(f"   {line}")
    else:
        print("   (empty)")
    
    print(f"\n📁 FILE TYPES DETECTED: {', '.join(analysis['file_types']) or 'none'}")
    print(f"🔧 ACTION VERBS: {', '.join(analysis['action_verbs'][:8]) or 'none'}")
    
    print(f"\n📑 HEADINGS ({len(analysis['headings'])}):")
    for h in analysis['headings'][:10]:
        print(f"   • {h}")
    
    print(f"\n🎯 ESTIMATED SCENARIOS:")
    for i, scenario in enumerate(analysis['estimated_scenarios'], 1):
        print(f"   ({i}) {scenario}")
    
    print(f"\n🛠️  TECHNOLOGIES: {', '.join(analysis['technologies'].keys()) or 'none detected'}")
    
    resources = [k for k, v in analysis['resources'].items() if v]
    print(f"📦 BUNDLED RESOURCES: {', '.join(resources) or 'none'}")
    
    print(f"\n⚠️  QUALITY ISSUES:")
    if analysis['quality_issues']:
        for issue in analysis['quality_issues']:
            print(f"   ❌ {issue}")
    else:
        print("   ✅ No major issues detected")
    
    print(f"\n{'='*60}\n")


def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze_skill.py /path/to/skill-folder")
        sys.exit(1)
    
    skill_path = Path(sys.argv[1]).resolve()
    
    if not skill_path.exists():
        print(f"❌ Path not found: {skill_path}")
        sys.exit(1)
    
    analysis = analyze_skill(skill_path)
    print_analysis(analysis)
    
    # Also output as parseable format for piping to generator
    print("--- RAW ANALYSIS (for generate_description.py) ---")
    import json
    print(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    main()
