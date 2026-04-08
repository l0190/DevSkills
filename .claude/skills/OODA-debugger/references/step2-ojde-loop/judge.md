# Judge (判断) — Hypothesis Analysis

## Goal

Based on observations, analyze the root cause of the problem, propose multiple possible hypotheses, and evaluate the likelihood of each.

## Hypothesis Generation Methods

### 1. Error Type Classification
Classify based on error type and generate hypotheses for each:

| Error Type | Common Causes | Hypothesis Direction |
|---|---|---|
| TypeError | Type mismatch, None value operations | Check variable types and None handling |
| IndexError | Out-of-bounds access, empty containers | Check boundary conditions and container length |
| AttributeError | Missing attributes, spelling errors | Check object types and attribute names |
| KeyError | Missing keys, key name errors | Check dictionary contents and key names |
| ValueError | Illegal values, format errors | Check value ranges and input validation |
| Logic Errors | Algorithm errors, incorrect conditions | Check logic flow and condition judgment |

### 2. Data Flow Analysis
- **Input hypothesis**: Is the input data correct? Are there abnormal values?
- **Processing hypothesis**: Are intermediate processing steps correct? Are there missed steps?
- **Output hypothesis**: Is the output format correct? Are there conversion errors?

### 3. Environmental Factors
- **Dependency hypothesis**: Are there version compatibility issues?
- **Concurrency hypothesis**: Are there race conditions?
- **Resource hypothesis**: Are there resource leaks or insufficient resources?

## Hypothesis Evaluation Criteria

Evaluate each hypothesis according to the following criteria:

1. **Consistency with observations** (1-5): How consistent is the hypothesis with the observed phenomena
2. **Explanatory power** (1-5): How many observed phenomena the hypothesis can explain
3. **Verifiability** (1-5): How easy the hypothesis is to verify
4. **Probability** (1-5): How likely the hypothesis is based on experience

## Output of Judgment Results

```markdown
## Judgment Record
- **Based on observations**: [List supporting observations]
- **Hypothesis list**:
  1. [Hypothesis 1]: Consistency [n/5], Explanatory power [n/5], Verifiability [n/5], Probability [n/5]
  2. [Hypothesis 2]: ...
  3. [Hypothesis 3]: ...
- **Most likely hypothesis**: [Selected hypothesis]
- **Reasoning process**: [Why this hypothesis was chosen]
```

## Important Principles

- Hypotheses should be based on **observations**, not pure speculation
- Propose at least **2-3** hypotheses, do not fixate on the first one
- Pay special attention to hypotheses with **high verifiability**
- Do not discard seemingly unlikely hypotheses
- Each hypothesis should have a clear verification method
