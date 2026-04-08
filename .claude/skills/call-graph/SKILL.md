---
name: call-graph
description: 为Python项目生成函数调用树，可视化执行流程和代码结构。务必在以下场景触发：用户想了解代码执行流程、追踪函数调用、分析调用链、可视化代码流、查找入口点、调试复杂执行路径；用户提到"调用图"、"调用树"、"函数追踪"、"执行流程"、"调用链"、"代码是怎么运行的"、"有哪些函数被调用了"、"分析代码结构"、"trace"、"call graph"、"call tree"、"function trace"。
---

# Python 函数调用图生成器

本技能使用 `trace_call_tree.py` 通过 `sys.setprofile` 追踪 Python 函数调用，输出结构化的调用树，帮助快速理解项目执行流程。

## 适用场景

- 理解陌生代码库的执行流程
- 分析某个入口点调用了哪些函数
- 调试复杂的调用链
- 对比实际运行时调用路径与静态代码结构的差异
- 验证重构后的代码是否遵循预期的执行路径

## 工作原理

追踪器使用 Python 的 `sys.setprofile` 钩子在运行时捕获每一次函数调用和返回。它会过滤掉标准库和第三方库的调用，只保留**项目内部**的调用，然后格式化为缩进树形结构。

## 使用方法

```bash
# 基本用法：从 main() 开始追踪
python .claude/skills/call-graph/scripts/trace_call_tree.py \
  --entry path/to/script.py \
  --project-root path/to/project

# 指定其他入口函数
python .claude/skills/call-graph/scripts/trace_call_tree.py \
  --entry path/to/script.py \
  --main-func run_server \
  --project-root path/to/project

# 追踪模块级代码（无需 main 函数）
python .claude/skills/call-graph/scripts/trace_call_tree.py \
  --entry path/to/script.py \
  --module-exec \
  --project-root path/to/project

# 自定义输出路径
python .claude/skills/call-graph/scripts/trace_call_tree.py \
  --entry path/to/script.py \
  --output my_call_tree.log
```

## 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| `--entry` | 是 | - | Python 入口文件路径 |
| `--main-func` | 否 | `main` | 入口函数名称 |
| `--project-root` | 否 | `.` | 项目根目录，用于过滤内部调用 |
| `--output` | 否 | `call_tree.log` | 输出日志文件路径 |
| `--module-exec` | 否 | `false` | 追踪模块级代码，无需 main() 函数 |
| `--` 分隔符 | 否 | - | `--` 之后的参数会转发给入口脚本 |

## 输出格式

输出为缩进树形结构，显示函数名称和调用次数：

```
├── module.py:main [count=1]
│   ├── module.py:process_data [count=3]
│   │   ├── module.py:validate [count=3]
│   │   └── module.py:transform [count=2]
│   └── module.py:write_output [count=1]
```

每个节点显示：
- **文件路径**（相对于项目根目录）
- **函数/方法名**（包含类名，如 `MyClass.my_method`）
- **调用次数** — 该函数在其父节点中被调用的次数

## 执行流程

当用户要求追踪或理解代码执行流程时：

1. **确定入口点** — 找到项目中的 `main()` 函数或相关入口脚本。
2. **确定项目根目录** — 使用项目顶层目录，确保追踪器正确过滤内部与外部调用。
3. **运行追踪器** — 使用合适的参数执行 `trace_call_tree.py`。如果目标脚本需要参数，在 `--` 之后传入。
4. **读取并展示输出** — 读取生成的 `call_tree.log` 文件，向用户解释执行结构。
5. **分析** — 高亮关键调用链、热点路径（高调用次数）以及任何异常模式。

## 注意事项

- 追踪器捕获的是**运行时**调用，未被执行到的代码路径（如未触发的异常处理）不会出现在调用树中。
- `--module-exec` 标志适用于在模块级别运行逻辑而非通过 `main()` 函数的脚本。
- 追踪器会过滤掉 `site-packages/`、`dist-packages/` 以及虚拟环境目录（`env/`、`venv/`、`.venv/`）中的调用。
- 对于多线程代码，追踪器会对所有线程进行 profile 并将结果合并到同一棵调用树中。
