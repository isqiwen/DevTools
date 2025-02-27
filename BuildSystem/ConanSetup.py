from Utilities.Logger import Logger

from BuildSystem.ConanHelper import install_conan, configure_conan
from BuildSystem.VenvHelper import check_pipenv


def conan_setup():
    Logger.Info("Conan setup begin!")

    # Check for required tools
    check_pipenv()

    # Install Conan
    install_conan()

    # Configure Conan
    configure_conan()

    Logger.Info("Conan setup end!")


if __name__ == "__main__":
    conan_setup()
