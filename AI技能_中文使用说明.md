# 最低工资复现AI技能

技能名：`minimum-wage-replication`。界面名称：最低工资论文复现与拓展。

## 你现在怎么用

在有本地文件和运行工具的Codex对话里输入下面这段话。不要把它粘贴到PowerShell终端：

```text
请使用 $minimum-wage-replication，项目在 C:\Users\ber寨\Desktop\01_DID\Table2_Python，
数据在 C:\Users\ber寨\Desktop\01_DID\data\public.csv。
请生成全部复现表图和所有权拓展，检查运行记录，并用中文解释结果与原文差异。
```

也可以不指定美元符号名称，直接请求“使用最低工资论文复现技能”。明确点名最便于验证它是否被调用。

只想讲解或核查现有结果时可以输入：

```text
请使用 $minimum-wage-replication，只检查我桌面01_DID里的现有结果并解释Table 4，不要重跑分析。
```

AI应该先定位项目和数据，再读取skill。需要重新计算时调用已验证的run_all.py；只问结果时读取现有输出。数据或项目位置不明时会询问，不会凭空造数据。

## AI应该按什么顺序做

1. 确认项目、输入路径以及你是要运行还是解释。
2. 检查Python与依赖，需要时使用项目内的虚拟环境。
3. 运行现有计算链：Table 2 → Figure 1 → Table 3 → Table 4 → 所有权拓展。
4. 核对退出状态、当前代码与输出校验和，读取真实数值。
5. 用中文说明样本、结果、复现差异和局限，给出表图位置。

skill不负责重新编写回归算法，也不会自动提交GitHub或改写Word报告。

## 文件在哪里

项目内用于提交和分享的技能文件夹是 `skills/minimum-wage-replication/`：

```text
minimum-wage-replication/
  SKILL.md
  agents/openai.yaml
  references/interpretation.md
  scripts/summarize_run.py
```

SKILL.md是AI执行说明；agents/openai.yaml是显示名称和默认提示；interpretation.md是样本、差异与解释规则；summarize_run.py只读检查现有完整运行并提取数值。

本机使用副本放在个人技能目录 `~/.agents/skills/minimum-wage-replication/`。
技能单独不包含整个分析项目。别人需要项目代码、获准使用的数据、Python依赖和支持技能的AI环境。

## 怎么验证

显式调用后，观察AI是否读取该SKILL.md、执行正确操作并给出真实输出。一个只说“我会使用技能”的回复不构成运行验证。

完整运行后，AI会读取results/workflow_run.json，并使用技能内的summarize_run.py。其成功输出包含：

- status为verified；
- files_hash_checked为39；
- paired_did的estimate约2.75；
- table4_n为357；
- primary_ownership_difference的estimate约−0.942，近似p约0.721；
- 仍保留原文差异和推断限制。

这些历史数字用于对照，不应硬编码成任何新数据的答案。文件被修改、记录失败或代码改动后，核验脚本会返回not_verified，AI应解释原因。

已完成技能结构验证、真实现有结果核验，以及改动输出和改动源代码的隔离负例测试。本机安装后的自动发现、自然语言触发与交互效果，还应通过你的显式调用确认；这与Python计算检查是不同层次的验证。

如果技能列表暂未显示，重启Codex后再查看。安装副本不会改变作业数据，也不需要修改PowerShell执行策略。

## 其他人如何使用

将项目中 `skills/minimum-wage-replication` 整个文件夹复制到自己的 `~/.agents/skills/`；或者在自己的Codex项目中放到 `.agents/skills/`，供项目内发现。两种方法选择一种，避免同名技能重复显示。确保AI有权限访问本地项目和输入。

若不使用Codex，也可以在支持读取Agent Skills的工具中使用，或直接让可运行本地代码的AI阅读SKILL.md后遵循。普通网页聊天没有本地文件/终端权限时，不能自动执行你的电脑代码，仍可以走README中的Python命令入口。

官方说明：https://learn.chatgpt.com/docs/build-skills。
