# C — OpenAaaS 公网中转服务器

C **必须是有公网可达 HTTPS 域名的独立服务器**。此仓库不包含真实云主机、公网域名或凭据。

从上游 https://github.com/Wolido/OpenAaaS/releases 下载对应操作系统的 `open-aaas-server` 与 `openaaas-admin` 二进制，或从 `server/` 和 `admin-cli/` 使用 Rust 编译。

1. 在 C 的独立工作目录执行 `open-aaas-server run`。首次启动自动生成 `config.toml`、SQLite 和 Admin API Key。只在 C 保存 Admin Key。
2. 服务默认 `0.0.0.0:8080`，通过 Caddy/Nginx 配置 HTTPS 域名反向代理到 `127.0.0.1:8080`。生产环境应让服务只绑定 loopback 或由防火墙封闭 8080，不要直接公网暴露 HTTP 管理接口。
3. 在 C 配置 `openaaas-admin config init`。执行 `openaaas-admin health`。
4. 执行两次服务创建：

```bash
openaaas-admin services create --name "AFLOW Query Agent" --description "Read-only local AFLOW materials record queries on B" --usage "Task prompt: query AFLOW mirror by compound / gap; returns response.md with auid and aurl" --public
openaaas-admin services create --name "AFLOW Statistics Agent" --description "Summaries of the local AFLOW mirror on B" --usage "Task prompt: count records/compounds and summarize AFLOW mirror; output response.md" --public
```

**保留每个服务创建返回的注册 token**，并在 B 对应的 agent-core `register --token ...` 使用（切勿提交 GitHub）。公共服务仅用于课程演示；真实材料数据库或敏感研究需设置为受限服务并授予 A 的 client 权限。

C 只保存路由元数据、任务描述、结果和传输文件；AFLOW 原始数据库只存放 B。OpenAaaS 并非端到端加密的数据秘密计算系统，C 管理员能够接触到经 C 传输的任务和结果。
