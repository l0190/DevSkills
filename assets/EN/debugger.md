## Debugger Skill Design Principles

1. Automatically generate detailed bug reports based on program execution and templates, then debug based on those reports.
2. The debugging process follows the OODA loop:
    - **O — Observe:** Collect current code execution status through source code, program state, instrumentation, logging, etc.
    - **O — Objective:** Based on observation data, confirm the specific debugging goal for this iteration — determine whether the problem exists, whether the root cause is located, whether the hypothesis holds, and clarify what this round needs to achieve.
    - **D — Decide:** Based on the confirmed objective, select the **most probable** or **easiest to verify** direction. Decide on a specific method to verify it (e.g., modify input data, add logging, write a unit test, inspect a specific code segment). Every decision must be supported by concrete observational evidence.
    - **A — Act:** Execute the decided operations (e.g., modify code, run tests). Then **immediately observe** the results to see if the issue is resolved or behavior has changed, generating new "observations" that feed into the next loop iteration.
3. Fully leverage `references` for progressive disclosure, keeping loaded markdown files as small as possible.
4. Extend the debugger by adding appropriate tool descriptions in the markdown files under `references/step2-ooda-loop/`:
    - **Embedded debuggers** can add serial debugging tools in the Observation phase to capture debug information.
    - **Compiled languages** (e.g., C, C++) compile before executing the Action phase.
    - **Domain knowledge** can be added in the Decision phase for extensibility.

## Usage

```
/debugger <code execution status / problem description>
```
