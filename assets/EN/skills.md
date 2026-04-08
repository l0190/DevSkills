## Skill Composition

```
your-skill-name/
├── SKILL.md          # Required, main entry file
├── scripts/          # Optional, executable scripts (bash preferred)
│   ├── process_data.py
│   └── validate.sh
├── references/       # Optional, on-demand loaded documents
│   ├── api-guide.md
│   └── examples/
└── assets/           # Optional, templates, fonts, icons, etc.
    └── report-template.md
```

- You can add new subdirectories under `references/` as long as they are documented in `SKILL.md`.
- Tell the AI what to do, but more importantly, tell it what **not** to do (and explain why).

## Harness Composition

OODA Loop: Observe - Orient - Decide - Act

Harness (the cockpit for agents) = Tools + Knowledge + Observation + Action Interfaces + Permissions

- **Tools (Function Calls):**
    - File read/write, shell (execution), web fetch/search
    - Skill, Task, Worktree
    - SubAgent, Spwarm
- **Action (Agent User Manual):** CLI commands, API calls, UI interactions (Devtools via DOM)
- **Observation:** git diff, error logs, browser state, sensor data
- **Knowledge:** Product docs, domain materials, API specs, style guides
    - Different domains have domain-specific debuggers (loggers).
    - The previous frontend/backend modeling and structured document generation approach is useful.
    - Use progressive disclosure — build multi-level project description documents with hierarchical directories.
- **Permissions:** Sandbox isolation, approval workflows, trust boundaries
- The entire project follows the **Occam's Razor principle**.

### Approval Mechanism via State Machines

- **Building debuggers:** Add them as decorators to code, displaying event types, location info, key variable states, function return values, and call chains.
    - Custom Python library functions for implementing debuggers, call chains, and decorators.
    - Let AI control VS Code to generate breakpoints/traces.
- **Test-driven development:** Add necessary comments during modifications. After reaching small milestones, produce reviewable markdown documents.
    - During the generation phase, produce both software architecture and interface test cases simultaneously: design documents should contain only interfaces and functional descriptions.
    - Treat the development of each small module as a large-scale debug session — develop while generating new tests.
- **Architecture diagram tool:** Translate containers into code.

## References

- https://github.com/shareAI-lab/learn-claude-code.git
- https://github.com/shareAI-lab/claw0.git
- https://github.com/Donchitos/Claude-Code-Game-Studios
- https://github.com/toukanno/claude-code-game-studios
