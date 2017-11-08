from setuptools import setup

setup(
    name="python-nrpc",
    version="0.0.1",
    packages=["nrpc"],
    entry_points={"console_scripts": [
        "protoc-gen-pynrpc=nrpc.gen:main",
    ]},
)
