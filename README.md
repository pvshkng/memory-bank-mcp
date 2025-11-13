# FastMCP Memory Bank Server
A FastMCP application built for managing user-related memory in Upstash Redis.

## Prerequisites
- Python >= 3.11
- uv (install using pip install uv or https://docs.astral.sh/uv/)
- Upstash Redis Instance (https://upstash.com/)
- Docker Desktop
- Docker Compose

## Running the standalone project
1. Install prerequisites 
2. Run ```uv venv``` to create a virtual environment
3. Run ```./.venv/Scripts/activate``` (Windows) or ```source ./.venv/bin/activate``` (MacOS)
4. Run ```uv sync``` to install dependencies
5. Copy ```.env.example``` to ```.env``` and add Upstash endpont and API key there
6. Run ```fastmcp run main.py:mcp --transport http --port 8000```
7. Or run with docker by ```docker build -t memory-bank-mcp .``` and ```docker run -p 8000:8000 --env-file .env memory-bank-mcp```
8. Connect to the server at ```http://127.0.0.1:8000/mcp``` using MCP Inspector, Postman or your custom MCP client.