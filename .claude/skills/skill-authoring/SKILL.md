---
name: skill-authoring
description: Create, design, and validate Agent Skills for Claude Code. Use when the user wants to create a new skill, improve an existing skill, or learn about skill authoring best practices. Helps with SKILL.md structure, frontmatter validation, progressive disclosure, and testing strategies.
---

# Skill Authoring

Expert guide for creating high-quality Agent Skills for Claude Code. This skill helps you design, implement, and validate skills that Claude can discover and use effectively.

## Quick Start

When creating a new skill:

1. **Identify the capability**: What specific task or domain should this skill handle?
2. **Choose location**: Personal (`~/.claude/skills/`) or project (`.claude/skills/`)
3. **Create structure**: Skill directory + `SKILL.md` file
4. **Write frontmatter**: Name, description with trigger words
5. **Add instructions**: Clear, step-by-step guidance
6. **Test discovery**: Ask questions that should trigger the skill

## File Structure

### Minimal Skill (Single File)
```
my-skill/
└── SKILL.md
```

### Multi-File Skill (Progressive Disclosure)
```
my-skill/
├── SKILL.md          # Required: Main entry point
├── REFERENCE.md      # Optional: Detailed API docs
├── EXAMPLES.md       # Optional: Extended examples
├── scripts/          # Optional: Helper scripts
│   └── helper.py
└── templates/        # Optional: Template files
    └── template.txt
```

## SKILL.md Format

### Required Frontmatter

```yaml
---
name: your-skill-name
description: What this skill does AND when to use it. Include trigger words users would mention.
---
```

**Field requirements**:
- `name`: lowercase, hyphens only, max 64 chars (e.g., `pdf-form-filler`)
- `description`: max 1024 chars, must include both WHAT and WHEN

### Optional Frontmatter

```yaml
---
name: safe-file-reader
description: Read files without making changes. Use when you need read-only access.
allowed-tools: Read, Grep, Glob
---
```

**allowed-tools**: Restricts which tools Claude can use when skill is active (whitelist approach)

## Writing Effective Descriptions

The description is **critical** for skill discovery. Claude uses it to decide when to activate your skill.

### Bad Examples

```yaml
# Too vague
description: Helps with documents

# Missing trigger words
description: Processes files

# No usage context
description: Data analysis tool
```

### Good Examples

```yaml
# Specific domain + trigger words
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.

# Clear capability + when to use
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when working with Excel files, spreadsheets, or analyzing tabular data in .xlsx format.

# Explicit tools + scenarios
description: Generate commit messages from git diffs. Use when writing commit messages, reviewing staged changes, or running git workflows.
```

**Formula**: `[What it does] + [Key capabilities] + "Use when" + [Trigger scenarios/keywords]`

## Progressive Disclosure Pattern

Keep `SKILL.md` concise. Reference additional files only when needed:

````markdown
# PDF Processing

## Quick Start

Extract text from PDFs:
```python
import pdfplumber
with pdfplumber.open("doc.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

For form filling workflows, see [FORMS.md](FORMS.md).
For complete API reference, see [REFERENCE.md](REFERENCE.md).

## Installation

```bash
pip install pypdf pdfplumber
```
````

Claude reads additional files **only when it needs them**, managing context efficiently.

## Dependencies and Requirements

**Always be explicit** about what needs to be installed:

### Bad Example
```markdown
Use the pdf library to process files.
```

### Good Example
````markdown
## Requirements

Install required packages in your environment:
```bash
pip install pypdf pdfplumber
```

Then use:
```python
from pypdf import PdfReader
reader = PdfReader("file.pdf")
```
````

**Note**: List required packages in the description frontmatter if they're critical:
```yaml
description: Extract text from PDFs. Requires pypdf and pdfplumber packages.
```

## Instructions Best Practices

### Use Clear Steps

```markdown
## Instructions

1. Run `git diff --staged` to see changes
2. Analyze the diff for:
   - Changed functionality
   - Affected components
   - Breaking changes
3. Generate commit message:
   - Summary line (max 50 chars)
   - Blank line
   - Detailed description
   - Why the change was made
```

### Provide Examples

```markdown
## Examples

