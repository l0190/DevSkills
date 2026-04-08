## SKILLS组成
your-skill-name/
├── SKILL.md          # 必须,主文件
├── scripts/          # 可选,可执行脚本(首选bash)
│   ├── process_data.py
│   └── validate.sh
├── references/       # 可选,按需加载的文档
│   ├── api-guide.md
│   └── examples/
└── assets/           # 可选,模板、字体、图标等
    └── report-template.md

- references下面可以添加新的文件夹,只需要在SKILL.md中进行说明即可
- 告诉AI应该怎么做,但是更应该告诉他什么不要做(并附上不要做的理由)

## Harness 组成
OODA循环:观察-判断-决策-行动
Harness(给agent的驾驶舱) = Tools + Knowledge + Observation + Action Interfaces + Permissions
- Tools(Function Call):
    - 文件读写、shell(执行)、网络获取/搜索
    - Skill、Task、Worktree
    - SubAgent、Spwarm
- Action(Agent用户手册):CLI命令、API调用、UI交互(Devtools依赖DOM)
- Observation:git diff、错误日志、浏览器状态、传感器数据
- Knowledge:产品文档、领域资料、API规范、风格指南
    - 不同领域有不同领域的调试器(logger)
    - 之前的前后端建模与结构化文档生成思路是有用的
    - 使用渐进式披露,即用多级目录的形式构建不同层级的项目描述文档.
- Permissions:沙箱隔离、审批流程、信任边界
- 整个项目满足**奥卡姆剃刀原则**

通过状态机建立审批机制
- 制作调试器:以装饰器的模式添加到代码中,显示事件类型,位置信息,关键变量的状态,函数返回值、调用链
    - 自定义python库函数,用于实现调试器和调用链,装饰器
    - 让AI控制Vscode生成断点/trace
- 测试驱动开发:修改过程中添加必要的注释,小的目标达成后形成可审阅的md文档
    - 生成阶段生成软件架构的同时生成接口测试用例:设计文档中只有接口和功能描述
    - 将具体小模块的开发看成一个巨大的debug,边开发边生成新的测试
- 制作架构图绘图工具:将容器翻译成代码

## 参考资料:
- https://github.com/shareAI-lab/learn-claude-code.git
- https://github.com/shareAI-lab/claw0.git

- https://github.com/Donchitos/Claude-Code-Game-Studios
- https://github.com/toukanno/claude-code-game-studios