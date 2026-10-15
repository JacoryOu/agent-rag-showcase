# 验证与评测说明

区分真实模型/数据库、受控测试、静态检查。下列原应用结果来源于2026-10-15本地执行记录和此前保留的测试报告；本仓库不附完整用例/原始日志，不能宣称第三方clone后可复现这些成绩。本次发布整理没有重新调用模型或重跑业务套件。

## 1. 最近的真实闭环

1篇合成文档、2个分块、1个会话、2轮问答。真实LLM/Embedding/FlagReranker/Chroma/PostgreSQL/React/FastAPI及浏览器参与：

- 知识库答案的三个要点与合成文档一致，公开来源为synthetic_handbook.md。
- 同会话追问正确保持上轮信息；刷新清空页面内存凭据后重新认证，历史从服务端恢复。
- live/ready/会话列表/轮次HTTP均200；SQL与HTTP的编号、问题、答案、状态、来源一致；活动状态释放。
- Checkpoint持久化：3条主Agent AIMessage带usage；2条research结果均has_evidence，各保留1候选。不是SDK总请求计费数量。
- 仓库轮次耗时14467/3590ms只是两个示例，不能作为平均延迟、P95、检索耗时或TTFT。

复核范围、原图哈希、实际问题和条件见[demo.md](demo.md)、[evidence.json](evidence.json)。没有Mock替代真实链路，也没有把生成截图当作程序截图。

## 2. 已执行的原应用自动检查

| 批次/条件 | 实际结果 | 证明与限制 |
|---|---|---|
| 展示副本首次默认后端检查，无模型权重 | 465 passed、3 failed、3 skipped；374.27秒，退出1 | 3失败用例实际加载真实Embedding，因无可用权重目录失败；不隐藏失败或改断言 |
| 显式离线范围复测，Node依赖已安装 | 466 passed、2 skipped、3 deselected；360.70秒，退出0 | 2跳过为真实PG开关关闭；3排除为前述权重用例。包含实际TS消费者→本地HTTP→受控业务链路，不是收费模型 |
| 前端Vitest/jsdom | 14 passed，3文件；4.43秒，退出0 | 受控UI/凭证/解析测试，不证明浏览器视觉或生产部署 |
| TypeScript/Vite构建 | tsc -b与Vite build通过，18模块 | 编译打包，不是上线 |
| 真实演示期间针对性离线检查 | 16 passed；15.41秒，退出0 | 证据子图、工具、公开结果3文件；与真实截图链路分开，不是重跑全回归 |
| 真实演示依赖检查 | uv pip check：192包兼容；npm离线缓存安装108包 | 不是干净Python安装或无缓存安装证明 |

未排除前的3项失败：test_build_initial_rag_index_rejects_nonempty_collection、test_build_initial_rag_index_builds_collection_and_returns_report、test_open_existing_rag_runtime_retrieves_from_built_index。原因链为build_initial_rag_index→build_embedding_from_settings→本地权重目录不存在；后续离线入口明确deselect，不把它们改成Fake通过。受控网络故障测试有过Windows连接中止线程日志，最终断言状态按各批结果记录。

原应用代表性定位：test_evidence_rag_subgraph_stage_f.py、test_knowledge_base_tool_stage_f.py、test_context_budget_middleware.py、test_model_sdk_network_day1.py、test_model_sdk_sse_day1.py、test_tenant_membership_alignment.py、test_readiness_revision_audit.py。这些文件当前未公开；名称提供追溯线索，不是本仓库可运行测试入口。

## 3. 候选证据筛选开发实验

原本地2026-09-15的v2开发实验：1篇手册类演示文档、8个查询，TopK设置5。512/64配置每查询实际2候选，共16；256/32每查询4候选，共32。原始正文、快照和标注不随本仓库发布，不能外部完整重跑。这里仅摘非业务内容的统计及口径。

| 分块/重叠 | 阈值 | TP/FP/FN/TN | Precision | Recall |
|---|---:|---|---:|---:|
| 512/64 | 0.50 | 7/0/1/8 | 7/7=100% | 7/8=87.5% |
| 512/64 | 0.70 | 6/0/2/8 | 6/6=100% | 6/8=75% |
| 256/32 | 0.70 | 7/1/0/24 | 7/8=87.5% | 7/7=100% |
| 256/32 | 0.80 | 6/0/1/25 | 6/6=100% | 6/7≈85.71% |

严格score > threshold才保留。Precision=保留相关候选/全部保留候选；Recall=保留相关候选/该次已召回集合中标为相关的候选。这是**候选内筛选指标**，不是全库Recall@K、最终答案准确率或满意度。跨分块的相关单元数不同，不能直接换算系统回答能力。

同一256配置阈值0.8→0.7，候选Recall增加14.29个百分点，同时Precision下降12.5个百分点，是取舍，不写成系统准确率提升。样本用于开发调参，没有独立留出测试集或泛化证明。合成公开文档不是这份历史开发集，不能拿新文档冒充原分数的复现。

## 4. 未测或无依据

独立答案质量/引用忠实度/无证据拒答率测试集、全库检索指标、并发QPS、P50/P95/P99、TTFT、成本收益、用户量与生产稳定性均未测或无原始依据。没有GPU/容器/多平台/公网部署验收；没有微调训练、Skill沙盒或认知IP成果。

公开材料检查工具本身的运行结果仅说明材料通过规则检查，不能折算为业务单元测试、真实模型调用或生产验证。
