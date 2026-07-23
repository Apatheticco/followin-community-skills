# Followin Community Skills

美股社群的内容与交易运营 skill 套件 —— 基于 **Followin MCP**，把市场数据、新闻、研报、社媒与公开策略信号编排成可审核的运营成品。

> **运营优先**：运营触发 skill、审核产出、发布内容；交易相关流程必须连接独立券商工具，并经过订单级人工确认。Followin MCP 本身不执行交易。

---

## 推荐：标准 Agent Skill

[`skills/followin-us-equity-ops/`](skills/followin-us-equity-ops/) 是当前推荐入口，适用于 Codex 及兼容 Agent Skills 的客户端。一个 Skill 内按需路由七条工作流：

- 昨夜早报
- 重要事件预告
- 研报热度与目标价标准化
- Twitter/X 热门标的
- 美股交易员与分析师公开策略信号
- KOL 信号订阅
- 券商辅助交易台

每次运行都返回「可发布内容 + 证据账本 + 编辑备注 + 下次刷新条件」，避免把 MCP 原始行直接扔给运营。

```bash
cp -R skills/followin-us-equity-ops ~/.codex/skills/
```

交易台只在存在独立券商/执行工具时提交订单；没有券商工具或缺少用户指定字段时只生成 `INCOMPLETE / NOT_SUBMITTED` 订单草案。

---

## 兼容的六个 Claude Commands

| # | 文件 | 一句话定位 | 触发示例 | 单次额度 |
|---|---|---|---|---|
| **c1** | [`c1_daily-brief.md`](skills-community/c1_daily-brief.md) | 每日早报（晨报/开盘前瞻/刷新 三模式） | 「跑早報」「開盤前瞻」 | ≈7 |
| **c2** | [`c2_event-radar.md`](skills-community/c2_event-radar.md) | 週報：上周兑现回顾 + 本周事件预告 | 「週報」「本周看点」 | ≈3 |
| **c3** | [`c3_research-hot.md`](skills-community/c3_research-hot.md) | 研报热议榜 + 单标的研究笔记 | 「研報熱點」「给 NVDA 写研究笔记」 | ≈4-6 |
| **c4** | [`c4_social-pulse.md`](skills-community/c4_social-pulse.md) | 热议标的温度计（喊单 × 实盘 × 内部人） | 「溫度計」「推特在吵什么」 | ≈4-6 |
| **c5** | [`c5_hot-take.md`](skills-community/c5_hot-take.md) | 实时热点扫描 + 速报 + 财报速读 | 「扫一下热点」「TSLA 财报出来了」 | ≈1-3 |
| **c6** | [`c6_ticker-check.md`](skills-community/c6_ticker-check.md) | 运营内部选题速查（产出不对外） | 「速查 SMCI」「这票值不值得写」 | ≈2 |

产出形态：**繁体中文、纯文本 + emoji**（TG / Discord / LINE 通吃，不依赖 markdown 渲染），运营零加工即可发布。

完整的一週運營節奏表、安装方式、额度预算与置顶帖模板见 [`skills-community/README.md`](skills-community/README.md)。

---

## 旧 Commands 的两份单一事实源（SSOT）

六个旧 command 共享，冲突时以 SSOT 为准；改规则先改 SSOT，再 sweep 各 command 内联镜像。标准 Agent Skill 以当前 MCP tool schema 和自身 `references/tool-routing.md` 为准。

- [`.claude/references/community-post-style.md`](.claude/references/community-post-style.md) —— 贴文风格规范：12 条编号规则（繁体用词、白话红线、贴文骨架、多空平衡、五条运营铁律、更正贴模板、发前自检清单）+ 4 份已核可样例。
- [`.claude/references/followin-mcp-caveats.md`](.claude/references/followin-mcp-caveats.md) —— MCP 调用红线与已知问题登记表，其中 N 系列全部来自本项目的在线实测。

---

## 快速开始

```bash
# 1. 取得 Followin MCP API Key 并接入客户端（详见 https://followin.io/en/mcp）
# 2A. 安装标准 Agent Skill
cp -R skills/followin-us-equity-ops ~/.codex/skills/
# 2B. Claude Commands 兼容安装
cp skills-community/c*.md ~/.claude/commands/
# 3. 直接说人话触发
#    「跑早報」/「扫一下热点」/「研報熱點」/「溫度計」/「速查 SMCI」/「週報」
```

---

## 先看产出长什么样

**[`docs/产出样张集.md`](docs/产出样张集.md)** —— 10 份真实实跑产出，覆盖 6 个模块中的 5 个（含跨源打架、数据稀薄、缺数据时的诚实标注三类边界案例）。全部为真实数据，非示意稿。

---

## 设计与验证

- [`docs/设计文档.md`](docs/设计文档.md) —— 需求边界、架构决策、六模块调用序列、错误处理与验收标准。
- [`docs/实测回归记录.md`](docs/实测回归记录.md) —— NVDA / MU 实测回归全记录，含三份产出样张全文与逐项断言结果。

**所有调用路径均为在线实测确认，非文档推断。** 实测过程中推翻过多条二手记载（例如异动榜实际不返回市值字段、财报当晚基本面接口仍停留在上一季），修正结果已写回 caveats SSOT。

---

## 额度

全套一轮（六模块各跑一次）约 13-17 次调用。按早报日跑、其余模块周跑估算，月耗约 600-750 点，Basic 档（1000/月）可跑；财报季速查频繁时建议 Pro。
