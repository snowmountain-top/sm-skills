# 仓库管理 API

## 搜索仓库

```
GET /repos/search
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `keyword` | string | 搜索关键词（匹配仓库名和描述） |
| `user` | string | 按用户名过滤 |
| `topic` | string | 按 Topic 过滤 |
| `include_mirror` | bool | 是否包含镜像仓库（默认 true） |
| `private` | bool | 是否包含私有仓库（需 token） |
| `limit` | int | 每页数量（默认 10） |
| `page` | int | 页码（从 1 开始） |
| `order` | string | `asc` 或 `desc` |
| `sort` | string | `alpha`、`created`、`updated`、`size`、`id` |

响应示例：

```json
{
  "ok": true,
  "data": [
    {
      "id": 2,
      "name": "BunnyDevOps",
      "full_name": "belink/BunnyDevOps",
      "description": "...",
      "private": false,
      "fork": false,
      "owner": { "login": "belink", "id": 2 },
      "html_url": "https://git.8848top.com/belink/BunnyDevOps",
      "clone_url": "https://git.8848top.com/belink/BunnyDevOps.git",
      "ssh_url": "git@git.8848top.com:belink/BunnyDevOps.git",
      "language": "TypeScript",
      "size": 367,
      "default_branch": "master",
      "branch_count": 7,
      "stars_count": 0,
      "forks_count": 0,
      "open_issues_count": 0,
      "open_pr_counter": 1,
      "created_at": "2026-04-24T17:54:29+08:00",
      "updated_at": "2026-04-28T15:04:12+08:00",
      "permissions": { "admin": true, "push": true, "pull": true }
    }
  ]
}
```

## 仓库详情

```
GET /repos/{owner}/{repo}
```

返回单个仓库的完整信息，包含 `permissions`（当前 token 对该仓库的权限）。

## 编辑仓库 ⚡ write:repository

```
PATCH /repos/{owner}/{repo}
```

可编辑字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `description` | string | 仓库描述 |
| `website` | string | 项目网站 |
| `private` | bool | 是否私有 |
| `visibility` | string | `public`、`private`、`limited` |
| `has_issues` | bool | 启用 Issue |
| `has_wiki` | bool | 启用 Wiki |
| `has_pull_requests` | bool | 启用 PR |
| `has_projects` | bool | 启用项目看板 |
| `has_releases` | bool | 启用 Release |
| `has_actions` | bool | 启用 Actions |
| `default_branch` | string | 默认分支 |
| `default_merge_style` | string | `merge`、`rebase`、`squash`、`fast-forward-only` |
| `default_delete_branch_after_merge` | bool | 合并后删除分支 |
| `allow_merge_commits` | bool | 允许 merge commit |
| `allow_rebase` | bool | 允许 rebase |
| `allow_squash_merge` | bool | 允许 squash merge |
| `topics` | string[] | 仓库标签 |
| `archived` | bool | 归档仓库 |

示例：

```bash
curl -s -X PATCH \
  -H "Authorization: token ${GITEA_TOKEN}" \
  -H "Content-Type: application/json" \
  "https://git.8848top.com/api/v1/repos/belink/BunnyDevOps" \
  -d '{"description":"DevOps automation platform","default_branch":"develop"}'
```

## 仓库分支

```
GET /repos/{owner}/{repo}/branches
```

返回分支列表，每个分支包含 `name` 和 commit 信息。

```bash
curl -s -H "Authorization: token ${GITEA_TOKEN}" \
  "https://git.8848top.com/api/v1/repos/belink/BunnyDevOps/branches"
```

## 仓库 Git 标签

```
GET /repos/{owner}/{repo}/tags
```

## 仓库 Release

```
GET /repos/{owner}/{repo}/releases
```

返回 Release 列表，包含 tag、标题、正文、附件等信息。

## 仓库 Webhook

```
GET /repos/{owner}/{repo}/hooks
```

查看已配置的 Webhook 列表。返回每个 hook 的 `id`、`type`、`config`、`events` 等信息。

## 仓库协作者

```
GET /repos/{owner}/{repo}/collaborators
```

返回有权限访问该仓库的用户列表。

## 仓库语言统计

```
GET /repos/{owner}/{repo}/languages
```

返回各语言代码量占比，如 `{"TypeScript": 15000, "JavaScript": 3000}`。

## 组织仓库列表

```
GET /orgs/{org}/repos
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `page` | int | 页码 |
| `limit` | int | 每页数量 |

## 仓库文件内容

```
GET /repos/{owner}/{repo}/contents/{filepath}
```

获取仓库中文件的内容（Base64 编码）或目录列表。

| 参数 | 类型 | 说明 |
|------|------|------|
| `ref` | string | 分支名或 commit SHA |
