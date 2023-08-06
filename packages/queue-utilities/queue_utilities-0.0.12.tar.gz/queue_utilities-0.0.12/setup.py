import setuptools  # type: ignore

setuptools.setup(
    name="queue_utilities",
    version="0.0.12",
    author="Jacob Richter",
    author_email="jaycorichter@gmail.com",
    description="A collection of helpful queue utilities. Pipes, timers, tickers, multiplexors, multicasters and queue select.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jaycosaur/queue-utilities",
    packages=setuptools.find_packages(),
    package_data={"queue_utilities": ["py.typed"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
