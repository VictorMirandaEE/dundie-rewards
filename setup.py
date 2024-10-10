from setuptools import setup, find_packages


setup(
    name="dundie",
    version="0.1.0",
    description="Dunder Mifflin Rewards System",
    author="Victor Miranda",
    url="https://github.com/VictorMirandaEE/dundie-rewards",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "dundie = dundie.__main__:main"
        ]
    },
)
