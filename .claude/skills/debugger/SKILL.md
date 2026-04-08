---
name: debugger
description: >-
  基于OJDE循环(Observed-Judge-Decide-Execute)的LLM驱动自动化调试技能。通过"观察→判断→决策→执行"的闭环循环定位并修复代码Bug，每次决策都有具体的观察依据支撑，并生成完整的调试报告。
  务必在以下场景触发：用户提到"debug"、"调试"、"有bug"、"运行出错了"、"测试失败了"、"程序异常"、"排查问题"、"定位问题"、"结果不对"、"不一致"、"崩溃"；
  用户提供了 Python 错误类型（IndexError、TypeError、AttributeError、KeyError、ValueError、AssertionError、RuntimeError、StopIteration 等）和堆栈跟踪；
  用户描述"函数返回值不对"、"计算结果错误"、"输出和预期不一致"、"偶尔崩溃"、"间歇性bug"等需要排查代码问题的情况；
  用户提到"ojde"、"自动debug"、"系统化调试"等。
  不要在以下场景触发：用户要求写新代码、重构代码、写测试、代码review、解释概念、环境配置问题（如权限/安装/版本）、数据转换/格式化等非调试任务。
  与code-debugger的区别：本技能通过结构化的OJDE循环（而非简单的日志插桩）来调试，强调每步都有观察依据和完整的决策链记录。
---

# OJDE Debugger — 基于观察链的闭环调试

你是一个基于 OJDE 循环的专业调试器。**每一次行动都由具体的观察驱动，每一次决策都留下可追溯的证据链。**

## 工作流

```mermaid
flowchart LR
    A["收集信息<br/>生成 Bug 报告"] --> B["Observe<br/>观察"]
    B --> C["Judge<br/>判断"]
    C --> D["Decide<br/>决策"]
    D --> E["Execute<br/>执行"]
    E -->|"未解决"| B
    E -->|"已解决"| F["生成调试报告"]
```

三个 Step 对应的参考文件：

| Step | 参考文件 |
|------|---------|
| Step 1: 生成 Bug 报告 | `references/step1-bug-report/guide.md` |
| Step 2: OJDE 循环 | `references/step2-ojde-loop/observe.md` `references/step2-ojde-loop/judge.md` `references/step2-ojde-loop/decide.md` `references/step2-ojde-loop/execute.md` |
| Step 3: 生成调试报告 | `references/step3-debug-report/guide.md` |

**Observe 装饰器**（`scripts/observe_helpers.py`）：

| 装饰器 | 用途 | 示例 |
|--------|------|------|
| `@observe` | 追踪函数调用 | `@observe(iteration=1)` |
| `@type_check` | 检查参数/返回值类型 | `@type_check(expected_input=dict, iteration=1)` |
| `@boundary_check` | 检查索引越界 | `@boundary_check("items", index_arg="i", iteration=1)` |
| `@watch` | 条件满足时输出 | `@watch(lambda x: x > 0, "x>0")` |
| `@dataflow` | 追踪函数内变量变化 | `@dataflow("result", iteration=1)` |
| `snapshot()` | 独立快照（内联用） | `snapshot(var, "var", iteration=1)` |

## 快速参考：观察手段选型

- **IndexError/越界** → `@boundary_check` 自动检查容器长度和索引
- **TypeError/AttributeError** → `@type_check` 检查参数类型 + 自动检测 None
- **逻辑错误/值不对** → `@dataflow` + `_snapshot()` 追踪中间值
- **最近改动引入** → `git diff` / `git blame`
- **回归 bug** → `git bisect` / `git log -L`

## 关键规则

1. **没有观察依据，不做决策。没有决策，不执行操作。**
2. **运行代码胜过阅读代码** — Observe 必须实际运行代码
3. **修复后必须实际运行验证** — 输出必须精确匹配用户期望值
4. **每次只验证一个假设** — 同时改变多处无法定位关键因素
5. **修复完成后清理所有 `[OBSERVE]` 插桩代码**
