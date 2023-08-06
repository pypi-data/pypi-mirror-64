from setuptools import setup, find_packages

MAIN_NAME = "clickstock"

if __name__ == '__main__':
    setup(
        name=MAIN_NAME,
        description="I am clickstock",
        version="1.0.1",
        author="Mathieu Cesbron",
        author_email="mathieuces@gmail.com",
        url="https://github.com/MathieuCesbron?tab=repositories",
        packages=find_packages(),
        entry_points={
            "console_scripts":
            ["{0} = {1}.__main__:main".format(MAIN_NAME, MAIN_NAME)],
        },

    )
