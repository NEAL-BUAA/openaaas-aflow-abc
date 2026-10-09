# 作业 2 — A → C → B → C → A（OpenAaaS + Pi + Docker + AFLOW）

本项目基于 [Wolido/OpenAaaS](https://github.com/Wolido/OpenAaaS) 的 **Server / Agent Core / Pi Extension** 构建课程示例。未修改或复制完整上游源码；依赖其公开发布的组件。

```text
机器 A（Pi orchestrator）         机器 C（公网 OpenAaaS Server）           机器 B（本地 AFLOW）
       |                                       |                                  |
       |-- HTTPS register/list/submit ------->|                                  |
       |                                       |<--- HTTPS agent-core poll -------|
       |                                       |---- task via poll response ----->|
       |                                       |                    Docker Worker 1: Query
       |                                       |                    Docker Worker 2: Statistics
       |                                       |<--- HTTPS result upload ---------|
       |<----------- HTTPS result ------------|                                  |
```

**禁止 A ↔ B 直接通信。** A 配置只含 C 的公网 URL；B 也只含 C 的公网 URL。B 的 AFLOW SQLite 镜像只读挂载到 Docker 中。`agent-core` 可在单机 B 启动两个节点（每节点 capacity=2），并发执行不同 Docker worker 任务。

## 文件导航

- `A/PI_SETUP.md`: A 的 Pi 安装和任务提交
- `C/SETUP.md`: C 的公网 Server 和服务注册
- `B/SETUP.md`: B 的两个 Agent Core、Docker、AFLOW 数据镜像
- `B/import_aflow.py`: 从真实 AFLOW CSV 导入本地 SQLite
- `B/executor/`: OpenAaaS Docker executor 契约、Pi 运行与只读 AFLOW 数据查询
- `tests/test_local.py`: 无网络/无 LLM 的脚本级测试

## 先决条件

三台机器（或三台独立 VM）：A 有 Pi + DeepSeek API 配置；C 有公网 HTTPS + OpenAaaS Server；B 有 Docker + OpenAaaS Agent Core + 合法 AFLOW CSV 镜像 + 可用 Pi 模型凭据。AFLOW 的完整公开数据库没有随项目下载或捆绑；需自行导入。

## 上游依据

OpenAaaS 文档说明 Agent Core **主动短轮询 C**，C 完成委派路由、心跳和结果中转；Docker executor 使用 `/workspace/task.json` 输入和 workspace 输出契约。这恰好支持 B 位于 NAT 后，没有公网入口的架构。

## 网络隔离与验收

1. A 主机只需 C 的 DNS 和 443 出站；不要向 A 配置 B 的 IP。
2. B 主机安全组/防火墙禁止来自 A 的入站，关闭 B 的公网端口；仅放行 B→C:443，以及 B→必要的模型 API 域名。B 不应拥有 A 的直接地址。
3. C Server 必须是**真实独立公网主机**；如果三者都在一台电脑的三个容器中，只能算拓扑模拟，不能声称异地公网部署。
4. 检查 C 注册了两个 Agent Core；向 Query/Stats 服务分别提交任务；在 B 日志中确认任务分别由两个 Docker 镜像执行；A 通过 C 获取 `response.md`。
5. **反事实检验**：停止 C 后 A 不应能提交新任务、B 不应认领新任务。恢复 C 后可恢复路由。不要用 A 直接调用 B 的私网 IP 充当成功。

## 注意

这里提供完整脚本、配置模板与部署流程，但当前尚未在你的真实 A/B/C 三台机器上执行公网联调。若缺乏 C 公网主机、B 数据文件或 B 的模型凭据，本项目不应被称为已完成远端端到端运行。
