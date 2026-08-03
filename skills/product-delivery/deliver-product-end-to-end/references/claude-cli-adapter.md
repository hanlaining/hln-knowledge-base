# Claude Code 本机适配事实

## 2026-08-03 核对结果

- 可执行文件：使用 `command -v claude` 获取，不在公开 Skill 中写死本机路径。
- 当前版本：Claude Code `2.1.185`
- 交互入口：位置参数 prompt；`-p/--print` 是非交互模式，不用于可见持续 TUI。
- 已确认参数：`--permission-mode` 支持 `bypassPermissions`、`auto`、`acceptEdits`、`default`、`dontAsk`、`plan`；`--append-system-prompt`、`--worktree`、`--tmux` 仍存在。
- 工作目录继续由 Akasha runner 的 `cd` 与 tmux `new-session -c` 双重锁定，不让 CLI 自行猜目录。
- `bypassPermissions` 只减少 Claude 工具确认，不扩大用户授权；Git、外部写入、付费、生产和不可逆动作仍由 hln 规则逐项审批。

Akasha 上游 `cli-contract.md` 记录的是 `2.1.72`。当前所需启动参数在 `2.1.185` 中仍兼容，因此不修改上游仓库；每次 Claude 版本变化后先重新运行 `--version` 与 `--help`，再更新本适配事实。
