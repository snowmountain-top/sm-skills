# 工作流模板参考

> **核心原则：所有步骤使用 `run:` 原生命令，禁止使用 `uses:` 引用外部 Action。**
> 国内 runner 从 gitea.com / GitHub 拉取 Action 不稳定，使用原生命令最可靠。

## Node.js CI（纯原生命令）

```yaml
name: CI
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: 检出代码
        run: |
          git clone "http://x-access-token:${{ gitea.token }}@server:3000/${{ gitea.repository }}.git" .
          git checkout ${{ gitea.sha }}

      - name: 配置 npm 阿里云镜像源
        run: npm config set registry https://registry.npmmirror.com

      - name: 安装依赖
        run: npm ci

      - name: 运行测试
        run: npm test
```

## 矩阵构建（自托管 Runner）

```yaml
jobs:
  test:
    runs-on: [self-hosted, linux, x64]
    strategy:
      matrix:
        node: ['18', '20', '22']
    steps:
      - name: 检出代码
        run: |
          git clone "http://x-access-token:${{ gitea.token }}@server:3000/${{ gitea.repository }}.git" .
          git checkout ${{ gitea.sha }}

      - name: 切换 Node.js 版本
        run: nvm use ${{ matrix.node }}

      - name: 运行测试
        run: npm test
```

## 条件步骤

```yaml
steps:
  - name: 生产环境部署
    if: gitea.ref == 'refs/heads/main'
    run: ./deploy.sh

  - name: PR 检查
    if: gitea.event_name == 'pull_request'
    run: ./pr-check.sh

  - name: 仅特定用户触发
    if: gitea.actor == 'admin'
    run: ./admin-task.sh
```

## 缓存依赖（原生目录缓存）

```yaml
steps:
  - name: 缓存 node_modules
    run: |
      mkdir -p /tmp/cache
      if [ -d /tmp/cache/node_modules ]; then
        cp -r /tmp/cache/node_modules .
      fi

  - name: 安装依赖
    run: npm ci

  - name: 保存缓存
    run: |
      rm -rf /tmp/cache/node_modules
      cp -r node_modules /tmp/cache/
```

## 构建产物（原生命令）

```yaml
# 上传产物到服务器
- name: 上传构建产物
  run: |
    tar czf build-output.tar.gz dist/
    curl -X PUT -T build-output.tar.gz http://artifacts-server/uploads/${{ gitea.sha }}.tar.gz

# 下载产物（在另一个 job 中）
- name: 下载构建产物
  run: |
    curl -o build-output.tar.gz http://artifacts-server/uploads/${{ gitea.sha }}.tar.gz
    tar xzf build-output.tar.gz
```

## 后端编译（pnpm + TypeScript）

> 适用于除 test 分支外的常规分支推送，仅执行 lint 和编译，不构建镜像。

```yaml
name: 后端编译

on:
  push:
    branches-ignore: ['test/*']

jobs:
  build-server:
    runs-on: ubuntu-latest
    steps:
      - name: 检出代码
        run: |
          git clone "http://x-access-token:${{ gitea.token }}@server:3000/${{ gitea.repository }}.git" .
          git checkout ${{ gitea.sha }}

      - name: 配置 npm 阿里云镜像源
        run: npm config set registry https://registry.npmmirror.com

      - name: 安装 pnpm
        run: npm install -g pnpm@10

      - name: 安装依赖
        run: cd server && pnpm install --frozen-lockfile --registry https://registry.npmmirror.com

      - name: ESLint 代码检查
        run: cd server && pnpm lint

      - name: 编译 TypeScript
        run: cd server && pnpm build

      - name: 输出构建信息
        run: |
          echo "构建完成: ${{ gitea.repository }}"
          echo "提交: ${{ gitea.sha }}"
          echo "触发者: ${{ gitea.actor }}"
          echo "分支: ${{ gitea.ref }}"
```

## 后端镜像构建与推送（pnpm + Docker + TCR）

> 适用于 test 分支和 tag 推送，执行完整编译流程后构建 Docker 镜像并推送到腾讯云 TCR。
> tag 推送生成 release 标签，test 分支推送生成 test 标签。

```yaml
name: 后端镜像构建

on:
  push:
    branches: ['test/*']
    tags: ['v*']

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - name: 检出代码
        run: |
          git clone "http://x-access-token:${{ gitea.token }}@server:3000/${{ gitea.repository }}.git" .
          git checkout ${{ gitea.sha }}

      - name: 配置 npm 阿里云镜像源
        run: npm config set registry https://registry.npmmirror.com

      - name: 安装 pnpm
        run: npm install -g pnpm@10

      - name: 安装依赖
        run: cd server && pnpm install --frozen-lockfile --registry https://registry.npmmirror.com

      - name: ESLint 代码检查
        run: cd server && pnpm lint

      - name: 编译 TypeScript
        run: cd server && pnpm build

      - name: 安装 Docker CLI
        run: |
          curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/static/stable/x86_64/docker-27.5.1.tgz | tar xz
          mv docker/docker /usr/bin/docker
          rm -rf docker
          docker --version

      - name: 生成镜像标签
        id: meta
        run: |
          REGISTRY="<你的镜像仓库地址>"
          TIMESTAMP=$(date +%Y%m%d-%H%M%S)
          if [ "${{ gitea.ref_type }}" = "tag" ]; then
            TAG="<项目名>-${TIMESTAMP}-release-${{ gitea.ref_name }}"
          else
            TAG="<项目名>-${TIMESTAMP}-test"
          fi
          echo "tag=${TAG}" >> $GITEA_OUTPUT
          echo "full_image=${REGISTRY}:${TAG}" >> $GITEA_OUTPUT
          echo "镜像标签: ${TAG}"

      - name: 登录镜像仓库
        run: echo "${{ secrets.REGISTRY_PASSWORD }}" | docker login -u "${{ secrets.REGISTRY_USERNAME }}" --password-stdin <镜像仓库域名>

      - name: 构建 Docker 镜像
        run: |
          cd server
          docker build -t ${{ steps.meta.outputs.full_image }} .

      - name: 推送镜像
        run: docker push ${{ steps.meta.outputs.full_image }}

      - name: 输出构建信息
        run: |
          echo "触发类型: ${{ gitea.ref_type }}"
          echo "触发者: ${{ gitea.actor }}"
          echo "分支/标签: ${{ gitea.ref_name }}"
          echo "镜像: ${{ steps.meta.outputs.full_image }}"
```

**使用前替换以下占位符：**

| 占位符 | 说明 | 示例 |
|--------|------|------|
| `<你的镜像仓库地址>` | 镜像仓库完整路径 | `belink-ai.tencentcloudcr.com/belink/db-archiver` |
| `<项目名>` | 镜像标签前缀 | `db_archiver` |
| `<镜像仓库域名>` | docker login 的域名 | `belink-ai.tencentcloudcr.com` |

**需要在 Gitea 仓库设置中配置以下 Secrets：**

| Secret | 说明 |
|--------|------|
| `REGISTRY_USERNAME` | 镜像仓库用户名 |
| `REGISTRY_PASSWORD` | 镜像仓库密码 |
