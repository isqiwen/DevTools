import sys
import argparse
import importlib
from pathlib import Path

dev_tools_package_location = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(dev_tools_package_location))


SUBCOMMANDS = {
    "setup-env": "BuildSystem.EnvSetup",
    "builder": "BuildSystem.Runner",
    "tree": "Utilities.PrintTree",
    "format": "Utilities.CodeFormat",
    "gitkeep": "Utilities.GitKeep"
}

def main():
    """
    Entry point for the project management script. Distributes subcommands to corresponding modules.
    """
    parser = argparse.ArgumentParser(description="Project management script")
    parser.add_argument(
        "-p, --show-project-info",
        dest = 'show_project_info',
        help = f"Display project info",
        default = False,
        action = 'store_true'
    )

    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Dynamically load and register subcommands
    try:
        for name, module_name in SUBCOMMANDS.items():
            module = importlib.import_module(module_name)
            if hasattr(module, "register_subcommand"):
                module.register_subcommand(subparsers)
            else:
                raise ImportError(f"Subcommand module {name} is missing `register_subcommand`.")
    except Exception as e:
        print(f"Failed to load subcommand {name}: {e}\n")

    # Parse arguments and dispatch to the correct function
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    # elif args.show_project_info:
    #     ProjectConfig.summary()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
