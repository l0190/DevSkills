"""
OJDE Debugger - 装饰器式观察工具集

零侵入插桩，装饰器挂在函数定义上即可。调试完成后移除装饰器即清理完毕。

用法:
    from observe_helpers import observe, type_check, boundary_check, watch, dataflow, snapshot

    @observe(iteration=1)
    def process(data):
        return transform(data)

    @type_check(expected_input=dict, expected_return=dict, iteration=1)
    def merge(a, b):
        return {**a, **b}

    @boundary_check("items", index_arg="idx", iteration=1)
    def get_at(items, idx):
        return items[idx]

    @watch(lambda r: r > 100, "result > 100", iteration=1)
    def compute(x):
        return x * 2

    @dataflow("result", iteration=1)
    def pipeline(raw, _snapshot=None):
        step1 = _snapshot(raw / 2, "half")
        return step1 * 3

    snapshot(my_var, "my_var", iteration=1)  # 内联场景
"""

import inspect
import time
from datetime import datetime
from functools import wraps


# ============================================================================
# 内部工具
# ============================================================================

def _log(tag, iteration, kind, message):
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{tag}] {ts} | iter#{iteration} | {kind}: {message}")


def _safe_repr(obj, max_len=200):
    try:
        r = repr(obj)
        return r if len(r) <= max_len else f"{r[:max_len]}... (len={len(r)})"
    except Exception:
        return f"<{type(obj).__name__} (repr failed)>"


def _resolve_args(fn, args, kwargs):
    """将 *args/**kwargs 解析为 {参数名: 值} 的字典。"""
    sig = inspect.signature(fn)
    bound = sig.bind(*args, **kwargs)
    bound.apply_defaults()
    return bound.arguments


def _try_len(obj):
    try:
        return len(obj)
    except Exception:
        return None


# ============================================================================
# observe — 函数追踪
# ============================================================================

def observe(func=None, iteration=0, tag="OBSERVE"):
    """追踪函数调用：记录参数、返回值、耗时。"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            parts = [_safe_repr(a) for a in args] + [f"{k}={_safe_repr(v)}" for k, v in kwargs.items()]
            _log(tag, iteration, "CALL", f"{fn.__name__}({', '.join(parts)})")

            start = time.perf_counter()
            result = fn(*args, **kwargs)
            elapsed_ms = (time.perf_counter() - start) * 1000

            _log(tag, iteration, "CALL", f"RETURN {fn.__name__} -> {_safe_repr(result)} ({elapsed_ms:.1f}ms)")
            return result
        return wrapper

    if func is not None:
        return decorator(func)
    return decorator


# ============================================================================
# type_check — 类型检查
# ============================================================================

def type_check(func=None, expected_input=None, expected_return=None, iteration=0, tag="OBSERVE"):
    """检查函数参数和返回值的类型，自动检测 None 参数。"""
    def _norm(t):
        if t is None:
            return None
        return t if isinstance(t, tuple) else (t,)

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            resolved = _resolve_args(fn, args, kwargs)

            none_names = [k for k, v in resolved.items() if v is None]
            if none_names:
                _log(tag, iteration, "TYPE_CHECK", f"{fn.__name__}: None in {none_names}")

            exp_in = _norm(expected_input)
            if exp_in:
                mismatched = [f"{k}={type(v).__name__}" for k, v in resolved.items() if not isinstance(v, exp_in)]
                status = "OK" if not mismatched else f"MISMATCH: {', '.join(mismatched)}"
                _log(tag, iteration, "TYPE_CHECK", f"{fn.__name__} args: {status}")

            result = fn(*args, **kwargs)

            exp_out = _norm(expected_return)
            if exp_out:
                names = "/".join(t.__name__ for t in exp_out)
                ok = "OK" if isinstance(result, exp_out) else f"MISMATCH: got {type(result).__name__}, expected {names}"
                _log(tag, iteration, "TYPE_CHECK", f"{fn.__name__} return: {ok}")

            return result
        return wrapper

    if func is not None:
        return decorator(func)
    return decorator


# ============================================================================
# boundary_check — 边界检查
# ============================================================================

def boundary_check(container_arg, index_arg=None, iteration=0, tag="OBSERVE"):
    """检查容器索引是否越界。"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            resolved = _resolve_args(fn, args, kwargs)
            container = resolved.get(container_arg)
            if container is None:
                return fn(*args, **kwargs)

            clen = _try_len(container)
            msg = f"{fn.__name__}: {container_arg}.len={clen}"

            if index_arg:
                idx = resolved.get(index_arg)
                if idx is not None:
                    valid = 0 <= idx < clen
                    msg += f", {index_arg}={idx}, {'OK' if valid else 'OUT_OF_RANGE'}"
                    _log(tag, iteration, "BOUNDARY", msg)

            return fn(*args, **kwargs)
        return wrapper

    return decorator


# ============================================================================
# watch — 条件观察
# ============================================================================

def watch(condition, desc="", arg_name=None, iteration=0, tag="OBSERVE"):
    """条件观察：只在 condition 为 True 时输出日志。默认对返回值求值。"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            result = fn(*args, **kwargs)

            target = result
            if arg_name:
                resolved = _resolve_args(fn, args, kwargs)
                target = resolved.get(arg_name, result)

            if condition(target):
                _log(tag, iteration, "WATCH", f"{fn.__name__}: {desc or 'TRUE'} (value={_safe_repr(target)})")

            return result
        return wrapper

    return decorator


# ============================================================================
# dataflow — 数据流追踪
# ============================================================================

def dataflow(label, iteration=0, tag="OBSERVE"):
    """追踪函数内变量的变化。被装饰函数需声明 _snapshot=None 参数。"""
    def decorator(fn):
        has_snapshot_param = "_snapshot" in inspect.signature(fn).parameters

        @wraps(fn)
        def wrapper(*args, **kwargs):
            records = []

            def _snapshot(value, stage=""):
                records.append({"stage": stage or f"step{len(records) + 1}", "value": _safe_repr(value), "type": type(value).__name__, "len": _try_len(value)})
                return value

            if has_snapshot_param:
                kwargs.setdefault("_snapshot", _snapshot)

            result = fn(*args, **kwargs)

            if not records:
                return result

            _log(tag, iteration, "DATAFLOW", f"--- {label} ({fn.__name__}) ---")
            for r in records:
                _log(tag, iteration, "DATAFLOW", f"  {r['stage']}: {r['value']} (type={r['type']}, len={r['len']})")

            for i in range(1, len(records)):
                prev, curr = records[i - 1], records[i]
                changed = "CHANGED" if prev["value"] != curr["value"] else "UNCHANGED"
                _log(tag, iteration, "DATAFLOW", f"  {prev['stage']} -> {curr['stage']}: {changed}")

            _log(tag, iteration, "DATAFLOW", f"--- END {label} ---")
            return result
        return wrapper

    return decorator


# ============================================================================
# snapshot — 独立快照（内联场景）
# ============================================================================

def snapshot(var, name, iteration=0, tag="OBSERVE"):
    """记录变量当前状态。用于装饰器不方便的内联场景。"""
    parts = [f"name={name}", f"type={type(var).__name__}", f"value={_safe_repr(var)}"]
    length = _try_len(var)
    if length is not None:
        parts.append(f"len={length}")
    if hasattr(var, "shape"):
        parts.append(f"shape={var.shape}")
    _log(tag, iteration, "SNAPSHOT", ", ".join(parts))
