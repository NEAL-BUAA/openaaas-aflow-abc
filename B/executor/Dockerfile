FROM node:22-bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends python3 ca-certificates && rm -rf /var/lib/apt/lists/*
RUN npm install -g --ignore-scripts @earendil-works/pi-coding-agent
RUN useradd --create-home --shell /bin/sh worker
COPY runner.py /opt/runner.py
COPY aflow_tool.py /opt/aflow_tool.py
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod 755 /opt/entrypoint.sh && mkdir -p /workspace && chown worker:worker /workspace
ARG AFLOW_ROLE=query
ENV AFLOW_ROLE=${AFLOW_ROLE}
USER worker
WORKDIR /workspace
ENTRYPOINT ["/opt/entrypoint.sh"]
