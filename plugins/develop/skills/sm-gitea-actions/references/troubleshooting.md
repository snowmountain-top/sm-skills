# 问题排查参考

## 常见错误速查表

| 错误/现象 | 根因 | 解决方案 |
|----------|------|---------|
| Workflow 未触发 | 文件放在了 `.github/workflows/` | 移到 `.gitea/workflows/` |
| "No matching online runner with label" | `runs-on` 标签与 Runner 标签不匹配 | 检查 Runner 注册时的标签，确保完全匹配 |
| Action 下载 404 | Runner 无法访问 GitHub | 设置 `DEFAULT_ACTIONS_URL` 或使用完整 URL |
| CI 完全未运行 | 仓库未启用 Actions | 在仓库设置中启用 "Repository Actions" |
| `gitea.*` 变量解析为空 | 变量名拼写错误或使用 `github.*` | 使用正确的 `gitea.*` 变量名 |
| 产物下载失败 | 产物名称冲突或 job 依赖未声明 | 矩阵构建中使用 `${{ matrix.xxx }}` 区分名称；使用 `needs` 声明依赖 |

## Action URL 配置

**核心原则：禁止使用任何外部 Action（`uses:`），全部使用 `run:` 原生命令。**

国内 runner 从 gitea.com / GitHub 拉取 Action 不稳定，所有步骤应通过原生 shell 命令完成。

### 正确写法（原生命令）

```yaml
# 正确：使用原生 git clone 检出代码（通过 Docker 内部网络）
- name: 检出代码
  run: |
    git clone "http://x-access-token:${{ gitea.token }}@server:3000/${{ gitea.repository }}.git" .
    git checkout ${{ gitea.sha }}

# 正确：使用原生命令安装工具
- name: 安装 pnpm
  run: npm install -g pnpm@10
```

### 禁止使用（外部 Action）

```yaml
# 错误：任何形式的外部 Action 引用都不允许
uses: actions/checkout@v4
uses: actions/setup-node@v4
uses: https://gitea.com/actions/checkout@v4
uses: https://gitea.com/actions/setup-node@v4
```

### 前提条件

使用 `server:3000` 内部主机名需要 runner 的 `config.yaml` 配置 `container.network`，使 job 容器与 Gitea 服务在同一 Docker 网络中。

## 仓库 Actions 未启用

即使 Gitea 实例全局启用了 Actions，每个仓库仍需单独开启：

**设置路径**：仓库设置 → Actions → 启用 "Repository Actions"

若未启用，任何 push 到 `.gitea/workflows/` 都不会触发工作流。

## Runner 标签调试

查看已注册 Runner 及其标签：

1. 进入 Gitea 管理后台 → Actions → Runners
2. 或使用 API：
   ```bash
   curl -H "Authorization: token $TOKEN" \
     https://gitea.example.com/api/v1/admin/runners
   ```

确认 `runs-on` 中的每个标签都出现在目标 Runner 的标签列表中。

## Step 输出调试

使用 `GITEA_OUTPUT` 在步骤间传递数据：

```yaml
steps:
  - name: 生成版本号
    id: version
    run: echo "version=1.2.3" >> $GITEA_OUTPUT

  - name: 使用版本号
    run: echo "部署版本：${{ steps.version.outputs.version }}"
```

若输出为空，检查：
1. 是否正确使用了 `$GITEA_OUTPUT`（不是 `$GITHUB_OUTPUT`）
2. 上游步骤是否设置了 `id`
3. 下游引用格式是否为 `steps.<id>.outputs.<key>`
