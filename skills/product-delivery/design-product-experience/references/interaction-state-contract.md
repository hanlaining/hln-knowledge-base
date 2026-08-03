# 交互状态合同

每个核心动作记录：入口、触发、即时反馈、进行中、成功、失败、取消、返回、恢复和权限拒绝。

每个交互组件检查：default、hover、focus-visible、active、disabled、loading、keyboard、screen-reader name。

每个页面检查：initial、loading、content、empty、partial、error、offline、unauthorized、forbidden。

点击验收脚本使用用户语言：

```text
从哪里进入
→ 点击什么
→ 输入什么
→ 故意制造哪个失败
→ 如何修正
→ 成功后看到什么
→ 返回后状态是否保留
```

动效必须写 duration/easing/触发/退出和 reduced-motion 替代，不只写“丝滑”。
