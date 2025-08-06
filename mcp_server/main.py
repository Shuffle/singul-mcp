import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from shufflepy import Singul

# Load configuration from environment variables
api_key = os.environ.get("SHUFFLE_API_KEY")
shuffle_url = os.environ.get("SHUFFLE_URL", "https://shuffler.io")

if not api_key:
    raise ValueError("SHUFFLE_API_KEY environment variable not set.")

# Instantiate the Singul client
singul = Singul(api_key, url=shuffle_url)

# Define the request body model
class ConnectRequest(BaseModel):
    app: str
    action: str
    fields: List[Dict[str, Any]]
    environment: Optional[str] = None

app = FastAPI()

@app.post("/connect")
async def connect(request: ConnectRequest):
    """
    Connect to an app and perform an action.
    """
    try:
        # Prepare the arguments for the singul.connect method
        connect_args = {
            "app": request.app,
            "action": request.action,
            "fields": request.fields,
        }
        if request.environment:
            connect_args["environment"] = request.environment

        # Call the singul.connect method
        result = singul.connect(**connect_args)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
