# Observe — 观察

**目的**：收集客观的代码运行状态数据。**必须实际运行代码，不可仅做静态分析。**

## 核心流程

1. 先运行代码拿到实际输出和错误
2. 在关键位置插桩并重新运行
3. 用实际运行时数据驱动后续判断

## 插桩工具（`scripts/observe_helpers.py`）

```python
from observe_helpers import snapshot, type_check, boundary_check, trace_call, watch_expr, DataFlowLogger
```

| 函数 | 用途 | 示例 |
|------|------|------|
| `snapshot(var, name)` | 记录变量当前值、类型、长度 | `snapshot(result, "result")` |
| `type_check(var, name, expected=(list,dict))` | 检查类型是否匹配 | `type_check(config, "config", expected=dict)` |
| `boundary_check(i, len(lst))` | 检查索引是否越界 | `boundary_check(idx, len(items))` |
| `trace_call(iteration=N)` | 装饰器：记录函数调用参数、返回值、耗时 | `@trace_call(iteration=1)` |
| `watch_expr(lambda: x > 0, "x>0")` | 条件为真时才输出 | `watch_expr(lambda: i > threshold, f"i={i}")` |
| `DataFlowLogger(name)` | 追踪变量在多个阶段的变化 | 见下方示例 |

**DataFlowLogger 示例：**
```python
dfl = DataFlowLogger("result", iteration=1)
result = step1(input_data)
dfl.log("after_step1", result)
result = step2(result)
dfl.log("after_step2", result)
dfl.summary()  # 自动对比各阶段变化
```

所有函数的日志前缀为 `[OBSERVE]`，迭代号通过 `iteration=N` 参数传入。

## 按错误类型选择观察策略

### IndexError / 越界

```python
print(f"[OBSERVE] {func} | len={len(my_list)}, index={i}")
boundary_check(i, len(my_list))
```

### TypeError / AttributeError

```python
type_check(obj, "obj", expected=dict)  # 检查类型
if obj is None:
    print(f"[OBSERVE] {func} | obj is None!")
```

### 值不对 / 逻辑错误

```python
dfl = DataFlowLogger("value", iteration=1)
dfl.log("input", value)
# ... 中间处理 ...
dfl.log("output", value)
dfl.summary()
```

### 最近改动引入的 bug

```bash
git diff HEAD~3 --stat     # 哪些文件被改了
git diff HEAD~1             # 具体改了什么
git blame <file>:<line>     # 谁改的这行
git log -L 40,50:<file>     # 这段代码的修改历史
```

## 观察原则

- 每个日志标注观察目的
- 优先观察错误点附近，逐步向外扩展
- 不只看报错变量，还要看上游数据来源
- 复杂对象记录 `type`/`len`/`repr`（截断）

## 输出格式

```markdown
### 观察记录 #N

**观察目的**：[为什么观察]
**观察位置**：`[file]:[line]`
**观察手段**：[snapshot/type_check/git diff/...]
**观察内容**：
<运行输出和数据>
```
