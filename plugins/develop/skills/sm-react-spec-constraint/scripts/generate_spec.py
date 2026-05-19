#!/usr/bin/env python3
"""
React Spec 简单生成器（备用实现）
"""

import re
import json
from datetime import datetime
from pathlib import Path

def parse_tech_review(doc_path):
    """解析技术评审文档"""
    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取关键信息
    info = {
        'title': '',
        'description': '',
        'components': [],
        'features': [],
        'constraints': []
    }

    # 提取标题
    title_match = re.search(r'#+\s*(.+)', content)
    if title_match:
        info['title'] = title_match.group(1).strip()

    # 提取功能描述
    desc_match = re.search(r'(功能描述|描述)\s*[:：]\s*(.+)', content, re.IGNORECASE)
    if desc_match:
        info['description'] = desc_match.group(2).strip()

    # 提取功能列表
    features_section = re.findall(r'[-*•]\s*(.+)', content)
    info['features'] = [f.strip() for f in features_section[:10]]  # 取前10个

    # 提取组件信息（基于页面结构）
    pages = re.findall(r'(#+\s*[^#\n]+)', content)
    for page in pages:
        page_name = re.sub(r'^#+\s*', '', page).strip()
        if '页面' in page_name or '管理' in page_name or '列表' in page_name:
            info['components'].append({
                'name': page_name,
                'type': 'page'
            })

    return info

def generate_mermaid_structure(components):
    """生成组件结构图"""
    structure = "graph TD\n"
    for i, comp in enumerate(components):
        structure += f"    A{i}[{comp['name']}]"
        if i < len(components) - 1:
            structure += " --> "
        structure += f"A{i+1}[{components[i+1]['name'] if i+1 < len(components) else '完成'}]\n"

    return structure

def generate_ts_interface(components):
    """生成 TypeScript 接口定义"""
    interfaces = []

    for comp in components:
        interface = f"""
interface {comp['name']}Props {{
    // 基础属性
    id?: string;
    className?: string;

    // 业务属性"""
        if comp['type'] == 'page':
            interface += """
    title?: string;
    data?: any[];
    loading?: boolean;"""

        interface += """

    // 事件回调
    onAction?: (action: string, data?: any) => void;
    onError?: (error: Error) => void;
}}

interface {comp['name']}State {{
    // 状态定义
    isLoading: boolean;
    error: Error | null;
"""
        if comp['type'] == 'page' and 'list' in comp['name'].lower():
            interface += """
    pagination: {{
        page: number;
        pageSize: number;
        total: number;
    }};
"""
        interface += """
}
"""
        interfaces.append(interface)

    return "\n".join(interfaces)

