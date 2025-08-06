#!/usr/bin/env python3

import os
import sys
import requests
from typing import List, Optional, Dict, Any
from mcp.server.fastmcp import FastMCP
from schemas import SingulApp, SingulAppSearchResult

# sys.stderr = open(os.devnull, 'w')

api_key = os.environ.get("SHUFFLE_API_KEY")
shuffle_url = os.environ.get("SHUFFLE_URL", "https://shuffler.io")

singul = None

if api_key:
    try:
        from shufflepy import Singul
        singul = Singul(api_key, url=shuffle_url)
    except Exception:
        pass

mcp = FastMCP("Singul MCP Server")

@mcp.tool()
def singul_connect(
    app: str,
    action: str, 
    fields: List[Dict[str, Any]],
    environment: Optional[str] = None
) -> Dict[str, Any]:
    """
    Connect to any API available from Singul search and perform an action.
    
    Args:
        app: The name of the app to connect to (e.g., 'slack', 'jira')
        action: The action to perform (e.g., 'list_messages', 'create_ticket')
        fields: A list of key-value pairs for the action
        environment: Optional environment name to run the execution in
    
    Returns:
        The result from the Shuffle operation
    """
    if not singul:
        return {
            "error": "Shuffle client not initialized. Please check SHUFFLE_API_KEY environment variable."
        }
    
    try:
        connect_args = {
            "app": app,
            "action": action,
            "fields": fields,
        }
        if environment:
            connect_args["environment"] = environment

        result = singul.connect(**connect_args)
        return result
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def search_singul_apps(query: str = "") -> SingulAppSearchResult:
    """
    Search available Singul apps (APIs of 3rd party services) and their actions that can be performed.
    
    Args:
        query: Search term to find apps (e.g., 'slack', 'jira', 'security')
    
    Returns:
        SingulAppSearchResult: Structured search results with app names, descriptions, and available actions
    """
    try:
        # Algolia search URL and headers
        url = "https://jnss5cfdzz-dsn.algolia.net/1/indexes/*/queries"
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'x-algolia-agent': 'Algolia for JavaScript (4.24.0); Browser (lite); JS Helper (3.14.0); react (18.3.1); react-instantsearch (6.40.4)',
            'x-algolia-api-key': 'c8f882473ff42d41158430be09ec2b4e',
            'x-algolia-application-id': 'JNSS5CFDZZ'
        }
        
        # Search payload
        payload = {
            "requests": [
                {
                    "indexName": "appsearch",
                    "params": f"clickAnalytics=true&facets=%5B%5D&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&query={query}&tagFilters="
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        results = data.get("results", [])
        
        if not results:
            return SingulAppSearchResult(
                query=query,
                total_hits=0,
                apps=[],
                error="No results found"
            )
        
        hits = []
        total_hits = 0
        for result in results:
            if result.get("index") == "appsearch":
                hits = result.get("hits", [])
                total_hits = result.get("nbHits", 0)
                break
        
        if not hits:
            return SingulAppSearchResult(
                query=query,
                total_hits=0,
                apps=[],
                error="No hits found in appsearch index"
            )
        
        apps = []
        for hit in hits[:20]:  # will change this soon
            app = SingulApp(
                name=hit.get("name", ""),
                description=(hit.get("description", "")[:200] + "..." 
                           if len(hit.get("description", "")) > 200 
                           else hit.get("description", "")),
                categories=hit.get("categories", []) or [],
                action_labels=hit.get("action_labels", []) or [],
                tags=hit.get("tags", []) or [],
                actions_count=hit.get("actions", 0),
                verified=hit.get("verified", False)
            )
            apps.append(app)
        
        return SingulAppSearchResult(
            query=query,
            total_hits=total_hits,
            apps=apps
        )
        
    except Exception as e:
        return SingulAppSearchResult(
            query=query,
            total_hits=0,
            apps=[],
            error=f"Search failed: {str(e)}"
        )
    
if __name__ == "__main__":
    mcp.run()
