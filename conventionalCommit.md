# Conventional Commits 约定式提交

约定式提交规范是一种基于提交消息的轻量级约定。它提供了一组简单规则来创建清晰的提交历史；这更有利于自动化工具的编写。通过在提交消息中描述功能、修复和破坏性变更，让这种约定更符合[语义化版本 (SemVer)](http://semver.org/lang/zh-CN/)。

## 格式

```bash
git commit -m "<类型>: <描述>"
```

## 类型 (Type)

以下是常用的提交类型：

*   **feat**: 新增功能 (feature)。
    *   示例: `feat: 增加用户注册功能`
*   **fix**: 修复缺陷 (bug fix)。
    *   示例: `fix: 修复登录页面无法跳转的问题`
*   **docs**: 文档 (documentation)变更。
    *   示例: `docs: 更新 README.md 中的项目描述`
*   **style**: 代码格式调整，不影响代码含义 (空格、格式化、缺少分号等)。
    *   示例: `style: 调整代码缩进和空格`
*   **refactor**: 代码重构，既不修复错误也不添加功能。
    *   示例: `refactor: 重构用户认证模块`
*   **perf**: 性能 (performance) 优化。
    *   示例: `perf: 优化图片加载速度`
*   **test**: 增加测试或修改现有测试。
    *   示例: `test: 为用户服务添加单元测试`
*   **build**: 影响构建系统或外部依赖关系的更改 (例如: gulp, broccoli, npm)。
    *   示例: `build: 更新 webpack 配置`
*   **ci**: 更改持续集成文件和脚本 (例如: Travis, Circle, BrowserStack, SauceLabs)。
    *   示例: `ci: 修改 GitHub Actions 配置文件`
*   **chore**: 其他不修改 `src` 或 `test` 文件的更改。
    *   示例: `chore: 更新依赖包版本`
*   **revert**: 撤销 (revert) 之前的提交。
    *   示例: `revert: 回滚到上一个稳定版本`

## 描述 (Description)

描述是类型和可选作用域之后的简短说明，概括了本次提交的变更内容。
