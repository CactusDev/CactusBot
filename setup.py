from distutils.core import setup

if __name__ == "__main__":
    with open("README.md", encoding="utf-8") as file:
        description = file.read()

    setup(
        name="CactusBot",
        version="v0.4-dev",
        packages=["cactusbot"],
        license="MIT",
        long_description=description
    )
