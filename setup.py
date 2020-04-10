import distutils.cmd
import subprocess

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


class protoc(distutils.cmd.Command):
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
    version="0.0.2",
    description="A python code generator and lib for Nats RPC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["nrpc"],
    cmdclass={"protoc": protoc},
    entry_points={"console_scripts": ["protoc-gen-pynrpc=nrpc.gen:main"]},
    install_requires=["protobuf", "mako", "asyncio-nats-client"],
)
