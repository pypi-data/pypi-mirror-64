import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kodiksnlp",
    version="0.0.7",
    author="Yavuz Kömeçoğlu",
    author_email="yavuz.komecoglu@kodiks.com",
    description="Kodiks Turkish NLP Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/kodiks-ai/kodiksnlp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=["requests>=2.21.0"]
)
