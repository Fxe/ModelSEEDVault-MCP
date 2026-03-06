from setuptools import find_packages, setup

setup(
    name="mcp-curation",
    version="0.1.0",
    description="ModelSEEDVault MCP curation server",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.110",
        "uvicorn[standard]>=0.27",
        "fastmcp>=2.0.0",
    ],
)
