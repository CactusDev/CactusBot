from distutils.core import setup

if __name__ == "__main__":
    with open("README.md") as file:
        description = file.read()

    setup(
        name="CactusBot",
        version="v0.4-dev",
        packages=["cactusbot"],
        license="MIT",
        long_description=description
    )
