AI-driven software development consists of two steps: Build pseudocode (structured description documents) like solving a math problem, then translate pseudocode into the target language.

- Structured description documents should not contain language-specific details — focus on describing the project itself.
- Architecture design (interfaces + communication) -> Algorithm design (pseudocode) -> Programming language
    - Software architecture design focuses on module interface design and inter-module communication design.
    - Algorithm design here means designing the high-level steps of an algorithm (annotated with comments explaining their purpose).
- Clarify whether your task is **algorithm development** (pseudocode) or **application engineering** (architecture design) — they require different problem-solving approaches.
    - Application Engineering:
        - Translate source code analysis tasks into collecting information from source code to build project analysis documents.
    - Algorithm Development:
        - Organize logs to generate algorithm analysis reports (function call chains, key variable changes, inputs, outputs).
        - Algorithm tracing: external hyperparameters, temporary variables, input processing variables.

- The first step in software system analysis is identifying the project's entry point.
- Core modules are initialized when the software system starts. By tracing the call chain from the entry point and finding initialization calls, you can discover the modules in the software architecture.
    - Other modules can be lazily loaded after startup.
- Python script for generating function call graphs, with the following requirements:
    1. Use `sys.setprofile` for function tracing.
    2. Retain only in-project calls.
    3. Start tracing from `main`.

**Key variable information disclosure:** For small variables, return values; for large variables, output `shape()`.
