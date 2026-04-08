## Skill结构
- skill本质上是一个存放脚本,文档和assets的文件夹

``` bash
  skill-name/
  ├── SKILL.md          # 必须,主文件
  ├── scripts/          # 可选,可执行脚本(首选bash)
  │   ├── process_data.py
  │   └── validate.sh
  ├── references/       # 可选,按需加载的文档
  │   ├── api-guide.md
  │   └── examples/
  └── assets/           # 可选,模板、字体、图标等
      └── template.md
```

## Skills迁移方式
迁移方式:将skill移动到AI编程工具对应的skills存放目录下

| 工具       | Skills 存放目录        |
| ------------ | -------------------- |
| ClaudeCode | `.claude/skills/`  |
| OpenCode   | `opencode/skills/` |
| Copilot    | `.github/skills`   |

## 已有Skills

| Skill | 说明 | 链接 |
| ------------ | -------------------- | ---- |
| OODA-debugger | 基于OODA循环的LLM自动化调试技能 | [中文版](.claude/skills-CN/OODA-debugger/) \| [English](.claude/skills/OODA-debugger/) |
| call-graph | Python函数调用树生成工具 | [中文版](.claude/skills-CN/call-graph/) \| [English](.claude/skills/call-graph/) |

## 相关文档

- [English README](README_EN.md)
- [设计文档(中文)](assets/CN/skills.md)
- [Debugger设计原理(中文)](assets/CN/debugger.md)
- [软件系统分析方法(中文)](assets/CN/analysis.md)
- [English Docs](assets/EN/skills.md) \| [Debugger](assets/EN/debugger.md) \| [Analysis](assets/EN/analysis.md)
- [LICENSE](LICENSE) (MIT)
