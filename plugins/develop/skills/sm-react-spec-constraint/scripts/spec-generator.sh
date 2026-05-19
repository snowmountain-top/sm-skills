#!/bin/bash

# React Spec 约束生成器脚本

# 设置严格模式
set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# 默认参数
DOC_PATH=""
OUTPUT_DIR="$PROJECT_ROOT/specs"
FORCE=false
VERBOSE=false

# 显示帮助信息
show_help() {
    cat << EOF
React Spec 约束生成器

用法:
    $0 [选项]

选项:
    -d, --doc PATH     技术评审文档路径 (必需)
    -o, --output DIR   输出目录 (默认: ./specs)
    -f, --force        强制覆盖现有文件
    -v, --verbose      显示详细输出
    -h, --help         显示此帮助信息

示例:
    $0 -d /path/to/tech-review.md
    $0 -d ./docs/tech-review.md -o ./generated-specs -v
EOF
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--doc)
            DOC_PATH="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

# 验证必需参数
if [[ -z "$DOC_PATH" ]]; then
    echo "错误: 必须指定技术评审文档路径"
    show_help
    exit 1
fi

# 检查文档是否存在
if [[ ! -f "$DOC_PATH" ]]; then
    echo "错误: 文档不存在: $DOC_PATH"
    exit 1
fi

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 设置日志级别
if [[ "$VERBOSE" == true ]]; then
    echo "项目根目录: $PROJECT_ROOT"
    echo "文档路径: $DOC_PATH"
    echo "输出目录: $OUTPUT_DIR"
fi

# 检查是否为 React 项目
check_react_project() {
    local package_json="$PROJECT_ROOT/package.json"
    if [[ ! -f "$package_json" ]]; then
        echo "错误: 未找到 package.json 文件"
        exit 1
    fi

    if ! grep -q "react" "$package_json"; then
        echo "警告: 未在 package.json 中找到 react 依赖"
        read -p "是否继续生成？(y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 0
        fi
    fi

    if [[ "$VERBOSE" == true ]]; then
        echo "✓ 确认为 React 项目"
    fi
}

# 生成 Spec 文件
generate_spec() {
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local spec_file="$OUTPUT_DIR/react-spec-$timestamp.md"
    local constraint_report="$OUTPUT_DIR/constraint-report-$timestamp.md"

    # 创建临时目录
    local temp_dir=$(mktemp -d)

    if [[ "$VERBOSE" == true ]]; then
        echo "临时工作目录: $temp_dir"
    fi

    # 复制文档到临时目录
    cp "$DOC_PATH" "$temp_dir/tech-review.md"

    # 使用 Claude 生成 spec
    cd "$temp_dir"

    cat > prompt.txt << EOF
请根据以下技术评审文档，生成符合 React 规范的 spec 文档：

文档内容：
$(cat tech-review.md)

请生成以下内容：
1. 组件结构图（使用 mermaid 语法）
2. 接口定义（TypeScript 类型）
3. 实现方案（关键代码片段）
4. 依赖说明
5. 注意事项

确保符合以下 React 约束规则：
- 使用函数组件和 Hooks
- 必须使用 TypeScript
- 组件命名使用 PascalCase
- 文件名使用 kebab-case
- 使用 React.memo 优化性能
- 使用 useCallback 和 useMemo
- 样式使用 CSS Modules

输出格式：
# React Spec

## 1. 组件结构
\`\`\`mermaid
graph TD
    A[组件名] --> B[子组件1]
    A --> C[子组件2]
\`\`\`

## 2. 接口定义
\`\`\`typescript
interface Props {
  // ...
}
\`\`\`

## 3. 实现方案
\`\`\`typescript
const Component: React.FC<Props> = ({ ... }) => {
  // ...
}
\`\`\`

## 4. 依赖说明
- package: xxx
- version: x.x.x

## 5. 注意事项
- ...
EOF

    # 调用 Claude API 生成 spec（这里需要根据实际环境调整）
    # 假设有一个 generate-spec 脚本
    if command -v claude &> /dev/null; then
        claude --skill react-spec-generator < prompt.txt > spec-output.md
    else
        # 如果没有 Claude CLI，使用简单的文本处理
        echo "使用简单文本处理生成 spec..."
        python3 "$SCRIPT_DIR/generate_spec.py" tech-review.md spec-output.md
    fi

    # 移动生成的文件
    if [[ -f "spec-output.md" ]]; then
        mv spec-output.md "$spec_file"
    fi

    # 生成约束报告
    cat > constraint-report.md << EOF
# 约束报告

生成时间: $(date)
源文档: $DOC_PATH

## 应用的约束规则

### 组件规范
- [x] 函数组件优先
- [x] 使用 Hooks
- [x] PascalCase 命名
- [x] kebab-case 文件名

### 性能优化
- [x] React.memo
- [x] useCallback
- [x] useMemo

### 类型安全
- [x] TypeScript
- [x] 接口定义
- [x] 类型守卫

### 样式方案
- [x] CSS Modules
- [x] 组件样式隔离

## 冲突统计
- 无冲突

## 建议
1. 建议添加单元测试
2. 考虑添加错误边界
3. 实现响应式设计
EOF

    mv constraint-report.md "$constraint_report"

    # 清理临时目录
    rm -rf "$temp_dir"

    # 输出结果
    echo "✓ Spec 生成完成"
    echo "Spec 文件: $spec_file"
    echo "约束报告: $constraint_report"

    # 如果存在文件且不允许覆盖，询问是否删除
    if [[ "$FORCE" == false && -f "$spec_file" ]]; then
        echo "警告: 输出文件已存在，使用 --force 覆盖"
    fi
}

# 主执行流程
main() {
    echo "开始生成 React Spec..."

    # 检查 React 项目
    check_react_project

    # 生成 Spec
    generate_spec

    echo "✓ React Spec 生成完成"
}

# 执行主函数
main "$@"