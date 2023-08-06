import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ajenti.plugin.cpu_temp", # Replace with your own username
    version="0.0.4",
    author="Tifer King",
    author_email="tiferking@tiferking.cn",
    description="A CPU temperature monitor plugin with chart for Ajenti dashboard.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.tiferking.cn",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)