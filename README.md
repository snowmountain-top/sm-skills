# sm-skills

Skills collection for Claude Code — 雪山之巅 skill 集合。

## 安装

### 添加 Marketplace

```bash
# 从 GitHub 添加
claude plugin marketplace add snowmountain-top/sm-skills

# 或在 Claude Code 中使用
/plugin marketplace add snowmountain-top/sm-skills
```

### 安装 Plugin

```bash
# 安装 develop plugin（包含所有 skills）
claude plugin install develop@sm-skills

# 或在 Claude Code 中使用
/plugin install develop@sm-skills
```

## 可用 Plugins

| Plugin | 描述 | 版本 | 包含 Skills |
|--------|------|------|-------------|
| develop | 开发技能合集 | 1.0.0 | sm-gitea, sm-gitea-actions |

## 开发

### 目录结构

```
sm-skills/
├── .claude-plugin/
│   └── marketplace.json       # Marketplace 入口文件
├── plugins/
│   └── develop/               # 开发技能合集
│       ├── plugin.json        # Plugin manifest
│       └── skills/
│           ├── sm-gitea/
│           │   ├── SKILL.md
│           │   └── references/
│           ├── sm-gitea-actions/
│           │   ├── SKILL.md
│           │   └── references/
│           └── <new-skill>/
│               └── SKILL.md   # 新增 skill 放这里
├── CLAUDE.md
├── README.md
└── LICENSE
```

### 添加新 Skill

1. 在 `plugins/develop/skills/` 下创建新目录
2. 编写 `SKILL.md`
3. 本地测试通过后推送

### 本地测试

```bash
# 添加本地 marketplace
/plugin marketplace add .

# 安装测试
/plugin install develop@sm-skills

# 验证 marketplace 结构
/plugin validate .
```

## License

MIT
