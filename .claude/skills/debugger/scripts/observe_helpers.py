"""
OJDE Debugger - 观察辅助工具集

提供多种观察手段，供 OJDE 循环的 Observe 阶段使用。
使用方式：在需要观察的代码位置导入并调用相应函数。

用法示例:
    from observe_helpers import snapshot, trace_call, watch_expr, type_check

    # 变量快照
    snapshot(my_var, "my_var", depth=2)

    # 条件观察
    watch_expr(lambda: my_list[i] > threshold, f"list[{i}]={my_list[i]}", iteration=1)

    # 类型检查
    type_check(obj, "obj", expected=(list, tuple))
"""

import json
import time
from datetime import datetime
from functools import wraps
from typing import Any, Optional, Tuple


# ============================================================================
# 变量快照
# ============================================================================

def snapshot(
    var: Any,
    name: str,
    *,
    max_len: int = 100,
    tag: str = "OBSERVE",
    iteration: int = 0,
) -> None:
    """记录变量在当前时刻的完整状态。

    Args:
        var: 要记录的变量
        name: 变量名（用于日志标识）
        max_len: 列表/字符串的最大显示长度
        tag: 日志前缀标签
        iteration: 当前 OJDE 迭代号
    """
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]

    info: dict[str, object] = {
        "name": name,
        "type": type(var).__name__,
        "value": _safe_repr(var, max_len=max_len),
    }

    # 类型特定信息
    if hasattr(var, "shape"):
        info["shape"] = str(var.shape)
    if hasattr(var, "dtype"):
        info["dtype"] = str(var.dtype)
    if isinstance(var, (list, tuple, set, dict, str, bytes)):
        info["len"] = int(len(var))

    print(f"[{tag}] {ts} | iter#{iteration} | SNAPSHOT: {json.dumps(info, ensure_ascii=False)}")


# ============================================================================
# 条件观察（只在条件满足时输出）
# ============================================================================

def watch_expr(
    condition: Any,
    expr_desc: str,
    *,
    tag: str = "OBSERVE",
    iteration: int = 0,
    once: bool = True,
    _counter: dict = {},  # type: ignore
) -> bool:
    """条件观察：只在 condition 为真时输出日志。

    Args:
        condition: 布尔值或可调用对象，为真时输出
        expr_desc: 条件的表达式描述
        tag: 日志前缀
        iteration: OJDE 迭代号
        once: 是否只触发一次（同一 expr_desc）
    """
    cond_val = condition() if callable(condition) else condition

    if cond_val:
        key = f"{expr_desc}:{iteration}"
        if once and _counter.get(key, 0) >= 1:
            return False
        _counter[key] = _counter.get(key, 0) + 1

        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{tag}] {ts} | iter#{iteration} | WATCH: {expr_desc} → TRUE")
        return True

    return False


# ============================================================================
# 函数追踪装饰器
# ============================================================================

