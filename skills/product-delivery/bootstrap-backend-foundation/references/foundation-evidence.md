# 底座 Evidence

`BACKEND_FOUNDATION_PASSED` 至少需要：

- 入口启动、health、readiness、优雅退出。
- 错误和日志样例，secret/PII 已脱敏。
- 配置覆盖与缺失配置失败路径。
- migration 在隔离数据库的 apply/兼容/恢复证据（适用时）。
- auth/permission 拒绝路径（适用时）。
- contract test、unit/integration totals。
- 完整 diff Review 与 P0–P3。
- 未验证项、残余风险与回退点。
