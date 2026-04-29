# 用户与组织 API

## 当前认证用户

```
GET /user
```

返回当前 token 所属用户的完整信息。

响应示例：

```json
{
  "id": 4,
  "login": "Muchen",
  "full_name": "",
  "email": "muchen@8848top.com",
  "avatar_url": "https://git.8848top.com/avatars/de51ef...",
  "html_url": "https://git.8848top.com/Muchen",
  "language": "zh-CN",
  "is_admin": true,
  "restricted": false,
  "active": true,
  "visibility": "public",
  "created": "2026-04-24T17:45:47+08:00",
  "last_login": "2026-04-25T09:56:04+08:00"
}
```

## 搜索用户

```
GET /users/search
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `q` | string | 搜索关键词（匹配用户名和全名） |
| `limit` | int | 返回数量（默认 10） |

响应示例：

```json
{
  "ok": true,
  "data": [
    {
      "id": 4,
      "login": "Muchen",
      "full_name": "",
      "email": "muchen@8848top.com",
      "is_admin": true,
      "avatar_url": "..."
    }
  ]
}
```

## 用户详情

```
GET /users/{username}
```

返回指定用户的公开信息（login、id、email、avatar、created 等）。

## 我的组织列表

```
GET /user/orgs
```

返回当前用户所属的组织列表。

响应示例：

```json
[
  {
    "id": 2,
    "name": "belink",
    "username": "belink",
    "avatar_url": "...",
    "description": "",
    "website": "",
    "visibility": "private",
    "repo_admin_change_team_access": true
  }
]
```

## 组织详情

```
GET /orgs/{org}
```

返回组织的完整信息。

| 字段 | 说明 |
|------|------|
| `id` | 组织 ID |
| `name` | 组织名 |
| `username` | 用户名（用于 API 路径） |
| `visibility` | `public`、`private`、`limited` |
| `description` | 组织描述 |
| `website` | 网站 |
| `location` | 位置 |

## 组织成员

```
GET /orgs/{org}/members
```

返回组织所有成员列表（包含 login、id、email、is_admin 等）。

```bash
curl -s -H "Authorization: token ${GITEA_TOKEN}" \
  "https://git.8848top.com/api/v1/orgs/belink/members"
```

可选过滤参数：

| 参数 | 类型 | 说明 |
|------|------|------|
| `page` | int | 页码 |
| `limit` | int | 每页数量 |

## 组织团队

```
GET /orgs/{org}/teams
```

返回组织下的团队列表。

响应示例：

```json
[
  {
    "id": 1,
    "name": "Owners",
    "description": "",
    "permission": "owner",
    "units": ["repo.code", "repo.issues", "repo.wiki", ...],
    "includes_all_repositories": true
  }
]
```

## 团队成员

```
GET /teams/{id}/members
```

返回指定团队的所有成员。需要先通过组织团队接口获取 team ID。

## 团队仓库

```
GET /teams/{id}/repos
```

返回指定团队有权限访问的仓库列表。

## 组织公开成员

```
GET /orgs/{org}/public_members
```

仅返回公开可见的成员（与 `/members` 的区别是可不含私有成员）。

## 检查成员关系

```
GET /orgs/{org}/members/{username}
```

返回 204 表示是该组织成员，返回 404 表示不是。

```bash
# 检查用户是否在组织中
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: token ${GITEA_TOKEN}" \
  "https://git.8848top.com/api/v1/orgs/belink/members/xingshan"
# 204 = 是成员, 404 = 不是
```
