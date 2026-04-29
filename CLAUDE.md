# CLAUDE.md - sm-skills 项目规范

> 这是 Claude Code 在本仓库中协作时应遵循的项目规范。

## 项目概述

这是一个 Claude Code Plugin Marketplace 仓库，用于发布和分发自定义 Skills 插件。用户通过 `/plugin marketplace add snowmountain-top/sm-skills` 安装后，可以浏览并安装其中的 plugin。

## 仓库结构

```
sm-skills/
├── .claude-plugin/
│   └── marketplace.json       # Marketplace 入口（必需）
├── plugins/
│   └── develop/               # 所有 skills 统一放在这个 plugin 下
│       ├── plugin.json        # Plugin manifest
│       └── skills/
│           ├── greeting/
│           │   └── SKILL.md
│           └── <new-skill>/
│               └── SKILL.md
├── CLAUDE.md
├── README.md
└── LICENSE
```

## 编写新 Skill 的完整流程

所有 skill 统一放在 `plugins/develop/skills/` 下，新增 skill 只需添加子目录和 SKILL.md。

### 1. 创建 Skill 目录

在 `plugins/develop/skills/` 下创建新目录，命名使用 kebab-case：

```
plugins/develop/skills/<skill-name>/
└── SKILL.md
```

### 2. 编写 SKILL.md

#### SKILL.md 格式规范

**Frontmatter（YAML）：** 只有 `name` 和 `description` 两个字段，总共不超过 1024 字符。

```yaml
---
name: skill-name-with-hyphens
description: Use when [具体触发条件和场景描述]
---
```

**description 编写规则：**
- 以 "Use when..." 开头，描述触发条件
- 只写「什么时候用」，不要概括 skill 的具体流程
- 使用第三人称
- 包含具体症状、场景、上下文
- 控制在 500 字符以内

**Body 结构：**

```markdown
# Skill Name

## Overview
核心原理，1-2 句话。

## When to Use
- 适用场景（bullet list）
- 不适用场景

## Instructions
具体步骤和规则。

## Examples
1 个高质量的完整示例。

## Constraints
限制条件和注意事项。
```

### 4. 更新 README.md

在 README 的「可用 Plugins」表格的「包含 Skills」列中添加新 skill 名称。

### 5. 验证和测试

```bash
# 验证 marketplace JSON 结构
claude plugin validate .

# 本地测试安装
/plugin marketplace add .
/plugin install develop@sm-skills
```

## 命名规范

| 对象 | 格式 | 示例 |
|------|------|------|
| Plugin 目录 | kebab-case | `code-review`, `api-testing` |
| Skill 目录 | kebab-case | `greeting`, `debug-helper` |
| Skill name 字段 | kebab-case，只用字母数字和连字符 | `my-skill-name` |
| Category | 小写单词 | `productivity`, `testing` |
| Tags | 小写，无空格 | `code-review`, `automation` |

## 质量检查清单

提交新 Skill 前必须确认：

- [ ] `plugin.json` 包含所有必需字段
- [ ] `SKILL.md` frontmatter 只有 `name` 和 `description`
- [ ] `description` 以 "Use when..." 开头，不含流程概括
- [ ] `marketplace.json` 已注册 develop plugin
- [ ] `source` 路径指向 `./plugins/develop`
- [ ] README 已更新
- [ ] `claude plugin validate .` 通过
