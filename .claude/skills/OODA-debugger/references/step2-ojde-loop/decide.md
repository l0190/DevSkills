# Decide (决策) — Formulate Verification Plan

## Goal

Select the most suitable hypothesis from the judgment results and formulate a specific verification plan. **Every decision must be supported by concrete observational evidence.**

## Decision Process

### 1. Hypothesis Selection
Select the optimal hypothesis to verify based on the judgment results:

**Priority principles:**
1. **Most probable hypothesis** — Most consistent with observed phenomena
2. **Easiest to verify** — Can be verified quickly with minimal changes
3. **Most critical hypothesis** — If verified, can directly locate the problem

### 2. Verification Method Selection

| Verification Method | Applicable Scenarios | Pros | Cons |
|---|---|---|---|
| Add logging | Need to view runtime state | Non-intrusive, can be retained | May affect performance |
| Modify input data | Suspected data issues | Intuitive and clear | May not cover all cases |
| Write unit test | Need to reproduce the problem | Repeatable, can be retained | Takes time to write |
| Code inspection | Suspected logic errors | No execution required | May miss runtime issues |
| Add assertions | Need to verify intermediate states | Automatic checking | Needs to know expected values |
| Simplified reproduction | Complex problem | Quick positioning | May lose key information |

### 3. Formulate Execution Plan

Clear steps must be defined:

```markdown
## Decision Record
- **Selected hypothesis**: [Specific hypothesis content]
- **Observation basis**: [Which observations support this decision]
- **Verification method**: [Specific method chosen]
- **Execution steps**:
  1. [Specific step 1]
  2. [Specific step 2]
  3. [Specific step 3]
- **Expected result**: [What outcome indicates the hypothesis is correct]
- **Fallback plan**: [What to do if the hypothesis is incorrect]
```

## Important Principles

- **Decisions must be supported by concrete observations** — cannot be based on feelings
- **Only verify one hypothesis** — avoid modifying multiple places simultaneously
- **Define clear success/failure criteria** — know what different results mean
- **Keep modifications small** — each verification should be as small a change as possible
- **Prepare a fallback plan** — know the next step if the current hypothesis is incorrect
