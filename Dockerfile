FROM python:3.11-slim

WORKDIR /app

# Install dependencies first so this layer is cached independently of source changes
COPY setup.py .
RUN mkdir -p mcp_curation && touch mcp_curation/__init__.py \
    && pip install --no-cache-dir -e . \
    && rm -rf mcp_curation

COPY mcp_curation/ mcp_curation/

ENV MCP_API_KEY="test"
ENV SBML_API_BASE_URL="http://localhost:8080"
ENV CORS_ALLOW_ORIGINS="http://192.168.1.22:90"

EXPOSE 8000

# Example CMD run
# CORS_ALLOW_ORIGINS="http://192.168.1.22:90"
# MCP_API_KEY='modelseed'
# SBML_API_BASE_URL='http://192.168.1.202:8080/'
# uv run --python .venv/bin/python uvicorn mcp_curation.main:app --host 0.0.0.0 --port 7800 --reload

CMD ["uvicorn", "mcp_curation.main:app", "--host", "0.0.0.0", "--port", "7800"]
