from setuptools import setup, find_packages

setup(
    name="gerrit-sync",
    version=0.1,
    description="a command line tool to easily"
                "clone gerrit repositories in bulk.",
    keywords="repository gerrit git clone sync",
    author="Fırat Civaner",
    author_email="fcivaner@gmail.com",
    license="MIT License",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ["gerrit-sync=gerrit_sync.__main__:main"],
    },
    install_requires=[
        "pygerrit2",
        "requests"
    ]
)
