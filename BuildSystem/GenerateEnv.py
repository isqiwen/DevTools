import sys
from pathlib import Path

from BuildSystem.VenvHelper import get_executable_path
from BuildSystem.ProjectConfig import ProjectConfig
from Utilities.Logger import Logger

def generate_env_file():
    """
    Generate a .env file in the .vscode directory based on the current system.
    The .env file includes paths for clang-format, clang-tidy, and cmake etc.
    """
    # Define executable names and their default locations
    tools = [
        "clang-format",
        "clang-tidy",
        "cmake",
        "conan"
    ]

    # Initialize paths dictionary
    paths = {}

    # Search paths based on system
    for tool in tools:
        tool_path = get_executable_path(tool)
        if tool_path != None:
            paths[tool] = tool_path
        else:
            Logger.Warning(f"{tool} not found in .venv.")

    # Define the .vscode directory and .env file path
    workspace_dir = ProjectConfig.PROJECT_ROOT
    vscode_dir = workspace_dir / ".vscode"
    vscode_dir.mkdir(exist_ok=True)
    env_file_path = vscode_dir / ".env"

    # Write paths to the .env file
    with open(env_file_path, "w") as env_file:
        for tool, path in paths.items():
            tool = tool.replace("-", "_")
            env_file.write(f"{tool.upper()}_PATH={path}\n")

    Logger.Info(f".env file has been generated at: {env_file_path}")

if __name__ == "__main__":
    generate_env_file()
