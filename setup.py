import setuptools
import subprocess

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


class protoc(setuptools.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.check_call(
            [
                "protoc",
                "--proto_path",
                ".",
                "--proto_path",
                "nrpc",
                "--python_out",
                ".",
                "nrpc/nrpc.proto",
            ]
        )


setup(
    name="python-nrpc",
    version="0.0.6",
    description="A python code generator and lib for Nats RPC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["nrpc"],
    package_data={"nrpc": ["*.mako"]},
    cmdclass={"protoc": protoc},
    entry_points={"console_scripts": ["protoc-gen-pynrpc=nrpc.gen:main"]},
    install_requires=["protobuf", "mako", "nats-py>=2.7"],
)
