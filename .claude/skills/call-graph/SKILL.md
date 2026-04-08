---
name: call-graph
description: Generate a function call tree for Python projects to visualize execution flow and code structure. MUST trigger in the following scenarios: the user wants to understand code execution flow, trace function calls, analyze call chains, visualize code flow, find entry points, or debug complex execution paths; the user mentions "call graph", "call tree", "function trace", "execution flow", "call chain", "how does this code run?", "what functions are called?", "trace", "调用图", "调用树", "函数追踪", "执行流程".
---

# Python Function Call Graph Generator

This skill uses `trace_call_tree.py` to trace Python function calls via `sys.setprofile` and output a structured call tree, helping you quickly understand project execution flow.

## When to Use

- Understanding an unfamiliar codebase's execution flow
- Analyzing which functions a specific entry point calls
- Debugging complex call chains
- Comparing actual runtime call paths vs. static code structure
- Verifying that refactored code follows expected execution paths

## How It Works

The tracer uses Python's `sys.setprofile` hook to capture every function call/return at runtime. It filters out standard library and third-party calls, retaining only **project-internal** calls, then formats them into an indented tree.

## Quick Usage

```bash
# Basic: trace from main() in a script
python .claude/skills-EN/call-graph/scripts/trace_call_tree.py \
  --entry path/to/script.py \
  --project-root path/to/project

# Specify a different entry function
python .claude/skills-EN/call-graph/scripts/trace_call_tree.py \
  --entry path/to/script.py \
  --main-func run_server \
  --project-root path/to/project

# Trace module-level code (no main function needed)
python .claude/skills-EN/call-graph/scripts/trace_call_tree.py \
  --entry path/to/script.py \
  --module-exec \
  --project-root path/to/project

# Custom output path
python .claude/skills-EN/call-graph/scripts/trace_call_tree.py \
  --entry path/to/script.py \
  --output my_call_tree.log
```

## Parameters

| Parameter | Required | Default | Description |
|---|---|---|---|
| `--entry` | Yes | - | Path to the Python entry file |
| `--main-func` | No | `main` | Entry function name to start tracing from |
| `--project-root` | No | `.` | Project root used to filter internal calls |
| `--output` | No | `call_tree.log` | Output log file path |
| `--module-exec` | No | `false` | Trace module-level code without requiring a main() function |
| `--` separator | No | - | Arguments after `--` are forwarded to the entry script |

## Output Format

The output is an indented tree showing function names with call counts:

```
├── module.py:main [count=1]
│   ├── module.py:process_data [count=3]
│   │   ├── module.py:validate [count=3]
│   │   └── module.py:transform [count=2]
│   └── module.py:write_output [count=1]
```

Each node shows:
- **File path** relative to project root
- **Function/method name** (including class name for methods, e.g. `MyClass.my_method`)
- **Call count** — how many times this function was invoked from its parent

## Workflow

When the user asks to trace or understand code execution flow:

1. **Identify the entry point** — find the `main()` function or relevant entry script in the project.
2. **Determine project root** — use the top-level project directory so the tracer correctly filters internal vs. external calls.
3. **Run the tracer** — execute `trace_call_tree.py` with appropriate parameters. If the target script requires arguments, pass them after `--`.
4. **Read and present the output** — read the generated `call_tree.log` file and explain the execution structure to the user.
5. **Analyze** — highlight key call chains, hot paths (high count values), and any unexpected patterns.

## Important Notes

- The tracer captures **runtime** calls, so code paths not executed (e.g., error handlers that don't trigger) won't appear in the tree.
- The `--module-exec` flag is useful for scripts that run logic at module level rather than through a `main()` function.
- The tracer filters out calls from `site-packages/`, `dist-packages/`, and virtual environment directories (`env/`, `venv/`, `.venv/`).
- For multi-threaded code, the tracer profiles all threads and merges results into a single tree.
