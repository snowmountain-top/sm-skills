# Runner 配置参考

## 自托管 Runner（act_runner）

### 注册与启动

```bash
# 下载 act_runner
wget https://gitea.com/gitea/act_runner/releases/latest/download/act_runner-linux-amd64
chmod +x act_runner-linux-amd64

# 注册到 Gitea 实例
./act_runner register \
  --instance https://gitea.example.com \
  --token <注册令牌>

# 启动 Runner
./act_runner daemon
```

### 标签匹配规则

`runs-on` 字段必须与 Runner 的标签**完全匹配**。所有指定的标签都必须同时存在于目标 Runner 上：

```yaml
# Runner 注册时的标签：self-hosted, linux, x64
jobs:
  build:
    runs-on: [self-hosted, linux, x64]  # 必须完全匹配
```

**常见错误**："No matching online runner with label" 表示没有在线 Runner 同时拥有 `runs-on` 中指定的所有标签。

### 默认标签

未配置自定义标签时，act_runner 自动提供以下默认标签：

- `ubuntu-latest`
- `ubuntu-22.04`
- `ubuntu-20.04`

### 自定义标签与 Docker 镜像

通过 `config.yaml` 或环境变量配置自定义标签，并绑定 Docker 镜像：

```yaml
# config.yaml
runner:
  labels:
    - "ubuntu-latest:docker://catthehacker/ubuntu:act-latest"
    - "ubuntu-22.04:docker://catthehacker/ubuntu:act-22.04"
    - "self-hosted"
    - "linux"
    - "x64"
```

或环境变量方式：

```bash
export GITEA_RUNNER_LABELS="ubuntu-latest:docker://catthehacker/ubuntu:act-latest"
```

**注意**：部分早期版本的 act_runner 存在环境变量 `GITEA_RUNNER_LABELS` 不生效的问题，建议优先使用 `config.yaml` 配置。
