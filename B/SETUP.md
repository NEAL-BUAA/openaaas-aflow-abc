# B — 数据节点：Docker 多子智能体

**必须在 B 的机器上操作**，不要在 A 机器运行这些服务。B 只访问 C 的 HTTPS 地址，不接受来自 A 的网络连接。

## 1. 数据准备

获取你有权限使用的 AFLOW CSV 导出文件；本仓库不包含真实 AFLOW 数据。CSV 至少包含 `auid,compound`，还支持 `prototype,spacegroup_relax,Egap,energy_atom,aurl`。

```bash
python3 import_aflow.py /path/to/aflow-export.csv
```

这会创建 `aflow-data/aflow.sqlite`。不导入数据就不能声称 AFLOW 已部署。文件必须是真实 AFLOW 数据镜像，而非示例造数。

## 2. Docker 镜像

安装 Docker Engine / Docker Desktop。运行：

```bash
bash build-images.sh
```

两个独立的容器执行器镜像 `abc-aflow-query` / `abc-aflow-stats` 均内置 Pi 和只读数据库工具。每个被认领任务由 Agent Core 启动单独容器，单个 Agent Core `capacity=2` 允许最多两个并发任务，两个 Agent Core 共可调度多个容器。

## 3. Pi 模型认证

在 B 准备 `pi-agent-auth/`（**不要提交 GitHub**），其中包含 B 上 Pi 所需的认证/模型配置。确保 `/home/worker/.pi/agent` 可读并匹配当前 Pi 版本及模型提供商。不要将 API Key 写入 Dockerfile、仓库或日志。对 DeepSeek 的 API 调用发生在 B 侧容器内，因此 B 需要对模型 API 有出站网络访问。

## 4. 下载官方 agent-core 并初始化

从 OpenAaaS 官方 releases 下载 `agent-core` 可执行文件，在两个分开的 B 工作目录运行：

```bash
mkdir -p runtime-query runtime-stats
cd runtime-query
/path/to/agent-core init
cd ../runtime-stats
/path/to/agent-core init
```

将 `config/agent-query.toml.example` 和 `config/agent-stats.toml.example` 分别用作两份 `config.toml` 的参考，注意保留 init 生成的其他有效配置字段。替换 `https://YOUR-C-DOMAIN`、`REPLACE_WITH_ABSOLUTE_B_PATH` 为实际值。每个配置必须有独立的数据目录和身份，不要把两份 `service_id`/`api_key` 混用。

## 5. 注册两个 Agent Core

C 管理员分别创建两个服务并提供两枚 **不同注册 Token**。在 B 上：

```bash
cd runtime-query
/path/to/agent-core register --token 'QUERY_TOKEN_FROM_C' --name 'aflow-query-node'
/path/to/agent-core run
```

打开 B 的第二个终端：

```bash
cd runtime-stats
/path/to/agent-core register --token 'STATS_TOKEN_FROM_C' --name 'aflow-stats-node'
/path/to/agent-core run
```

分别查看 `/path/to/agent-core status`。如有注册错误，先确认到 C 的 HTTPS 出站可达和服务 token 是否匹配。

注意容器的 `/workspace/task.json` 是 OpenAaaS Agent Core 挂载的真实任务；执行器写 `/workspace/response.md`，agent-core 扫描并回传给 C。A 再经 C 的 OpenAaaS API 得到结果。
