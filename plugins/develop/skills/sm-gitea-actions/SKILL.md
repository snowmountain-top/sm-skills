---
name: sm-gitea-actions
description: Use when creating, editing, or reviewing CI/CD workflow files for Gitea instances. Use when encountering runner label mismatch errors, action URL resolution failures, or when migrating GitHub Actions workflows to Gitea.
---

# sm-gitea-actions

## 概述

Gitea Actions 是 Gitea 内置的 CI/CD 系统，与 GitHub Actions 语法高度兼容，但在文件路径、上下文变量和 Runner 配置方面有 Gitea 专属的约定。

## 何时使用

- 创建或编辑 `.gitea/workflows/*.yml` 文件
- 将 GitHub Actions 工作流迁移到 Gitea
- 遇到 "No matching online runner with label" 错误
- 排查 Action URL 解析或上下文变量问题
- 配置基于 act_runner 的自托管 Runner

**不适用场景**：GitHub Actions、GitLab CI、Jenkins 等其他 CI 系统。

## 快速对照表：Gitea vs GitHub

| 对比项 | Gitea | GitHub |
|--------|-------|--------|
| 工作流路径 | `.gitea/workflows/` | `.github/workflows/` |
| 上下文前缀 | `gitea.*`（推荐） | `github.*` |
| 输出环境变量 | `GITEA_OUTPUT` | `GITHUB_OUTPUT` |
| 环境变量文件 | `GITEA_ENV` | `GITHUB_ENV` |
| PATH 变量文件 | `GITEA_PATH` | `GITHUB_PATH` |
| 自托管 Runner | `act_runner` | GitHub Runner |
| 默认 Action URL | 禁止使用外部 Action，全部用 `run:` 原生命令 | `github.com` |

## 核心规则

**1. 文件路径必须是 `.gitea/workflows/`**

```yaml
# 正确
# 文件位置：.gitea/workflows/ci.yml

# 错误
# .github/workflows/ci.yml  ← 这是 GitHub 的路径
```

**2. 上下文变量必须使用 `gitea.*`**

`github.*` 别名仅为向后兼容，新工作流应始终使用原生命名空间：

```yaml
# 正确
run: |
  echo "仓库：${{ gitea.repository }}"
  echo "触发者：${{ gitea.actor }}"
  echo "分支：${{ gitea.ref }}"
  echo "事件：${{ gitea.event_name }}"
  echo "提交 SHA：${{ gitea.sha }}"

# 避免使用
run: echo "仓库：${{ github.repository }}"
```

**3. 环境变量必须使用 `GITEA_*`**

```yaml
# 正确
run: echo "key=value" >> $GITEA_OUTPUT
run: echo "MY_VAR=value" >> $GITEA_ENV
run: echo "/custom/bin" >> $GITEA_PATH

# 避免使用
run: echo "key=value" >> $GITHUB_OUTPUT
```

**4. 禁止使用外部 Action，全部使用原生命令**

国内 runner 从 gitea.com / GitHub 拉取 Action 不稳定，所有步骤应使用 `run:` 原生命令完成，禁止使用 `uses:` 引用任何外部 Action：

```yaml
# 正确：使用原生 git clone 检出代码
- name: 检出代码
  run: |
    git clone "http://x-access-token:${{ gitea.token }}@server:3000/${{ gitea.repository }}.git" .
    git checkout ${{ gitea.sha }}

# 正确：使用原生命令安装工具
- name: 安装 pnpm
  run: npm install -g pnpm@10

# 正确：使用原生命令设置 Node.js（如果需要版本管理）
- name: 设置 Node.js
  run: |
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt-get install -y nodejs

# 禁止使用
uses: actions/checkout@v4
uses: actions/setup-node@v4
uses: actions/cache@v4
uses: actions/upload-artifact@v4
uses: https://gitea.com/actions/checkout@v4
uses: https://gitea.com/actions/setup-node@v4
```

**注意**：`server:3000` 是 Docker 内部网络中 Gitea 服务的主机名，runner 的 `config.yaml` 需配置 `container.network` 使 job 容器加入同一网络。

## 深入参考

| 主题 | 文件 | 何时查看 |
|------|------|---------|
| Runner 注册与标签匹配 | [references/runner-configuration.md](references/runner-configuration.md) | 使用自托管 Runner 时 |
| 工作流模板（Node.js、矩阵构建等） | [references/workflow-patterns.md](references/workflow-patterns.md) | 需要参考具体示例时 |
| 问题排查与常见错误 | [references/troubleshooting.md](references/troubleshooting.md) | 遇到错误需要排查时 |

## 危险信号

看到以下内容时请立即 STOP 并修正：

- `.github/workflows/` 出现在 Gitea 项目中
- `github.*` 变量出现在新建的 Gitea 工作流中
- `$GITHUB_OUTPUT` 替代了 `$GITEA_OUTPUT`
- 使用 act_runner 时 `runs-on` 缺少 `self-hosted` 标签
- `uses:` 引用任何外部 Action（如 `actions/checkout`、`actions/setup-node`、`https://gitea.com/actions/*`）
- 工作流步骤依赖从外部（gitea.com / GitHub）拉取 Action
