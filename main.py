import os

import dlt
from dlt.extract import DltSource
from dlt.sources.helpers.rest_client.auth import APIKeyAuth
from dlt.sources.helpers.rest_client.paginators import JSONLinkPaginator
from dlt.sources.rest_api import rest_api_source
from dlt.sources.rest_api.typing import ClientConfig, RESTAPIConfig
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN not found in environment. Please set it in .env")

client: ClientConfig = {
    "base_url": "https://kobo.impact-initiatives.org/api/v2/",
    "auth": APIKeyAuth(
        name="Authorization", api_key=f"Token {TOKEN}", location="header"
    ),
    "paginator": JSONLinkPaginator(),
}

config: RESTAPIConfig = {
    "client": client,
    "resource_defaults": {
        "write_disposition": "append",
        "endpoint": {
            "params": {
                "format": "json",
            },
        },
    },
    "resources": [
        {
            "name": "assets",
            "endpoint": {
                "path": "assets/",
            },
            "primary_key": ["uid"],
        },
        {
            "name": "content",
            "endpoint": {
                "path": "assets/{resources.assets.uid}/content",
                "data_selector": "data",
            },
            "include_from_parent": ["uid"],
            "primary_key": ["_assets_uid"],
        },
    ],
}

source: DltSource = rest_api_source(config)

pipeline = dlt.pipeline(
    pipeline_name="kobo_de",
    destination="duckdb",
)

if __name__ == "__main__":
    load_info = pipeline.run(source)
    print(load_info)
