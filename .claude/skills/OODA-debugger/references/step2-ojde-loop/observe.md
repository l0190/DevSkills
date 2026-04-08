# Observe (观察) — Information Collection

## Goal

Through various means, collect sufficient information about current code execution status to provide an evidence base for subsequent judgment and decision-making.

## Observation Methods

### 1. Code Static Analysis
- Read related source code files
- Check function definitions and call relationships
- Analyze data flow and control flow
- Check boundary conditions and exception handling

### 2. Dynamic Execution Observation
- Run the program to reproduce the problem
- Add print/logging statements to key locations
- Use Python's built-in debugging tools:
  ```python
  import pdb; pdb.set_trace()  # Breakpoint
  import logging; logging.basicConfig(level=logging.DEBUG)
  ```
- Check variable values and state

### 3. Instrumentation Observation
When basic observation is insufficient, add instrumentation code to key locations:
- **Function entry/exit**: Log function call and return values
- **Key variable changes**: Track variable value changes
- **Conditional branches**: Log which branch was executed
- **Loop iterations**: Log loop count and key state

### 4. Log Analysis
- Check application logs
- Check system logs
- Check error output
- Analyze log timestamp sequence

## Output of Observation Results

Each observation should produce a clear record:

```markdown
## Observation Record
- **Method**: [Code Reading/Execution/Instrumentation/Log Analysis]
- **Target**: [Specific file/function/variable]
- **Result**: [Specific observed phenomenon]
- **Evidence**: [Related code snippet, log output, variable values]
```

## Important Principles

- Observations should be **objective facts**, not subjective speculation
- Every observation should have concrete **evidence**
- When observation information is insufficient, proactively add instrumentation
- Record all observations, including those that seem irrelevant
- Use multiple observation methods for cross-validation
