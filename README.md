# 钱迹账单转换技能 (qianji-bill-mapper)

A Claude [Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that converts any bank or credit-card statement (PDF or image) into a CSV ready to import into the [钱迹 (Qianji)](https://www.qianjiapp.com/) personal-finance app.

把任意银行/信用卡账单（PDF 或图片）解析成钱迹 App 可直接导入的标准模板 CSV。

## 它能做什么

- 读取任意银行的 PDF / 图片账单，逐笔提取交易
- 映射进钱迹模板（13 列，UTF-8 带 BOM）
- 自动判断收支方向（支出 / 收入 / 报销 / 转账 / 还款）
- 按可自定义的分类体系推断分类，**拿不准的先汇总问用户**
- 处理信用卡还款方向、退款、外币、综合电商平台逐笔确认等实战场景

## 目录结构

本仓库按 Agent Skill 跨平台标准布局，同一份技能可在 Claude 与 OpenAI（ChatGPT / Codex）通用：

```
qianji-bill-mapper/
├── .claude-plugin/
│   └── plugin.json               # Claude Code 插件清单
└── skills/
    └── qianji-bill-mapper/       # 技能本体（SKILL.md 在此目录根部）
        ├── SKILL.md              # 技能主文件：工作流与规则
        ├── scripts/
        │   └── write_qianji_csv.py   # 从交易 JSON 生成合规 CSV（强制 BOM/列序，并做校验）
        ├── references/
        │   ├── categories.md         # 分类映射表（可自定义）+ 本地商户速查
        │   └── accounts.md           # 账户列表模板（首次使用时填入自己的账户）
        └── assets/
            └── template.csv          # 钱迹官方导入模板
```

> Codex / ChatGPT 等需要「`SKILL.md` 在文件夹根部」的环境，直接指向 `skills/qianji-bill-mapper/` 这一层即可。

## 安装

### Claude Code（通过 marketplace 一键安装，推荐）

```
/plugin marketplace add ubwzwd/claude-skills
/plugin install qianji-bill-mapper@ubwzwd-skills
```

安装后用 `/reload-plugins` 加载。技能会在你提到账单/钱迹/导入时自动触发。

### Claude.ai / Claude API（Agent Skills）

把 `skills/qianji-bill-mapper/` 这个文件夹打包成 `.zip`（或 `.skill`）上传到设置里的 Skills；或放进 API 代码执行环境的技能目录。

### OpenAI Codex CLI

把技能放到 Codex 的技能目录（个人：`~/.agents/skills/`，仓库级：`<repo>/.agents/skills/`）：

```bash
git clone https://github.com/ubwzwd/qianji-bill-mapper.git
mkdir -p ~/.agents/skills
cp -r qianji-bill-mapper/skills/qianji-bill-mapper ~/.agents/skills/
# 重启 Codex 让它发现新技能；也可在 Codex 里用 $skill-installer 从仓库安装
```

### ChatGPT

ChatGPT 已支持 Agent Skills 格式：在支持 Skills 的入口上传 `skills/qianji-bill-mapper/` 文件夹（含 `SKILL.md`、`scripts/`、`references/`、`assets/`）即可。

**给完全不写代码、只用 app 聊天的人**：建议你把它做成一个 Custom GPT，发链接给对方，对方点开就能用、零安装。完整设置步骤和可直接粘贴的 GPT 说明见 [chatgpt-gpt-setup.md](chatgpt-gpt-setup.md)。

## 使用方式

1. 按上面任一方式安装本技能。
2. 首次使用时，按提示把自己的信用卡 / 银行账户填进 `references/accounts.md`。
3. 上传一份银行账单，告诉它账户和币种（或从账户列表选），它会：
   解析交易 → 自动归类 → 把拿不准的归类汇总问你 → 生成可导入的 CSV。
4. 把生成的 CSV 按[钱迹模板导入流程](https://docs.qianjiapp.com/other/import_templete.html)导入。

> 提示：首次导入建议先小批量验证方向和分类无误，再批量导入。

## 自定义

- **分类体系**：编辑 `references/categories.md`，改成你自己钱迹账本里的分类名，避免导入后产生重复分类。
- **账户列表**：编辑 `references/accounts.md`。

## 隐私

`references/accounts.md` 在本仓库中是**通用占位模板**，不含真实账户。请在本地填入你自己的账户，不要把含真实账号/卡号的版本提交到公开仓库。

## License

MIT — 见 [LICENSE](LICENSE)。

钱迹模板文件 `assets/template.csv` 版权归钱迹所有，此处仅为方便参照。
