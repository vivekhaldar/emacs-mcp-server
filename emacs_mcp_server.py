# /// script
# dependencies = [
#   "mcp[cli]",
#   "smartfunc",
# ]
# ///

from smartfunc import backend
from mcp.server.fastmcp import FastMCP
import subprocess
import logging
import functools
import os


# Convenience routine for logging function invocations.
# logging.basicConfig(level=logging.INFO, filename="emacs_mcp_server.log", filemode="a")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logger.info(f"{func.__name__} returned: {result}")
        return result

    return wrapper

# Assumes that you have set the environment variable OPENAI_API_KEY.
llmify = backend("gpt-4o", system="You are an expert at Emacs Lisp.", temperature=0.5)

# Create an MCP server
mcp = FastMCP("Emacs-MCP-Server")


@log_execution
@llmify
def generate_emacs_lisp_code_from_llm(purpose: str):
    """Generate Emacs Lisp code for the following purpose: {{ purpose }}.

    Make sure to include a docstring in the code, and insert explanatory comments.

    MAKE SURE TO ONLY RETURN THE CODE, DO NOT RETURN ANY EXPLANATION OR ADDITIONAL TEXT.

    DO NOT WRAP THE CODE IN MARKDOWN CODE BLOCKS.
    """
    pass


@log_execution
@mcp.tool()
def generate_emacs_lisp_code(purpose: str) -> str:
    """Generate Emacs Lisp code for the given purpose."""
    return generate_emacs_lisp_code_from_llm(purpose)


@log_execution
@mcp.tool()
def execute_emacs_lisp_code(code: str) -> str:
    """Execute Emacs Lisp code by sending it to the Emacs process and return the result."""
    try:
        # Properly escape the Emacs Lisp code and pass it to emacsclient
        # The -e or --eval flag is used to evaluate the expression
        emacsclient_path = os.environ.get("EMACSCLIENT", "emacsclient")
        result = subprocess.check_output(
            [emacsclient_path, "--eval", code], text=True, stderr=subprocess.PIPE
        ).strip()
        return result
    except subprocess.CalledProcessError as e:
        return f"Error executing Emacs Lisp code: {e.stderr}"
