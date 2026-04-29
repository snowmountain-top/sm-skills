# Issue 与 PR API

## 全局搜索 Issue

```
GET /repos/issues/search
```

跨仓库搜索 Issue 和 PR。

| 参数 | 类型 | 说明 |
|------|------|------|
| `state` | string | `open`、`closed`、`all` |
| `type` | string | `issues`（仅 Issue）、`pulls`（仅 PR） |
| `labels` | string | 标签过滤（逗号分隔） |
| `milestones` | string | 里程碑过滤（逗号分隔） |
| `created_by` | string | 创建者 |
| `assigned_by` | string | 指派人 |
| `mentioned_by` | string | 被 @ 的人 |
| `since` | string | 起始时间（ISO 8601） |
| `before` | string | 截止时间（ISO 8601） |
| `limit` | int | 每页数量 |
| `page` | int | 页码 |
| `sort` | string | `created`、`updated`、`comments` |
| `order` | string | `asc`、`desc` |

示例：

```bash
# 搜索所有开放的 PR
curl -s -H "Authorization: token ${GITEA_TOKEN}" \
  "https://git.8848top.com/api/v1/repos/issues/search?type=pulls&state=open"

# 搜索特定用户创建的 Issue
curl -s -H "Authorization: token ${GITEA_TOKEN}" \
  "https://git.8848top.com/api/v1/repos/issues/search?created_by=xingshan&limit=10"
```

## 仓库 Issue 列表

```
GET /repos/{owner}/{repo}/issues
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `state` | string | `open`、`closed`、`all` |
| `labels` | string | 标签过滤 |
| `milestones` | string | 里程碑过滤 |
| `assignee` | string | 指派人 |
| `created_by` | string | 创建者 |
| `since` | string | 起始时间 |
| `limit` | int | 每页数量 |
| `page` | int | 页码 |

注意：默认包含 PR（PR 在 Gitea 中也是 Issue 的一种）。用 `type=issue` 或 `type=pull` 过滤。

## Issue 详情

```
GET /repos/{owner}/{repo}/issues/{index}
```

返回 Issue 完整信息，包含：

| 字段 | 说明 |
|------|------|
| `number` | Issue 编号 |
| `title` | 标题 |
| `body` | 内容（Markdown） |
| `state` | `open` 或 `closed` |
| `user` | 创建者 |
| `assignee` | 指派人 |
| `labels` | 标签列表 |
| `milestone` | 里程碑 |
| `created_at` | 创建时间 |
| `updated_at` | 更新时间 |
| `closed_at` | 关闭时间 |
| `comments` | 评论数 |
| `html_url` | 网页链接 |

## Issue 评论

```
GET /repos/{owner}/{repo}/issues/{index}/comments
```

返回 Issue 下的所有评论。

响应示例：

```json
[
  {
    "id": 1,
    "body": "评论内容（Markdown）",
    "user": { "login": "Muchen", "id": 4 },
    "created_at": "2026-04-25T10:00:00+08:00",
    "updated_at": "2026-04-25T10:00:00+08:00"
  }
]
```

## PR 列表

```
GET /repos/{owner}/{repo}/pulls
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `state` | string | `open`、`closed`、`all` |
| `sort` | string | `created`、`updated`、`priority` |
| `order` | string | `asc`、`desc` |
| `limit` | int | 每页数量 |
| `page` | int | 页码 |
| `base` | string | 目标分支过滤 |

## PR 详情

```
GET /repos/{owner}/{repo}/pulls/{index}
```

返回 PR 完整信息，除 Issue 字段外还包含：

| 字段 | 说明 |
|------|------|
| `head` | 源分支信息 `{ label, ref, sha, repo }` |
| `base` | 目标分支信息 `{ label, ref, sha, repo }` |
| `mergeable` | 是否可合并 |
| `merged` | 是否已合并 |
| `merged_at` | 合并时间 |
| `merge_commit_sha` | 合并 commit SHA |

## 标签管理

```
GET /repos/{owner}/{repo}/labels
```

返回仓库的所有标签。

```json
[
  {
    "id": 1,
    "name": "bug",
    "color": "ee0701",
    "description": "Something isn't working"
  }
]
```

## 里程碑管理

```
GET /repos/{owner}/{repo}/milestones
```

返回仓库的所有里程碑。

```json
[
  {
    "id": 1,
    "title": "v1.0",
    "description": "First release",
    "state": "open",
    "open_issues": 5,
    "closed_issues": 3,
    "due_on": "2026-06-01T00:00:00+08:00"
  }
]
```

## PR 评论（Review Comments）

```
GET /repos/{owner}/{repo}/pulls/{index}/comments
```

返回 PR 中针对具体代码行的评论（不同于 Issue 评论）。

## PR 文件变更

```
GET /repos/{owner}/{repo}/pulls/{index}/files
```

返回 PR 变更的文件列表。

## PR 合并信息

```
GET /repos/{owner}/{repo}/pulls/{index}/merge
```

返回 204 表示 PR 已合并，返回 404 表示未合并。
