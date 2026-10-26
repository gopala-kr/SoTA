# tool_server.py — exposing the client's test runner to the agent as a tool over
# the Model Context Protocol (sketch using the MCP Python SDK's FastMCP helper;
# check names against the SDK version you install).
from mcp.server.fastmcp import FastMCP
from sandbox import run_in_sandbox            # micro-VM runner (Part 13)

mcp = FastMCP("maestro-repo-tools")

@mcp.tool()
def run_tests(path: str = "tests/", timeout_s: int = 300) -> str:
    """Run the repository's test suite inside the task sandbox and return a summary."""
    res = run_in_sandbox(["pytest", "-q", path], timeout=timeout_s, network=False)
    return res.summary(max_chars=4000)

@mcp.tool()
def open_pull_request(title: str, body: str) -> str:
    """Propose the current patch as a pull request. Requires human confirmation (Part 13)."""
    return request_confirmation("open_pull_request", title=title, body=body)

if __name__ == "__main__":
    mcp.run()