### Basic Usage
Input: "Extract text from report.pdf"
Output: Extracted text with page numbers

### Advanced Usage
Input: "Fill out form.pdf with data from spreadsheet.csv"
Output: Completed form.pdf with validation report
```

### Define Constraints

```markdown
## Constraints

- Only process PDF files smaller than 100MB
- Maximum 500 pages per document
- Requires read permission on input files
- Output directory must exist before processing
```

## Tool Restrictions with allowed-tools

Use `allowed-tools` to create focused, secure skills:

### Read-Only Skill
```yaml
---
name: code-analyzer
description: Analyze code quality and patterns. Use for code review without modifications.
allowed-tools: Read, Grep, Glob
---
```

### Data Analysis Skill
```yaml
---
name: log-analyzer
description: Parse and analyze log files. Use for debugging and diagnostics.
allowed-tools: Read, Grep, Bash
---
```

**When to use**:
- Read-only workflows (analysis, review, search)
- Security-sensitive operations
- Limited-scope tasks (only data processing, no file writing)

**When NOT to use**:
- Skills that need full tool access
- Development workflows requiring multiple tools
- Skills where tool needs vary by task

## Testing Your Skill

### 1. Description Testing

Ask questions that match your description trigger words:

**Skill description**: "Extract text from PDF files..."

**Test queries**:
- "Can you help me extract text from this PDF?"
- "I need to process a PDF document"
- "Read the contents of report.pdf"

### 2. Capability Testing

Verify each capability works:

```markdown
Test cases for pdf-processing skill:
✓ Extract text from single-page PDF
✓ Extract text from multi-page PDF
✓ Handle password-protected PDFs (error case)
✓ Fill form fields
✓ Validate form data
✓ Merge multiple PDFs
```

### 3. Edge Case Testing

```markdown
Error scenarios:
- File not found
- Corrupted PDF
- Missing dependencies
- Invalid permissions
- Unsupported PDF version
```

## Common Issues and Fixes

### Issue: Skill Not Discovered

**Symptoms**: Claude doesn't use your skill for relevant queries

**Diagnosis**:
1. Check description specificity
2. Verify trigger words match user queries
3. Ensure YAML syntax is valid

**Fix**:
```yaml
# Before (too vague)
description: Helps with data

# After (specific + triggers)
description: Analyze CSV and Excel files, generate reports, create visualizations. Use when working with spreadsheets, data files, or mentions of .csv, .xlsx formats.
```

### Issue: YAML Syntax Errors

**Symptoms**: Skill not loading, no errors in Claude

**Diagnosis**:
```bash
# View frontmatter
cat .claude/skills/my-skill/SKILL.md | head -n 10

# Check for:
# - Missing opening/closing ---
# - Tabs instead of spaces
# - Unquoted special characters
```

**Fix**:
```yaml
# Wrong (uses tabs, missing quotes)
name:	my-skill
description: Has : special chars

# Right (spaces, quoted)
name: my-skill
description: "Has : special chars in quotes"
```

### Issue: Wrong Skill Activated

**Symptoms**: Claude confuses similar skills

**Diagnosis**: Overlapping descriptions

**Fix**: Use distinct trigger words and domains

```yaml
# Skill 1 - Specific
description: Analyze sales data from Excel and CRM. Use for sales reports, pipeline analysis, revenue tracking.

# Skill 2 - Specific
description: Analyze log files and system metrics. Use for performance monitoring, debugging, system diagnostics.
```

## Skill Templates

### Simple Single-Purpose Skill

````yaml
---
name: commit-message-generator
description: Generate conventional commit messages from git diffs. Use when writing commits or reviewing staged changes.
---

# Commit Message Generator

## Instructions

1. Run `git diff --staged`
2. Analyze changes for:
   - Type: feat, fix, docs, refactor, test, chore
   - Scope: affected component
   - Breaking changes
3. Generate message:
   - `type(scope): summary` (max 50 chars)
   - Detailed description
   - Footer (breaking changes, issues)

## Examples

```
feat(auth): add OAuth2 support

Implement OAuth2 authentication flow with Google provider.
Includes token refresh and session management.

