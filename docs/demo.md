# 真实演示记录与复现边界

## 记录身份

2026-10-15，本地Windows，Python3.13.9、Node24.16.0/npm11.13.0。使用原应用，不替换模型、检索、数据库或身份依赖；远端兼容LLM通过真实SDK调用，本地Embedding/Reranker/Chroma和新PostgreSQL演示库参与执行。

原始截图来自同一版本的Codex内置浏览器。只载入[合成文档](../data/synthetic_handbook.md)，1篇文档、2分块，chunk256/overlap32，沿用已配置重排阈值。开发身份、签名键、服务资格、数据库和索引均独立生成；没有读写原业务会话表。Token、连接串、真实资料与运行日志不公开。

## 已实际执行的流程

| 步骤 | 输入或动作 | 观察结果 |
|---|---|---|
| 进入应用 | 原凭证入口使用临时合成身份 | 服务就绪，空会话；没有依赖override |
| 知识库问答 | 星舟演示组织的设备预约需要提前多久、在哪里提交、由谁确认？请依据知识库回答。 | 两个演示工作日、星舟预约板、演示管理员；引用synthetic_handbook.md，提醒虚构资料 |
| 连续追问 | 刚才说要提前多久？预约板和确认人分别是什么？ | 保持同会话语境的三个要点，形成第2轮 |
| 恢复历史 | 新建空会话→刷新→凭据清空→重新认证 | 恢复原会话2轮；没有重新生成模型答案 |
| 只读复核 | GET健康/会话/轮次，再读新演示库与本scope Checkpoint | 四类HTTP均200，2轮completed，API/SQL逐字段一致，metadata活动状态释放 |

Checkpoint有3条带usage的主Agent AIMessage、2条research工具结果，均has_evidence，各保留1候选，公开来源去重为1项。主Agent消息数不等于包括SDK重试/内部改写在内的总请求或计费次数。

第1轮duration_ms=14467，第2轮3590，口径为业务asked_at至answered_at；不是纯检索耗时、首Token时间或性能基准。2个成功问题也不是通用答案质量保证。

## 截图索引

| 原始文件 | 尺寸 | 输入/输出与能力 |
|---|---|---|
| [知识库回答](images/01-knowledge-answer.jpg) | 1265×1101 | 首问输出三条合成规则和来源；展示工具/证据/回答/落库链路 |
| [连续追问](images/02-context-followup.jpg) | 1265×1609 | 追问沿用上轮信息，两轮同屏；展示上下文而非只显示历史 |
| [刷新恢复](images/03-restored-history.jpg) | 1265×712 | 重新认证后的历史末轮视口；展示服务端历史读取 |

图像未拼接、未改写，未使用设计稿、静态页面或Mock输出；无EXIF。SHA-256及核验摘要见[evidence.json](evidence.json)。

## 本地原应用怎样启动的

**这些是原本地应用的执行记录，不是本公开仓库可以直接运行的命令。** 业务源码、测试和隔离启动脚本暂未公开；在没有它们时，不应把下面命令当作完整复现入口。

```text
uv pip check --python <已安装Python>
npm ci --offline --ignore-scripts --no-audit --no-fund
<Python> tools/live_demo.py prepare --source-env <私有配置.env> --runtime-dir <项目外空目录>
<Python> tools/live_demo.py serve --runtime-dir <运行目录> --port <本机端口>
<Python> tools/live_demo.py frontend --runtime-dir <运行目录> --backend-port <后端端口> --port <前端端口>
<Python> tools/verify_live_demo.py --runtime-dir <运行目录> --port <后端端口>
```

实际依赖检查192包兼容、npm缓存安装108包；prepare新建演示库与独立索引成功，HTTP/SQL/Checkpoint只读校验退出0。Python复用已有环境，干净环境安装未验证。后台进程仅绑定回环地址；初始权重预热时曾连接失败，等待ready200后完成演示，不是绕过健康检查。

外部完整复现还需：经许可的完整源码、依赖锁/运行环境、可用模型凭据与规格、本地授权Embedding/Reranker权重、可建库的独立本地PG、临时JWT与成员配置。配置示例仅列[变量名和空值](../.env.example)，不包含可运行凭据。

## 本公开仓库可以复核什么

```bash
python tools/check_showcase.py
```

仅校验公开文件、链接、敏感模式、合成资料和原图哈希，不启动应用、不调用模型。原本地测试的范围和限制见[evaluation.md](evaluation.md)。

## 已知限制

此次没有验证服务器重启续跑、并发/容量、审批、预算故障、无证据拒答、跨用户/文档ACL、移动端或生产部署。页面仍按原纯文本显示Markdown星号，凭据栏样式基础。原模型可能发出多次工具调用，没有明确有界重检索合同。业务与参考源码的公开许可仍待确认。
