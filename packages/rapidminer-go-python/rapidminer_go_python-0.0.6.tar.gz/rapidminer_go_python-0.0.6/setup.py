import setuptools

readme = ''
with open("README.md", "r") as fh:
    long_description = fh.read()
    
required_install = []
with open("requirements.txt", "r") as fh_req:
    required_install = fh_req.read().splitlines()

setuptools.setup(
    name="rapidminer_go_python", # Replace with your own username
    version="0.0.6",
    author="RapidMiner-Labs",
    author_email="bpatil@rapidminer.com",
    description="A python package to interact with RapidMiner GO Engine",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/rapidminer-labs/python-go",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires= required_install,
    python_requires='>=3.6',
)