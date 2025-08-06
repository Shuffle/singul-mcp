#!/usr/bin/env python3

import os
import sys
from typing import List, Optional, Dict, Any
from mcp.server.fastmcp import FastMCP

sys.stderr = open(os.devnull, 'w')

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
def shuffle_connect(
    app: str,
    action: str, 
    fields: List[Dict[str, Any]],
    environment: Optional[str] = None
) -> Dict[str, Any]:
    """
    Connect to a Shuffle app and perform an action.
    
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
def list_shuffle_apps() -> Dict[str, Any]:
    """
    List available Shuffle apps that can be connected to.
    
    Returns:
        Information about available apps
    """
    
    # i need to connect this with algolia    
    return {
        "message": "Use shuffle_connect with app names like 'slack', 'jira', 'github', etc.",
        "example_apps": ["slack", "jira", "github", "email", "webhook"],
        "shuffle_client_status": "initialized" if singul else "not initialized"
    }
