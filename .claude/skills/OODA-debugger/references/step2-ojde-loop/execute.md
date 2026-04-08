# Execute (执行) — Execute and Test

## Goal

Execute the verification plan from the decision phase, immediately observe the results, and provide new observational information for the next loop iteration.

## Execution Steps

### 1. Backup Current State
Before making any changes, ensure the current state is recoverable:
```bash
# Use git to save current state
git stash  # or git add + git commit
```

### 2. Execute Verification Plan
Execute step by step according to the plan from the decision phase:

- **Add logging**: Add logging statements at specified locations
- **Modify code**: Make necessary code modifications according to the plan
- **Run tests**: Execute related test cases
- **Run program**: Reproduce the problem and observe new output

### 3. Immediately Observe Results
Immediately collect the following information after execution:

```markdown
## Execution Record
- **Executed operation**: [Specifically what was done]
- **Modified files**: [List of modified files]
- **Execution result**:
  - Program output: [New output]
  - Error information: [New error (if any)]
  - Variable values: [Key variable changes]
- **Comparison with expected result**: [Consistent/Inconsistent]
- **New observations**: [New phenomena discovered]
```

### 4. Evaluate Results

Evaluate the execution result according to the success/failure criteria defined in the decision phase:

- **Hypothesis confirmed** → Enter fix phase
- **Hypothesis not confirmed** → Return to Observe phase, bring new observations into the next loop iteration
- **New problem discovered** → Add to observation list, enter the next loop iteration

## Execution Principles

- **Execute strictly according to plan** — do not make additional modifications
- **Only modify one place** — ensure the cause-effect relationship of the problem is clear
- **Immediately observe** — do not wait, check the result right after execution
- **Record everything** — even seemingly irrelevant output
- **Do not over-fix** — the goal of the Execute phase is verification, not repair

## Loop Control

After execution, determine based on the results:
- **Continue loop**: New observations need further analysis
- **Terminate loop**: Problem resolved, or maximum iteration count reached
- **Escalate**: Problem exceeds processing capacity, report to user
