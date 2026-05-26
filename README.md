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

```
qianji-bill-mapper/
├── SKILL.md                      # 技能主文件：工作流与规则
├── scripts/
│   └── write_qianji_csv.py       # 从交易 JSON 生成合规 CSV（强制 BOM/列序，并做校验）
├── references/
│   ├── categories.md             # 分类映射表（可自定义）+ 本地商户速查
│   └── accounts.md               # 账户列表模板（首次使用时填入自己的账户）
└── assets/
    └── template.csv              # 钱迹官方导入模板
```

## 使用方式

1. 在支持 Agent Skills 的 Claude 环境中安装本技能（上传 `.skill` 包，或将本仓库内容放入技能目录）。
2. 首次使用时，按提示把自己的信用卡 / 银行账户填进 `references/accounts.md`。
3. 上传一份银行账单，告诉 Claude 账户和币种（或从账户列表选），它会：
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
