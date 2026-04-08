# Step 3: Debug Report Generation Guide

## Goal

Organize the complete records of the OJDE loop debugging process and generate a structured debug report.

## Debug Report Template

```markdown
# Debug Report

## Overview
- **Problem**: [Brief description of the problem]
- **Root Cause**: [Root cause of the problem]
- **Fix Method**: [Method used to fix the problem]
- **Total Loop Iterations**: [Number of OJDE loops executed]

## Bug Report Summary
[Brief summary of the initial bug report]

## Debugging Process

### Loop Iteration 1
- **Observe**: [Key observations]
- **Judge**: [Proposed hypotheses and evaluation]
- **Decide**: [Selected hypothesis and verification plan]
- **Execute**: [Execution result and new discoveries]

### Loop Iteration 2
...

## Final Fix

### Problem Root Cause
[Detailed description of the root cause]

### Fix Solution
[Specific fix steps and code changes]

### Changed Files
- `file1.py`: [Change description]
- `file2.py`: [Change description]

## Verification

### Test Results
- [ ] Original test cases pass
- [ ] New test cases pass
- [ ] Related functionality is unaffected

### Side-Effect Assessment
[Assessment of the impact of the fix on other functionality]

## Lessons Learned
- [Experience and lessons from this debugging session]
- [Recommended improvement measures]
```

## Report Writing Principles

1. **Objectivity**: State facts based on facts, not subjective judgments
2. **Completeness**: Record the complete process of each loop iteration
3. **Traceability**: Each conclusion should be traceable to specific observations
4. **Clarity**: Non-project members should also be able to understand the report
5. **Constructiveness**: Provide improvement recommendations, not just problem descriptions

## Supplementary Materials

The following supplementary materials can be attached as needed:
- Key code snippets (before and after changes)
- Complete log output
- Screenshots or screen recordings
- Related Issue/PR links
