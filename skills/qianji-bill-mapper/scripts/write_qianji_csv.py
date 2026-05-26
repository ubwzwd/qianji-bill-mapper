#!/usr/bin/env python3
"""
把交易列表写成钱迹可导入的 CSV。

用法:
    python write_qianji_csv.py transactions.json output.csv

transactions.json 是一个数组，每个元素是一笔交易，字段名与钱迹列一一对应
（缺失字段当作空）。脚本负责：
  - 强制 13 列、固定列顺序
  - 校验「类型」「金额」等关键字段
  - UTF-8 带 BOM 输出（钱迹导入要求）
  - 用 \r\n 行尾，与官方模板一致

每笔交易支持的键（全部可选，除了 时间/类型/金额 建议必填）：
  时间, 分类, 二级分类, 类型, 金额, 账户1, 账户2,
  备注, 账单标记, 手续费, 优惠券, 标签, 账单图片
"""
import csv
import json
import sys

COLUMNS = ["时间", "分类", "二级分类", "类型", "金额", "账户1", "账户2",
           "备注", "账单标记", "手续费", "优惠券", "标签", "账单图片"]

# 官方支持 5 种类型
VALID_TYPES = {"收入", "支出", "报销", "转账", "还款"}
# 这些类型需要/可用「账户2」（转入账户）
TYPES_NEED_ACCOUNT2 = {"转账", "还款"}
# 手续费仅支持这些类型
TYPES_ALLOW_FEE = {"转账", "还款"}


def main():
    if len(sys.argv) != 3:
        sys.exit("用法: python write_qianji_csv.py <transactions.json> <output.csv>")

    in_path, out_path = sys.argv[1], sys.argv[2]
    with open(in_path, encoding="utf-8") as f:
        txns = json.load(f)

    if not isinstance(txns, list):
        sys.exit("错误: JSON 顶层必须是数组")

    warnings = []
    rows = []
    for i, t in enumerate(txns, 1):
        if not isinstance(t, dict):
            sys.exit(f"错误: 第 {i} 笔不是对象")

        # 未知键提醒（不致命，避免拼写错误悄悄丢数据）
        for k in t:
            if k not in COLUMNS:
                warnings.append(f"第 {i} 笔有未知字段「{k}」，已忽略")

        typ = str(t.get("类型", "")).strip()
        if typ and typ not in VALID_TYPES:
            warnings.append(f"第 {i} 笔类型「{typ}」非法（应为 收入/支出/报销/转账/还款）")
        if not typ:
            warnings.append(f"第 {i} 笔缺少「类型」")

        amt = t.get("金额", "")
        if amt == "" or amt is None:
            warnings.append(f"第 {i} 笔缺少「金额」")
        else:
            # 清理千分位逗号、货币符号、空格，输出纯数字字符串
            raw = str(amt).strip()
            cleaned = raw.replace(",", "").replace(" ", "")
            for sym in ("¥", "￥", "$", "€", "£", "S$", "RM", "HK$", "US$", "CNY", "RMB"):
                cleaned = cleaned.replace(sym, "")
            try:
                v = float(cleaned)
                if v < 0:
                    warnings.append(f"第 {i} 笔金额为负数（{raw}），钱迹金额应为正数，"
                                    f"方向由「类型」决定")
                t["金额"] = cleaned  # 写回清理后的值
            except ValueError:
                warnings.append(f"第 {i} 笔金额「{raw}」不是数字")

        if typ in TYPES_NEED_ACCOUNT2 and not str(t.get("账户2", "")).strip():
            label = "信用卡还款" if typ == "还款" else "转账"
            warnings.append(f"第 {i} 笔是{label}但缺少「账户2」（转入账户）")

        # 手续费仅支持 转账/还款
        if str(t.get("手续费", "")).strip() and typ not in TYPES_ALLOW_FEE:
            warnings.append(f"第 {i} 笔填了「手续费」，但仅 转账/还款 类型支持，其余会被忽略")
        # 优惠券不支持收入类型
        if str(t.get("优惠券", "")).strip() and typ == "收入":
            warnings.append(f"第 {i} 笔填了「优惠券」，但收入类型不支持")

        rows.append([str(t.get(c, "") if t.get(c) is not None else "") for c in COLUMNS])

    # UTF-8 带 BOM + \r\n，与官方模板一致
    with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(COLUMNS)
        w.writerows(rows)

    print(f"✓ 已写入 {len(rows)} 笔交易 -> {out_path}")
    if warnings:
        print(f"\n⚠ {len(warnings)} 条提醒（请人工核对）:")
        for wmsg in warnings:
            print("  - " + wmsg)


if __name__ == "__main__":
    main()
