# Observe — 观察

**目的**：收集客观的代码运行状态数据。**必须实际运行代码，不可仅做静态分析。**

## 核心流程

1. 先运行代码拿到实际输出和错误
2. 用装饰器插桩关键函数并重新运行
3. 用实际运行时数据驱动后续判断

## 装饰器工具（`scripts/observe_helpers.py`）

所有工具均以装饰器为主，调试完成后移除装饰器即可，无需手动清理 print。

```python
from observe_helpers import observe, type_check, boundary_check, watch, dataflow, snapshot
```

| 装饰器 | 用途 | 示例 |
|--------|------|------|
| `@observe` | 追踪函数调用（参数、返回值、耗时） | `@observe(iteration=1)` |
| `@type_check` | 检查参数/返回值类型 | `@type_check(expected_input=dict, iteration=1)` |
| `@boundary_check` | 检查索引是否越界 | `@boundary_check("items", iteration=1)` |
| `@watch` | 条件满足时才输出日志 | `@watch(lambda x: x > 0, "x>0")` |
| `@dataflow` | 追踪函数内变量的变化 | `@dataflow("result", iteration=1)` |
| `snapshot()` | 独立快照函数（内联场景） | `snapshot(var, "var", iteration=1)` |

### observe — 函数追踪

```python
@observe(iteration=1)
def process(data):
    return transform(data)
# 输出: [OBSERVE] ... | CALL process(data_repr)
# 输出: [OBSERVE] ... | RETURN process -> result_repr (12.3ms)
```

### type_check — 类型检查

```python
@type_check(expected_input=(dict, list), expected_return=dict, iteration=1)
def merge(a, b):
    return {**a, **b}
# 输出: [OBSERVE] ... | TYPE_CHECK: merge input: OK / MISMATCH: ...
# 输出: [OBSERVE] ... | TYPE_CHECK: merge return: OK / MISMATCH: ...
```

自动检测 None 参数并警告。

### boundary_check — 边界检查

```python
@boundary_check("items", iteration=1)          # 自动检测 list/tuple
def get_first(items):
    return items[0]

@boundary_check("items", index_arg="idx", iteration=1)  # 指定索引参数
def get_at(items, idx):
    return items[idx]
# 输出: [OBSERVE] ... | BOUNDARY: get_at: items.len=7, idx=3, OK
```

### watch — 条件观察

```python
@watch(lambda x: x > 100, "x exceeds threshold", iteration=1)
def compute(x):
    return x * 2
# 只在 x > 100 时输出: [OBSERVE] ... | WATCH: compute(150): x exceeds threshold
```

### dataflow — 数据流追踪

在函数内用 `self._snapshot(value, stage)` 记录中间值：

```python
@dataflow("score", iteration=1)
def calculate(raw, _snapshot=None):  # 必须声明 _snapshot 参数
    normalized = _snapshot(raw / 2, "normalized")
    weighted = _snapshot(normalized * 0.8, "weighted")
    return weighted
# 调用: calculate(100)  → _snapshot 由装饰器自动注入
# 输出各阶段值 + 自动对比变化: CHANGED / UNCHANGED
```

### snapshot — 独立快照（内联场景）

装饰器不方便时，可用独立函数：

```python
snapshot(my_var, "my_var", iteration=1)
```

所有日志前缀为 `[OBSERVE]`，迭代号通过 `iteration=N` 传入。

## 按错误类型选择装饰器

### IndexError / 越界

```python
@boundary_check("items", index_arg="i", iteration=1)
def get_score(items, i):
    return items[i]
```

### TypeError / AttributeError

```python
@type_check(expected_input=dict, expected_return=dict, iteration=1)
def merge_configs(default, user):
    return {**default, **user}
```

### 值不对 / 逻辑错误

```python
@dataflow("value", iteration=1)
def calculate(price, level):
    base = self._snapshot(PRICES[level], "base")
    final = self._snapshot(base * 0.9, "final")
    return final
```

### 最近改动引入的 bug

```bash
git diff HEAD~3 --stat     # 哪些文件被改了
git diff HEAD~1             # 具体改了什么
git blame <file>:<line>     # 谁改的这行
git log -L 40,50:<file>     # 这段代码的修改历史
```

## 观察原则

- 每个装饰器标注观察目的（通过 desc 参数或注释）
- 优先装饰错误点附近的函数，逐步向外扩展
- 不只看报错函数，还要装饰其上游调用者
- 复杂对象会自动截断 repr

## 输出格式

```markdown
### 观察记录 #N

**观察目的**：[为什么观察]
**观察位置**：`[file]:[line]`
**观察手段**：[@observe / @type_check / git diff / ...]
**观察内容**：
<运行输出和数据>
```
