# 后端底座合同

## 必需能力按需选择

- 启动入口、模块边界、优雅退出。
- 配置优先级、secret 来源、日志脱敏。
- health/readiness 与依赖降级。
- 统一 error envelope、日志和 trace。
- 数据库、事务、migration 与测试隔离（适用时）。
- authentication、authorization、tenant 隔离（适用时）。
- API/事件合同校验。
- unit/integration/contract/smoke 入口。

## 禁止

- 在合同外提前实现业务。
- 把 secret 放入源码、命令参数、日志或交付文件。
- 用自动 migration 写生产。
- 两个 Worker 同时改入口/schema/migration。
- 只因框架惯例加入未确认的队列、缓存、云服务或账号体系。
