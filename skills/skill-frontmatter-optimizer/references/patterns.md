# Production Frontmatter Patterns

Patterns extracted from Anthropic's production skills that achieve reliable triggering.

## Anatomy of an Effective Description

```
[CAPABILITY_SUMMARY]. [TRIGGER_PHRASE] [ENUMERATED_SCENARIOS]. [EXAMPLES]
```

### Component Breakdown

| Component | Purpose | Character Budget |
|-----------|---------|------------------|
| Capability Summary | What the skill does | ~200-300 chars |
| Trigger Phrase | Signal to invoke | ~30-50 chars |
| Enumerated Scenarios | Specific use cases | ~300-400 chars |
| Examples/Catch-all | Edge case coverage | ~100-200 chars |

**Total budget: 1024 characters max**

---

## Production Examples

### docx (Document Processing)

```yaml
description: "Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. When Claude needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks"
```

**Pattern elements:**
- Capability: "Comprehensive document creation, editing, and analysis"
- Features: "tracked changes, comments, formatting preservation, text extraction"
- File type: "(.docx files)"
- Trigger: "When Claude needs to work with"
- Enumeration: "(1) Creating... (2) Modifying... (3) Working with... (4) Adding..."
- Catch-all: "or any other document tasks"

### xlsx (Spreadsheet Processing)

```yaml
description: "Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. When Claude needs to work with spreadsheets (.xlsx, .xlsm, .csv, .tsv, etc) for: (1) Creating new spreadsheets with formulas and formatting, (2) Reading or analyzing data, (3) Modify existing spreadsheets while preserving formulas, (4) Data analysis and visualization in spreadsheets, or (5) Recalculating formulas"
```

**Pattern elements:**
- Multiple file extensions: "(.xlsx, .xlsm, .csv, .tsv, etc)"
- Five enumerated scenarios
- Specific actions: "preserving formulas", "recalculating"

### pdf (PDF Processing)

```yaml
description: "Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When Claude needs to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale."
```

**Pattern elements:**
- Toolkit framing: "manipulation toolkit"
- Action verbs: "extracting, creating, merging/splitting, handling"
- Specific highlight: "fill in a PDF form" (common use case)
- Scale indicator: "at scale"

### frontend-design (UI/Web)

```yaml
description: "Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics."
```

**Pattern elements:**
- Quality markers: "distinctive", "production-grade", "high design quality"
- Trigger phrase: "Use this skill when the user asks to"
- Parenthetical examples: "(examples include websites, landing pages...)"
- Negative definition: "avoids generic AI aesthetics"

### product-self-knowledge (Reference/Knowledge)

```yaml
description: "Authoritative reference for Anthropic products. Use when users ask about product capabilities, access, installation, pricing, limits, or features. Provides source-backed answers to prevent hallucinations about Claude.ai, Claude Code, and Claude API."
```

**Pattern elements:**
- Authority claim: "Authoritative reference"
- Query types: "capabilities, access, installation, pricing, limits, features"
- Value proposition: "prevent hallucinations"
- Product scope: "Claude.ai, Claude Code, Claude API"

---

## Trigger Phrase Variants

All production skills use one of these patterns:

| Pattern | Example |
|---------|---------|
| "When Claude needs to..." | "When Claude needs to work with professional documents" |
| "Use this skill when..." | "Use this skill when the user asks to build" |
| "Use when..." | "Use when users ask about product capabilities" |

---

## Keyword Categories to Include

### Action Verbs (front-load these)
- create, build, generate, make
- edit, modify, update, change
- analyze, extract, process, parse
- convert, transform, merge, split
- fill, complete, validate

### Domain Markers
- File extensions: .docx, .pdf, .xlsx, .pptx, .csv
- Formats: document, spreadsheet, presentation, form
- Domains: financial, legal, technical, creative

### Intent Signals
- "professional documents"
- "data analysis"
- "form filling"
- "content creation"

---

## Anti-Patterns

### ❌ Vague capability
```yaml
description: "Helps with documents"
```

### ❌ Missing trigger phrase
```yaml
description: "PDF processing with text extraction and form handling"
```

### ❌ No enumeration
```yaml
description: "Use for creating and editing spreadsheets"
```

### ❌ Body-dependent
```yaml
description: "See SKILL.md for when to use this skill"
```

### ❌ Over-technical
```yaml
description: "Implements OOXML manipulation via python-docx library for programmatic document generation using the Open Packaging Convention"
```

---

## Character Counting Strategy

With 1024 char limit, prioritize:

1. **Must have** (~400 chars): Core capability + trigger phrase
2. **Should have** (~400 chars): Enumerated scenarios (at least 3)
3. **Nice to have** (~200 chars): Examples, catch-all, quality markers

If over limit, cut:
- Redundant feature lists
- Technical implementation details
- Verbose qualifiers ("comprehensive", "advanced")
