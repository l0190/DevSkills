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
