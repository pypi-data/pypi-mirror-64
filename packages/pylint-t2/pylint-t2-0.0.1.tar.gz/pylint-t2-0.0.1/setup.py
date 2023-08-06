import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = ["pylint>=2.4", "pylint-plugin-utils>=0.6"]
dev_requires = [
    "black==19.10b0",
]

setuptools.setup(
    name="pylint-t2",
    version="0.0.1",
    author="Röstäm Gazizov",
    author_email="gazizov@tn.ru",
    license="MIT",
    description="Transport2 pylint plugin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rustemg/pylint-t2",
    packages=setuptools.find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="pylint plugin",
    python_requires=">=3.6",
    install_requires=install_requires,
    extras_require={"dev": dev_requires,},
)
