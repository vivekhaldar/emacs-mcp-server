# Emacs MCP Server

Model Context Protocol (MCP) server for Emacs. Enables generating and running elisp code in a running Emacs process.

## Tools

The server exposes two tools:
- `generate_emacs_lisp_code`: generates elisp for a given task
- `execute_emacs_lisp_code`: passes elisp to a running Emacs (via `emacsclient`) to eval and execute it.

## Invocation

The project is managed with `uv`. First, run `uv sync` to install all dependencies. Then `source .venv/bin/activate` to activate the resulting venv.

To run the MCP server in the inspector:

```sh
mcp dev emacs_mcp_server.py
```

To install the MCP server so that Claude Desktop can use it:

```sh
mcp install emacs_mcp_server.py
```

But you will have to edit the resulting JSON config in `claude_desktop_config.json` to include API keys and the full path to `emacsclient`. It should look something like this:

```json
    "Emacs-MCP-Server": {
      "command": "/Users/haldar/.local/bin/uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "--with",
        "smartfunc",
        "mcp",
        "run",
        "/Users/haldar/repos/gh/emacs-mcp-server/emacs_mcp_server.py"
      ],
      "env": {
          "OPENAI_API_KEY": "sk-xxxx",
          "EMACSCLIENT": "/your/path/to/emacsclient"
      }
    }
```