def generate_logger_setup():
    """生成日志设置方案"""
    return """
### 日志配置 (logger.ts)
```typescript
import winston from 'winston';

// 日志格式配置
const logFormat = winston.format.combine(
  winston.format.timestamp(),
  winston.format.errors({ stack: true }),
  winston.format.json()
);

// 创建日志实例
export const logger = winston.createLogger({
  level: process.env.NODE_ENV === 'production' ? 'info' : 'debug',
  format: logFormat,
  transports: [
    // 控制台输出（开发环境）
    new winston.transports.Console({
      format: winston.format.simple(),
      level: 'debug'
    }),
    // 文件输出（生产环境）
    new winston.transports.File({
      filename: 'logs/error.log',
      level: 'error',
      maxsize: 5242880, // 5MB
      maxFiles: 5,
    }),
    new winston.transports.File({
      filename: 'logs/combined.log',
      maxsize: 5242880, // 5MB
      maxFiles: 14,
    }),
  ],
});

// 性能监控装饰器
export function withPerformanceLog(target: any, propertyName: string, descriptor: TypedPropertyDescriptor<any>) {
  const method = descriptor.value;

  descriptor.value = async function(...args: any[]) {
    const start = Date.now();
    logger.info(`[${propertyName}] 开始执行`, { args });

    try {
      const result = await method.apply(this, args);
      const duration = Date.now() - start;

      logger.info(`[${propertyName}] 执行完成`, {
        duration: `${duration}ms`,
        result: typeof result === 'object' ? JSON.stringify(result).substring(0, 200) : result
      });

      return result;
    } catch (error) {
      const duration = Date.now() - start;
      logger.error(`[${propertyName}] 执行失败`, {
        error: error.message,
        duration: `${duration}ms`,
        args
      });
      throw error;
    }
  };
}

// API 调用日志中间件
export const apiLogger = (req: any, res: any, next: any) => {
  const startTime = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - startTime;
    logger.info('API 调用', {
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration: `${duration}ms`,
      userAgent: req.get('User-Agent'),
      ip: req.ip
    });
  });

  next();
};
```

### 日志使用示例
```typescript
// 组件中使用日志
import React, { useEffect, useState } from 'react';
import { logger, withPerformanceLog } from '../utils/logger';

const UserProfilePage: React.FC<UserProfilePageProps> = ({ id, onAction }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  // 带性能监控的数据获取
  const fetchData = async () => {
    setLoading(true);
    try {
      logger.info('开始获取用户数据', { userId: id });

      const response = await fetch(\`/api/users/\${id}\`);
      const result = await response.json();

      setData(result);
      logger.info('用户数据获取成功', { userId: id, dataLength: Object.keys(result).length });
    } catch (error) {
      logger.error('获取用户数据失败', {
        userId: id,
        error: error.message,
        stack: error.stack
      });
      onAction?.('error', error);
    } finally {
      setLoading(false);
    }
  };

  // 性能监控装饰器使用示例
  @withPerformanceLog
  const handleUserAction = (action: string, data?: any) => {
    logger.info('用户操作', { action, data });
    onAction?.(action, data);
  };

  useEffect(() => {
    if (id) {
      fetchData();
    }
  }, [id]);

  return (
    <div>
      {/* 组件内容 */}
    </div>
  );
};
```

def generate_implementation(components):
    """生成实现方案示例"""
    implementations = []

    for comp in components:
        impl = f"""const {comp['name']}: React.FC<{comp['name']}Props> = ({{
    id,
    className,
    title,
    data = [],
    loading = false,
    onAction,
    onError
}}) => {{
    const [state, setState] = React.useState<{comp['name']}State>({{\n        isLoading: false,\n        error: null"""

        if comp['type'] == 'page' and 'list' in comp['name'].lower():
            impl += """,
        pagination: {
            page: 1,
            pageSize: 10,
            total: 0
        }"""

        impl += """
    }]);

    // 使用 useCallback 优化事件处理
    const handleAction = React.useCallback((action: string, data?: any) => {
        try {
            // 实现业务逻辑
            onAction?.(action, data);
        } catch (error) {
            setState(prev => ({ ...prev, error: error as Error }));
            onError?.(error as Error);
        }
    }, [onAction, onError]);

    // 使用 useMemo 优化计算
    const processedData = React.useMemo(() => {
        return data.map(item => ({
            ...item,
            processed: true
        }));
    }, [data]);

    // 使用 React.memo 优化性能
    return (
        <div className={\`container \${className}\`}>
            <h1>{title}</h1>
            {loading && <div className="skeleton-loader" />}
            {!loading && (
                <div className="content">
                    {/* 组件内容 */}
                </div>
            )}
        </div>
    );
}};"""

        implementations.append(impl)

    return "\n\n".join(implementations)

def generate_spec(info):
    """生成完整的 spec 文档"""
    spec = f"""# React Spec

## 1. 组件结构

```mermaid
{generate_mermaid_structure(info['components'])}
```

## 2. 接口定义

```typescript
{generate_ts_interface(info['components'])}
```

## 3. 实现方案

```typescript
{generate_implementation(info['components'])}
```

## 4. 日志实现方案

{generate_logger_setup()}

## 5. 依赖说明

### 核心依赖
- react: ^18.0.0
- react-dom: ^18.0.0
- typescript: ^4.9.0

### UI 组件库（可选）
- antd: ^5.0.0  或
- material-ui: ^5.0.0

### 状态管理（根据项目大小选择）
- 小型项目: 无额外依赖
- 中型项目: zustand: ^4.0.0
- 大型项目: @reduxjs/toolkit: ^1.9.0

### 样式方案
- css-modules: 默认
- styled-components: 可选
- tailwindcss: 如果项目已配置

### 日志方案
- 小型项目: 无额外依赖（使用 console）
- 中型项目: winston: ^3.8.0
- 大型项目: log4js: ^6.6.1
- 性能监控: @opentelemetry/api: ^1.4.0

## 6. 注意事项

### 性能优化
1. 所有展示组件必须使用 `React.memo`
2. 事件处理函数必须使用 `useCallback`
3. 复杂计算结果必须使用 `useMemo`
4. 长列表必须实现虚拟滚动

### 日志规范
1. 所有 API 调用必须记录日志
2. 关键业务操作必须记录日志
3. 错误必须记录完整堆栈
4. 性能监控点必须记录响应时间
5. 日志文件按日期分割，保留最近30天
6. 敏感信息不能记录日志

### 代码规范
1. 使用 TypeScript，必须定义类型
2. 组件使用 PascalCase 命名
3. 文件使用 kebab-case 命名
4. 使用 CSS Modules 管理样式

### 错误处理
1. 实现错误边界组件
2. 异步操作必须处理错误
3. 提供用户友好的错误提示

### 测试要求
1. 使用 React Testing Library
2. 核心组件必须有单元测试
3. 页面必须有集成测试
4. 测试覆盖率不低于 80%

## 6. 实现步骤

### 阶段一：基础结构
1. 创建组件目录结构
2. 实现基础组件框架
3. 配置 TypeScript 和 ESLint
4. 集成日志系统

### 阶段二：功能实现
1. 实现核心业务逻辑
2. 添加状态管理
3. 完成交互功能
4. 添加日志记录点

### 阶段三：优化完善
1. 性能优化
2. 样式美化
3. 添加测试用例
4. 实现性能监控

### 阶段四：部署上线
1. 构建优化
2. 性能监控
3. 线上验证
4. 配置日志收集

---

### 项目结构

```
src/
├── components/          # 公共组件
│   ├── common/         # 通用组件
│   └── business/       # 业务组件
├── pages/              # 页面组件
├── hooks/              # 自定义 Hooks
├── store/              # 状态管理
├── api/           # API 服务
├── utils/              # 工具函数
│   ├── logger.ts       # 日志配置
│   └── performance.ts  # 性能监控
├── types/              # TypeScript 类型定义
├── styles/             # 全局样式
├── constants/          # 常量定义
└── logs/               # 日志文件目录
```

---
*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    return spec

def main():
    """主函数"""
    import sys

    if len(sys.argv) != 3:
        print("用法: python3 generate_spec.py <输入文档> <输出文件>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # 解析文档
    info = parse_tech_review(input_path)

    # 生成 spec
    spec = generate_spec(info)

    # 保存输出
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(spec)

    print(f"✓ Spec 已生成: {output_path}")

if __name__ == "__main__":
    main()