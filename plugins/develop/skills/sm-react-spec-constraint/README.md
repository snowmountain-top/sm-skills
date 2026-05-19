# React Spec 约束生成器

这个技能用于根据 React 前端技术评审文档生成符合规范的 spec 流程，并应用前端约束规则。

## 功能特点

1. **文档解析**：自动解析技术评审文档，提取关键信息
2. **约束检查**：应用 React 前端最佳实践约束规则
3. **Spec 生成**：生成标准化的 React 实现方案
4. **性能优化**：包含必要的性能优化建议
5. **类型安全**：强制使用 TypeScript 和类型定义

## 使用方法

### 1. 基本使用

```bash
# 在项目根目录执行
./skills/sm-react-spec-constraint/scripts/spec-generator.sh -d /path/to/tech-review.md
```

### 2. 完整参数

```bash
./skills/sm-react-spec-constraint/scripts/spec-generator.sh [选项]

选项:
    -d, --doc PATH     技术评审文档路径 (必需)
    -o, --output DIR   输出目录 (默认: ./specs)
    -f, --force        强制覆盖现有文件
    -v, --verbose      显示详细输出
    -h, --help         显示此帮助信息
```

### 3. 示例

```bash
# 基本用法
./skills/sm-react-spec-constraint/scripts/spec-generator.sh -d ./docs/技术评审.md

# 指定输出目录
./skills/sm-react-spec-constraint/scripts/spec-generator.sh -d ./docs/技术评审.md -o ./generated-specs

# 显示详细输出
./skills/sm-react-spec-constraint/scripts/spec-generator.sh -d ./docs/技术评审.md -v
```

## 生成的文件

### 1. React Spec 文件 (react-spec-YYYYMMDD_HHMMSS.md)
包含：
- 组件结构图（Mermaid 语法）
- TypeScript 接口定义
- 实现方案示例
- 依赖说明
- 注意事项

### 2. 约束报告文件 (constraint-report-YYYYMMDD_HHMMSS.md)
包含：
- 应用的约束规则列表
- 冲突统计
- 优化建议

## 约束规则

### 组件规范
- ✅ 函数组件优先
- ✅ 使用 Hooks
- ✅ PascalCase 命名
- ✅ kebab-case 文件名

### 性能优化
- ✅ React.memo
- ✅ useCallback
- ✅ useMemo

### 类型安全
- ✅ TypeScript
- ✅ 接口定义
- ✅ 类型守卫

### 样式方案
- ✅ CSS Modules
- ✅ 组件样式隔离

## 项目结构建议

```
src/
├── components/          # 公共组件
│   ├── common/         # 通用组件
│   └── business/       # 业务组件
├── pages/              # 页面组件
├── hooks/              # 自定义 Hooks
├── store/              # 状态管理
├── services/           # API 服务
├── utils/              # 工具函数
├── types/              # TypeScript 类型定义
├── styles/             # 全殊全局样式
└── constants/          # 常量定义
```

## 特殊场景处理

### 1. 表单组件
- 必须使用 `react-hook-form` 或 `formik`
- 表单验证规则必须类型化

### 2. 列表组件
- 长列表必须使用虚拟滚动
- 必须实现骨架屏加载

### 3. 图表组件
- 使用 `recharts` 或 `echarts` React 封装
- 必须响应式设计

## 故障排除

### 1. 未找到 React 项目
错误：`警告: 未在 package.json 中找到 react 依赖`
解决：确保项目包含 React 依赖，或使用 `-f` 参数强制继续

### 2. 文档解析失败
- 检查文档格式是否正确
- 确保文档包含足够的技术细节

### 3. 生成失败
- 检查 Python 3 是否安装
- 确保有足够的磁盘空间

## 日志规范说明

### 日志级别使用
- **error**: 系统错误、异常、关键业务失败
- **warn**: 潜在问题、配置警告、非关键错误
- **info**: 重要操作开始/结束、状态变更、关键业务流程
- **debug**: 调试信息、详细流程、变量状态

### 日志记录点
1. **API 调用**: 请求参数、响应数据、耗时
2. **业务操作**: 创建、更新、删除操作的执行结果
3. **状态变更**: 重要状态变化的前后对比
4. **错误处理**: 完整的错误堆栈和上下文信息
5. **性能监控**: 关键函数的执行时间

### 日志格式
```json
{
  "timestamp": "2024-01-01T12:00:00.000Z",
  "level": "info",
  "module": "user-service",
  "message": "用户登录成功",
  "metadata": {
    "userId": "12345",
    "duration": "150ms",
    "ip": "192.168.1.1"
  }
}
```

## 更新日志

### v1.0.0
- 初始版本发布
- 支持 React 基础约束
- 支持 Markdown 技术评审文档解析
- 生成标准化的 spec 文档

## 开发者指南

### 添加新的约束规则
1. 编辑 `SKILL.md` 文件
2. 在约束规则部分添加新规则
3. 更新 Python 解析器（如需要）

### 自定义生成模板
- 修改 `generate_spec.py` 中的模板
- 保持基本的文件结构

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个工具。

## 许可证

MIT License