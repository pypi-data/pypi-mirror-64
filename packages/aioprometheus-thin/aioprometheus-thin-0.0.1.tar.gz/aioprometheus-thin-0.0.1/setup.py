import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aioprometheus-thin",  # Replace with your own username
    version="0.0.1",
    author="Raz Co.",
    author_email="razchn@gmail.com",
    description="Python asyncIO Prometheus package - using aioprometheus, but simpler !",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RazcoDev/aioprometheus-thin",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'aioprometheus',
        'asyncio',
    ],
    python_requires='>=3.6',
)
