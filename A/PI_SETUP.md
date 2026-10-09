# A — Pi 主智能体（独立计算机）

在 A 的 Pi 安装官方 OpenAaaS 扩展：

```powershell
pi install npm:open-aaas-pi-extension
pi
```

在 Pi 中 `/reload` 后对主智能体发送：

> 请调用 OpenAaaS 工具，用 `set_server_url` 将新的服务器别名 `course-c` 设置为 `https://YOUR-C-DOMAIN`，然后在 `course-c` 上 register，列出两个 AFLOW Agent 服务。按问题分别向 AFLOW Query 和 AFLOW Statistics 提交任务，取得结果文件并汇总。所有远程通信只能通过 C。

官方工具 action：`set_server_url`、`register`、`list_services`、`submit_task`、`get_task`、`download_result`。

注意：官方 Pi 扩展会自动跟踪任务进度，结果完成后再下载；不要向 A 填写 B 的私网 IP 或端口。A 只能知道 C 的公网 HTTPS 域名和服务 ID。
