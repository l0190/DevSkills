## Skill Structure
A skill is essentially a folder containing scripts, documents, and assets.

```bash
skill-name/
├── SKILL.md          # Required, main entry file
├── scripts/          # Optional, executable scripts (bash preferred)
│   ├── process_data.py
│   └── validate.sh
├── references/       # Optional, on-demand loaded documents
│   ├── api-guide.md
│   └── examples/
└── assets/           # Optional, templates, fonts, icons, etc.
    └── template.md
```

## Skill Migration
To migrate a skill, move it to the corresponding skills directory of your AI coding tool.

| Tool         | Skills Directory      |
| -------------- | -------------------- |
| ClaudeCode   | `.claude/skills/`  |
| OpenCode     | `opencode/skills/` |
| Copilot      | `.github/skills`   |

## Available Skills

| Skill | Description | Link |
| ------------ | -------------------- | ---- |
| OODA-debugger | LLM-driven automated debugging skill based on the OODA loop | [CN](.claude/skills-CN/OODA-debugger/) \| [EN](.claude/skills/OODA-debugger/) |
| call-graph | Python function call tree generator | [CN](.claude/skills-CN/call-graph/) \| [EN](.claude/skills/call-graph/) |

## Documentation

- [中文 README](README.md)
- [Design Docs (CN)](assets/CN/skills.md) \| [Debugger](assets/CN/debugger.md) \| [Analysis](assets/CN/analysis.md)
- [English Docs](assets/EN/skills.md) \| [Debugger](assets/EN/debugger.md) \| [Analysis](assets/EN/analysis.md)
- [LICENSE](LICENSE) (MIT)
