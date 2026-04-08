---
name: OODA-debugger
description: LLM-driven automated debugging skill based on the OJDE loop (Observed-Judge-Decide-Execute). Locates and fixes code bugs through the closed-loop "Observe → Judge → Decide → Execute" cycle, with each decision supported by concrete observational evidence, and generates a complete debug report. MUST trigger in the following scenarios: the user mentions "debug", "调试", "有bug", "运行出错了", "测试失败了", "程序异常", "排查问题", "定位问题", "结果不对", "不一致", "崩溃"; the user provides Python error types (IndexError, TypeError, AttributeError, KeyError, ValueError, ImportError, RuntimeError, etc.); the user provides error stack traces or error output; the user describes unexpected program behavior.
---

# OODA Debugger — Automated Debugging Skill

This skill implements LLM-driven automated debugging based on the OJDE loop (Observed-Judge-Decide-Execute). Through the "Observe → Judge → Decide → Execute" closed-loop cycle, it locates and fixes code bugs, ensuring that each decision is supported by concrete observational evidence, and ultimately generates a complete debug report.

## Execution Steps

### Step 1: Generate Bug Report

Read references/step1-bug-report/guide.md to learn how to generate the initial bug report.

Based on the problem description and program execution status provided by the user:
1. **Collect information**: Run the program, read source code, check error logs
2. **Fill in the bug report template**: Generate a structured bug report based on template requirements
3. **Confirm the report**: Ensure all key information is captured

### Step 2: OJDE Loop Debugging

After generating the bug report, enter the OJDE loop debugging phase. Execute in the following order:

1. **Observe** — Read `references/step2-ojde-loop/observe.md`
   - Collect current code execution status through source code reading, program execution, instrumentation, logging, etc.
   - Use tools: run code, check logs, add print statements, use debuggers, etc.

2. **Judge** — Read `references/step2-ojde-loop/judge.md`
   - Analyze hypotheses: Based on observations, infer the root cause of the problem
   - Propose multiple possible hypotheses and evaluate the likelihood of each
   - Hypothesis examples: "Is it a data issue?", "A logic boundary error?", "A race condition?"

3. **Decide** — Read `references/step2-ojde-loop/decide.md`
   - Formulate a verification plan: Select the most probable or easiest-to-verify hypothesis from the many
   - Decide on a specific method to verify it (e.g., modify input data, add logging, write unit test, inspect specific code segment)
   - **Every decision must have concrete observational evidence**

4. **Execute** — Read `references/step2-ojde-loop/execute.md`
   - Execute the verification plan from the previous step (e.g., modify code, run tests)
   - Immediately observe results to see if the issue is resolved or behavior has changed
   - Generate new "observation" information and enter the next loop iteration

**Loop termination conditions:**
- Bug is fixed and tests pass
- Reached maximum number of iterations (default 5)
- User explicitly stops

### Step 3: Generate Debug Report

Read references/step3-debug-report/guide.md to learn how to generate the final debug report.

After the OJDE loop ends:
1. Organize all observations, judgments, decisions, and executions throughout the process
2. Generate a complete debug report based on the template
3. Include: final fix solution, change description, lessons learned

## Important Principles

- **Every decision must have concrete observational evidence** — cannot judge based solely on speculation
- **Only one hypothesis is verified per loop** — avoid modifying multiple places simultaneously
- **Immediately observe results after execution** — quickly feed back into the next loop
- **Keep records** — each step should leave documentation for the final report
- **Instrumentation first** — when observation information is insufficient, add logging/instrumentation before judging
