import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CodeProfiler", # Replace with your own username
    version="1.0.0.1.2",
    author="Shreyas",
    author_email="shreyasajitrajendran@gmail.com",
    description="Print memory and cpu usage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/connosieurofdoom/profiler",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)