def trace_call(
    tag: str = "OBSERVE",
    iteration: int = 0,
    log_args: bool = True,
    log_return: bool = True,
    log_duration: bool = True,
    max_repr_len: int = 200,
):
    """函数追踪装饰器：记录函数调用的参数、返回值和耗时。

    Args:
        tag: 日志前缀
        iteration: OJDE 迭代号
        log_args: 是否记录参数
        log_return: 是否记录返回值
        log_duration: 是否记录耗时
        max_repr_len: 参数/返回值的最大显示长度
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]

            if log_args:
                args_str = ", ".join(
                    _safe_repr(a, max_len=max_repr_len) for a in args
                )
                kwargs_str = ", ".join(
                    f"{k}={_safe_repr(v, max_len=max_repr_len)}" for k, v in kwargs.items()
                )
                all_args = ", ".join(filter(None, [args_str, kwargs_str]))
                print(f"[{tag}] {ts} | iter#{iteration} | CALL {func.__name__}({all_args})")

            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start

            ts2 = datetime.now().strftime("%H:%M:%S.%f")[:-3]

            parts = [f"RETURN {func.__name__}"]
            if log_return:
                parts.append(f"→ {_safe_repr(result, max_len=max_repr_len)}")
            if log_duration:
                parts.append(f"({elapsed*1000:.1f}ms)")

            print(f"[{tag}] {ts2} | iter#{iteration} | {' '.join(parts)}")
            return result
        return wrapper
    return decorator


# ============================================================================
# 类型检查
# ============================================================================

def type_check(
    var: Any,
    name: str,
    expected: Optional[Tuple[type, ...]] = None,
    *,
    tag: str = "OBSERVE",
    iteration: int = 0,
) -> bool:
    """检查变量类型，记录类型信息。

    Args:
        var: 要检查的变量
        name: 变量名
        expected: 期望的类型元组，如果不符合会额外标记
        tag: 日志前缀
        iteration: OJDE 迭代号

    Returns:
        True 如果类型符合预期（或未指定预期）
    """
    actual_type = type(var)
    matches = expected is None or isinstance(var, expected)
    status = "OK" if matches else "MISMATCH"

    info: dict[str, object] = {
        "name": name,
        "actual": actual_type.__name__,
        "status": status,
    }
    if expected:
        info["expected"] = [t.__name__ for t in expected]
    if var is None:
        info["warning"] = "Variable is None!"

    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{tag}] {ts} | iter#{iteration} | TYPE_CHECK: {json.dumps(info, ensure_ascii=False)}")
    return matches


# ============================================================================
# 边界检查
# ============================================================================

def boundary_check(
    index: int,
    container_len: int,
    index_name: str = "index",
    container_name: str = "container",
    *,
    tag: str = "OBSERVE",
    iteration: int = 0,
) -> bool:
    """检查索引是否在容器范围内。

    Args:
        index: 索引值
        container_len: 容器长度
        index_name: 索引变量名
        container_name: 容器变量名
        tag: 日志前缀
        iteration: OJDE 迭代号

    Returns:
        True 如果索引在合法范围内
    """
    valid = 0 <= index < container_len
    status = "OK" if valid else "OUT_OF_RANGE"

    info = {
        "index": index,
        "range": f"[0, {container_len})",
        "status": status,
        "vars": f"{index_name}[{index}] in {container_name}(len={container_len})",
    }

    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{tag}] {ts} | iter#{iteration} | BOUNDARY: {json.dumps(info, ensure_ascii=False)}")
    return valid


# ============================================================================
# 数据流记录
# ============================================================================

class DataFlowLogger:
    """记录变量在多个位置的变化，用于追踪数据流。

    用法:
        dfl = DataFlowLogger("result", iteration=1)
        dfl.log("after_step1", result)
        dfl.log("after_step2", result)
        dfl.log("after_step3", result)
        dfl.summary()  # 打印对比摘要
    """

    def __init__(self, var_name: str, iteration: int = 0, tag: str = "OBSERVE"):
        self.var_name = var_name
        self.iteration = iteration
        self.tag = tag
        self.records = []

    def log(self, stage: str, value: Any) -> None:
        """在某个阶段记录变量值。"""
        self.records.append({
            "stage": stage,
            "value": _safe_repr(value),
            "type": type(value).__name__,
            "len": len(value) if hasattr(value, "__len__") else None,
        })
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(
            f"[{self.tag}] {ts} | iter#{self.iteration} | "
            f"DATAFLOW {self.var_name}@{stage} = {_safe_repr(value)}"
        )

    def summary(self) -> None:
        """打印所有阶段的对比摘要。"""
        if len(self.records) < 2:
            print(f"[{self.tag}] DATAFLOW {self.var_name}: 只有一个记录点，无法对比")
            return

        print(f"\n[{self.tag}] === DataFlow Summary: {self.var_name} ===")
        for r in self.records:
            print(f"  {r['stage']}: {r['value']} (type={r['type']}, len={r['len']})")

        # 检测变化
        for i in range(1, len(self.records)):
            prev = self.records[i - 1]
            curr = self.records[i]
            changed = prev["value"] != curr["value"]
            marker = "CHANGED" if changed else "UNCHANGED"
            print(f"  {prev['stage']} → {curr['stage']}: {marker}")
        print(f"[{self.tag}] === End Summary ===\n")


# ============================================================================
# 内部工具函数
# ============================================================================

def _safe_repr(obj: Any, max_len: int = 200) -> str:
    """安全地将对象转换为字符串表示，避免过长或递归。"""
    try:
        r = repr(obj)
        if len(r) > max_len:
            r = r[:max_len] + f"... (truncated, total {len(r)} chars)"
        return r
    except Exception:
        return f"<{type(obj).__name__} (repr failed)>"
