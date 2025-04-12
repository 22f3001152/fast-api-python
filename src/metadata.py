from pathlib import Path

import toml


def fetch_project_metadata():
    metadata = {
        "version": "unknown",
        "title": "unknown",
        "description": "unknown",
        "docs_url": "/docs",
        "api_url": "/api",
        "openapi_url": "/openapi.json",
        "openapi_tags": [
            {
                "name": "default",
                "description": "Default tag for all endpoints",
            },
        ],
        "openapi_version": "3.0.3",
    }
    pyproject_toml_file = Path(__file__).parent.parent / "pyproject.toml"
    if pyproject_toml_file.exists() and pyproject_toml_file.is_file():
        data = toml.load(pyproject_toml_file)
        if "project" in data:
            metadata["version"] = data["project"].get("version", "FAStAPI")
            metadata["title"] = data["project"].get("name", "unknown")
            metadata["description"] = data["project"].get("description", "unknown")

    return metadata
