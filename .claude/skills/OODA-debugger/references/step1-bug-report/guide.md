# Step 1: Bug Report Generation Guide

## Goal

Based on the problem description and program execution status provided by the user, generate a structured bug report to provide clear entry information for the subsequent OJDE loop.

## Bug Report Template

```markdown
# Bug Report

## Basic Information
- **Reporter**: [User/Developer]
- **Time**: [Discovery Time]
- **Severity**: [Critical/High/Medium/Low]

## Problem Description
[Clear description of the problem phenomenon]

## Reproduction Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Behavior
[Description of expected correct behavior]

## Actual Behavior
[Description of the actual erroneous behavior]

## Environment Information
- **Operating System**: [OS version]
- **Python Version**: [Python version]
- **Related Dependencies**: [Key dependency versions]

## Error Information
```
[Paste complete error stack trace]
```

## Preliminary Analysis
- **Error Type**: [e.g., TypeError, IndexError, Logic Error]
- **Affected Files**: [List related files]
- **Suspected Scope**: [Which module/function the issue might be in]

## Supplementary Information
[Logs, screenshots, related code snippets, etc.]
```

## Information Collection Methods

When the information provided by the user is insufficient, proactively collect through the following methods:

1. **Run the program**: Reproduce the problem and obtain the error stack trace
2. **Read source code**: Locate related code files and functions
3. **Check dependencies**: Confirm version compatibility
4. **View logs**: Check application logs and system logs
5. **Check configuration**: Confirm configuration file correctness

## Important Notes

- Ensure the reproduction steps are accurate and complete
- Error information should include the complete stack trace, not just the error message
- The preliminary analysis should be based on facts, not speculation
- If the problem cannot be reproduced, explicitly state this
