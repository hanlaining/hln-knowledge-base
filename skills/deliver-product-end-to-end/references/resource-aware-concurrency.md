# 资源自适应并发

## 原则

不设置固定窗口数，设置资源、依赖和写入冲突上限。每轮逐个扩容；`hard_limit: null` 不等于无视机器极限。

## 状态

- `GREEN`：内存、Swap、load、磁盘和 Review 队列稳定，可继续启动。
- `YELLOW`：保持 active Worker，只允许 light 或不再启动。
- `RED`：停止所有新启动，让 active Worker安全到达交付点。

## 资源等级

- `light`：文档、只读调研、小型合同测试。
- `medium`：普通页面、单模块接口、单元测试。
- `heavy`：全量构建、浏览器 E2E、数据库 smoke、大型集成测试。

## 强制约束

- 每轮默认最多新增一个 heavy Worker。
- Review backlog 大于可审容量时暂停扩容。
- 模型限流、频繁网络错误和前台明显卡顿视为 YELLOW/RED 信号。
- 资源恢复后重新计算 ready，不重复启动已 active Issue。
- 不自动杀进程；停止/终止必须精确目标并遵守任务授权。

脚本输出只是调度 Evidence，不替代主 Codex 对写入冲突和授权的判断。

资源快照默认拒绝覆盖已有文件，输出使用新的 `.json` 路径。只有已核对目标确为旧快照时才显式传 `--overwrite`；不得把配置、合同、Evidence 或业务 JSON 当成快照输出目标。
