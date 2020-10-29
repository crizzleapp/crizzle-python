import setuptools

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

dev_requirements = [
    "black",
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crizzle",
    version="0.1.0",
    author="Krishna Penukonda",
    url="https://github.com/crizzleapp/crizzle-python",
    description="Financial time-series analysis",
    long_description=long_description,
    packages=setuptools.find_packages(),
    license="MIT",
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={"dev": dev_requirements},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["crizzle=crizzle.__main__:main"]},
)