BREAKING CHANGE: Session format changed, users will be logged out.
Closes #123
```
````

### Multi-File Reference Skill

````yaml
---
name: api-integration
description: Integrate with REST APIs including authentication, error handling, rate limiting. Use when connecting to external APIs or web services.
---

# API Integration

## Quick Start

Basic API call with authentication:
```python
import requests

response = requests.get(
    "https://api.example.com/data",
    headers={"Authorization": f"Bearer {token}"}
)
data = response.json()
```

## Advanced Topics

- Authentication patterns: See [AUTH.md](AUTH.md)
- Error handling: See [ERRORS.md](ERRORS.md)
- Rate limiting: See [RATE_LIMITS.md](RATE_LIMITS.md)
- Testing: See [TESTING.md](TESTING.md)

## Best Practices

1. Always handle timeouts
2. Implement exponential backoff
3. Log request/response for debugging
4. Validate responses before processing
````

### Tool-Restricted Skill

````yaml
---
name: security-auditor
description: Audit code for security vulnerabilities and best practices. Read-only analysis. Use for security review, vulnerability scanning.
allowed-tools: Read, Grep, Glob
---

# Security Auditor

## Audit Checklist

1. **Authentication & Authorization**
   - Password storage (hashing, salting)
   - Session management
   - Access control

2. **Input Validation**
   - SQL injection prevention
   - XSS protection
   - Command injection

3. **Data Protection**
   - Encryption at rest
   - Encryption in transit
   - Sensitive data exposure

4. **Dependencies**
   - Known vulnerabilities
   - Outdated packages
   - License compliance

## Instructions

1. Use Glob to find relevant files:
   - `**/*.py`, `**/*.js`, `**/*.java`
   - `**/package.json`, `**/requirements.txt`
2. Use Read to examine code
3. Use Grep to find security patterns:
   - `password`, `secret`, `token`
   - `eval`, `exec`, `system`
4. Report findings with severity levels
````

## Validation Checklist

Before considering a skill complete:

- [ ] Frontmatter uses valid YAML syntax
- [ ] `name` follows naming rules (lowercase, hyphens, max 64)
- [ ] `description` includes both WHAT and WHEN (max 1024)
- [ ] Description contains trigger words users would say
- [ ] Instructions are clear and step-by-step
- [ ] Dependencies are explicitly documented
- [ ] Examples show realistic usage
- [ ] Error cases are handled
- [ ] Skill activates for relevant queries
- [ ] Skill doesn't conflict with existing skills
- [ ] Supporting files use progressive disclosure
- [ ] `allowed-tools` is set if restricting access

## Sharing Skills

### Via Project Repository
```bash
# Add to project
mkdir -p .claude/skills/team-skill
# Create SKILL.md

# Commit and share
git add .claude/skills/
git commit -m "Add team skill for X"
git push

# Team members get automatically
git pull
claude  # Skill now available
```

### Via Claude Code Plugin
1. Create plugin with `skills/` directory
2. Add skills to plugin `skills/` folder
3. Publish to marketplace
4. Team installs plugin

See [Claude Code plugins documentation](https://docs.claude.com/en/plugins) for details.

## Best Practices Summary

1. **Be specific in descriptions** - Include trigger words and usage scenarios
2. **Keep SKILL.md focused** - Use progressive disclosure for detail
3. **Document dependencies** - Explicit installation instructions
4. **Provide clear examples** - Show realistic, practical usage
5. **Test thoroughly** - Verify discovery, capabilities, edge cases
6. **Use allowed-tools wisely** - Restrict for security/focus when needed
7. **One skill, one capability** - Avoid overly broad skills
8. **Name clearly** - Use domain-specific, discoverable names
9. **Handle errors gracefully** - Document failure modes
10. **Version your skills** - Track changes in content/comments

## Resources

- [Official Claude Code Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Skills Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Progressive Disclosure Pattern](PROGRESSIVE_DISCLOSURE.md)
- [Skill Examples Collection](EXAMPLES.md)
- [Testing Strategies](TESTING.md)

---

**Remember**: A skill's effectiveness comes from **clear descriptions** that help Claude discover when to use it, and **focused instructions** that guide execution. Start simple, test thoroughly, iterate based on usage.
