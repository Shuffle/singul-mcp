# MCP Server

This server provides a simple interface to the `shufflepy` library, allowing you to connect to various services and perform actions with a single API call.

## Setup

1.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Set environment variables:**

    Before running the server, you need to set the following environment variables:

    *   `SHUFFLE_API_KEY`: Your Shuffle API key.
    *   `SHUFFLE_URL`: The URL of the Shuffle instance you want to connect to (e.g., `https://shuffler.io`).

    You can set them in your shell like this:

    ```bash
    export SHUFFLE_API_KEY="your_api_key"
    export SHUFFLE_URL="https://shuffler.io"
    ```

## Running the server

To run the server, use the following command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The server will be available at `http://localhost:8000`.

## API

The server exposes a single endpoint: `POST /connect`.

### Request

The request body should be a JSON object with the following fields:

*   `app` (string, required): The name of the app to connect to (eg., `slack`, `jira`).
*   `action` (string, required): The action to perform (e.g., `list_messages`, `create_ticket`).
*   `fields` (list of objects, required): A list of key-value pairs for the action. Each object in the list should have a `key` and a `value` field.
*   `environment` (string, optional): The name of the environment to run the execution in.

**Example request:**

```json
{
  "app": "slack",
  "action": "list_messages",
  "fields": [
    {
      "key": "channel",
      "value": "C12345678"
    }
  ]
}
```

### Response

The response will be the JSON output from the `shufflepy` library.
