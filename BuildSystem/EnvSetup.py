import os
import sys
import argparse
from pathlib import Path

from Utilities.Logger import Logger
from BuildSystem.ConanSetup import conan_setup
from BuildSystem.GenerateEnv import generate_env_file
from BuildSystem.ProjectConfig import ProjectConfig
from BuildSystem.VenvHelper import (
    get_python_info,
    get_pipenv_venv,
    delete_virtualenv,
    create_virtualenv,
    EnvironmentSetupError,
    get_virtualenv_python_info
)


def setup_python_env(env_root, pypi_source="https://pypi.tuna.tsinghua.edu.cn/simple"):
    """
    Setup the python development environment.
    """
    # Set script path and target root
    env_root = Path(env_root).resolve()

    Logger.Info(f"Setting up the python environment in {env_root}, using PyPI source {pypi_source}")

    # Backup the current working directory
    work_dir_backup = os.getcwd()

    if not env_root.is_dir():
        raise EnvironmentSetupError(f"Python environment root {env_root} does not exist or is not a directory.")

    os.chdir(env_root)

    Logger.Info("########################################################################################")
    Logger.Info(f"# ENV_ROOT             = {env_root}")
    Logger.Info(f"# PYPI_SOURCE          = {pypi_source}")
    Logger.Info("########################################################################################")

    Logger.Info("Starting initializing python virtual environment...")

    try:
        # Check Python version
        python_version, _ = get_python_info()
        venv_exist, venv_path = get_pipenv_venv()

        if venv_exist:
            Logger.Info(f"Python virtual environment already exists in {venv_path}.")
            user_input = input("Do you want to delete the existing virtual environment? (y/n): ").strip().lower()
            if user_input == "y":
                delete_virtualenv(env_root)
                create_virtualenv(python_version, pypi_source)
            else:
                Logger.Info("Using the existing virtual environment.")
        else:
            create_virtualenv(python_version, pypi_source)

        if get_virtualenv_python_info(venv_path) == None:
            Logger.Error(f"Cannot detect python in {venv_path}.")
    except EnvironmentSetupError as e:
        Logger.Error(f"Environment setup error: {e}")
        sys.exit(2)  # Exit with a specific status code for setup errors
    except Exception as e:
        Logger.Error("Failed initializing python virtual environment.")
        Logger.Error(f"Error: {e}")
        sys.exit(1)
    finally:
        os.chdir(work_dir_backup)
        Logger.Info("Finished initializing python virtual environment.")

def setup_env(env_root, pypi_source):
    Logger.Info("Setup the development environment.")
    setup_python_env(env_root, pypi_source)
    conan_setup()
    generate_env_file()

def _create_parser(parent_parser = None):
    description="Setup the development environment."
    if parent_parser is None:
        parser = argparse.ArgumentParser(description=description)
    else:
        parser = parent_parser.add_parser("setup-env", help=description, description=description)

    parser.add_argument(
        "config_filepath",
        type=str,
        help="The project config filepath."
    )
    parser.add_argument(
        "--pypi-source",
        type=str,
        default="https://pypi.tuna.tsinghua.edu.cn/simple",
        help="PyPI source for package installation (default: TUNA mirror)."
    )

    return parser

def setup_env_adapter(config_filepath, pypi_source):
    ProjectConfig.initialize(config_filepath)
    setup_env(ProjectConfig.PROJECT_ROOT, pypi_source)

def register_subcommand(parent_parser):
    """
    Add 'setup-env' subcommand to the parser.
    """
    parser = _create_parser(parent_parser)

    parser.set_defaults(func=lambda args: setup_env_adapter(args.config_filepath, args.pypi_source))

def main():
    parser = _create_parser()
    args = parser.parse_args()

    setup_env_adapter(args.config_filepath, args.pypi_source)

if __name__ == "__main__":
    main()
