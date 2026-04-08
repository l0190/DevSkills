#!/usr/bin/env python3
import argparse
import importlib.util
import os
import sys
import threading
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class CallNode:
    func_id: str
    display_name: str
    count: int = 0
    children: Dict[str, "CallNode"] = field(default_factory=dict)


class CallTreeTracer:
    def __init__(self, project_root: Path, entry_file: Path, main_func: str, module_exec: bool = False) -> None:
        self.project_root = project_root.resolve()
        self.entry_file = entry_file.resolve()
        self.main_func = main_func
        self.module_exec = module_exec
        self.root = CallNode("ROOT", "ROOT")
        self.lock = threading.Lock()
        self.thread_local = threading.local()

    def _get_state(self) -> dict:
        state = getattr(self.thread_local, "state", None)
        if state is None:
            state = {
                "started": self.module_exec,
                "trace_depth": 0,
                "frame_stack": [],
                "node_stack": [self.root],
            }
            self.thread_local.state = state
        return state

    def _normalize_path(self, filename: Optional[str]) -> Optional[Path]:
        if not filename:
            return None
        try:
            return Path(filename).resolve()
        except OSError:
            return None

    def _is_project_file(self, filename: Optional[str]) -> bool:
        path = self._normalize_path(filename)
        if path is None:
            return False
        try:
            rel_path = path.relative_to(self.project_root)
        except ValueError:
            return False

        if path.suffix != ".py":
            return False

        rel_parts = rel_path.parts
        if rel_parts and rel_parts[0] in {"env", "venv", ".venv"}:
            return False

        path_text = path.as_posix()
        if "/site-packages/" in path_text or "/dist-packages/" in path_text:
            return False

        return True

    def _is_entry_main(self, frame) -> bool:
        filename = self._normalize_path(frame.f_code.co_filename)
        return (
            filename == self.entry_file
            and frame.f_code.co_name == self.main_func
        )

    def _func_id(self, frame) -> str:
        filename = self._normalize_path(frame.f_code.co_filename)
        rel_path = filename.relative_to(self.project_root).as_posix()
        qualname = getattr(frame.f_code, "co_qualname", frame.f_code.co_name)
        lineno = frame.f_code.co_firstlineno
        return f"{rel_path}:{lineno}:{qualname}"

    def _display_name(self, frame) -> str:
        filename = self._normalize_path(frame.f_code.co_filename)
        rel_path = filename.relative_to(self.project_root).as_posix()
        # co_qualname (Python 3.11+) already includes class name, e.g. "MyClass.my_method"
        qualname = getattr(frame.f_code, "co_qualname", None)
        if qualname is not None:
            return f"{rel_path}:{qualname}"
        # Fallback for Python < 3.11: infer class name from self/cls in locals
        func_name = frame.f_code.co_name
        local_vars = frame.f_locals
        if "self" in local_vars:
            cls_name = type(local_vars["self"]).__name__
            return f"{rel_path}:{cls_name}.{func_name}"
        if "cls" in local_vars:
            cls_obj = local_vars["cls"]
            cls_name = cls_obj.__name__ if isinstance(cls_obj, type) else str(cls_obj)
            return f"{rel_path}:{cls_name}.{func_name}"
        return f"{rel_path}:{func_name}"

    def _handle_call(self, frame) -> None:
        state = self._get_state()
        is_project = self._is_project_file(frame.f_code.co_filename)

        if not state["started"]:
            if self.module_exec:
                if not is_project:
                    return
                state["started"] = True
            else:
                if not (is_project and self._is_entry_main(frame)):
                    return
                state["started"] = True

        if not is_project:
            return

        node_key = self._func_id(frame)
        node_name = self._display_name(frame)

        with self.lock:
            parent = state["node_stack"][-1]
            child = parent.children.get(node_key)
            if child is None:
                child = CallNode(node_key, node_name)
                parent.children[node_key] = child
            child.count += 1

        state["trace_depth"] += 1
        state["frame_stack"].append(frame)
        state["node_stack"].append(child)

    def _handle_return(self, frame) -> None:
        state = self._get_state()
        if not state["started"]:
            return

        if state["frame_stack"] and state["frame_stack"][-1] is frame:
            state["frame_stack"].pop()
            state["node_stack"].pop()
            state["trace_depth"] -= 1

            if state["trace_depth"] == 0:
                state["started"] = False

    def profile(self, frame, event, arg):
        if event == "call":
            self._handle_call(frame)
        elif event in {"return", "exception"}:
            self._handle_return(frame)
        return self.profile

    def format_tree(self) -> str:
        lines: List[str] = []

        def walk(node: CallNode, prefix: str) -> None:
            children = list(node.children.values())
            total = len(children)
            for index, child in enumerate(children):
                connector = "└── " if index == total - 1 else "├── "
                lines.append(f"{prefix}{connector}{child.display_name} [count={child.count}]")
                extension = "    " if index == total - 1 else "│   "
                walk(child, prefix + extension)

        walk(self.root, "")
        return "\n".join(lines)


def load_module(entry_file: Path):
    module_name = f"_trace_target_{entry_file.stem}"
    spec = importlib.util.spec_from_file_location(module_name, entry_file)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module from {entry_file}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Trace project-internal function calls from main() and output a log tree."
    )
    parser.add_argument(
        "--entry",
        required=True,
        help="Path to the Python entry file that defines main().",
    )
    parser.add_argument(
        "--main-func",
        default="main",
        help="Entry function name to start tracing from.",
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Project root used to filter internal calls.",
    )
    parser.add_argument(
        "--output",
        default="call_tree.log",
        help="Output log file path.",
    )
    parser.add_argument(
        "--module-exec",
        action="store_true",
        help="Trace module-level code execution without requiring a main() function.",
    )
    parser.add_argument(
        "entry_args",
        nargs=argparse.REMAINDER,
        help="Arguments forwarded to the entry script. Prefix them with --.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    entry_file = Path(args.entry).resolve()
    output_path = Path(args.output).resolve()

    if not entry_file.exists():
        raise FileNotFoundError(f"Entry file not found: {entry_file}")

    entry_args = list(args.entry_args)
    if entry_args and entry_args[0] == "--":
        entry_args = entry_args[1:]

    sys.path.insert(0, str(project_root))
    sys.path.insert(0, str(entry_file.parent))

    tracer = CallTreeTracer(
        project_root=project_root,
        entry_file=entry_file,
        main_func=args.main_func,
        module_exec=args.module_exec,
    )

    old_argv = sys.argv[:]
    sys.argv = [str(entry_file), *entry_args]

    if args.module_exec:
        module_name = f"_trace_target_{entry_file.stem}"
        spec = importlib.util.spec_from_file_location(module_name, entry_file)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Failed to load module from {entry_file}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module

        sys.setprofile(tracer.profile)
        threading.setprofile(tracer.profile)
        try:
            spec.loader.exec_module(module)
        finally:
            sys.setprofile(None)
            threading.setprofile(None)
    else:
        target_module = load_module(entry_file)
        target_main = getattr(target_module, args.main_func, None)
        if target_main is None or not callable(target_main):
            raise AttributeError(f"{entry_file} does not define callable {args.main_func}()")

        sys.setprofile(tracer.profile)
        threading.setprofile(tracer.profile)
        try:
            target_main()
        finally:
            sys.setprofile(None)
            threading.setprofile(None)

    sys.argv = old_argv

    tree = tracer.format_tree()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(tree + ("\n" if tree else ""), encoding="utf-8")
    print(f"call tree saved to {output_path}")


if __name__ == "__main__":
    main()
