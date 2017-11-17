from setuptools import setup
import distutils.cmd
import subprocess


class protoc(distutils.cmd.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.check_call([
            "protoc",
            "--proto_path", ".",
            "--proto_path", "nrpc",
            "--python_out", ".",
            "nrpc/nrpc.proto",
        ])


setup(
    name="python-nrpc",
    version="0.0.1",
    packages=["nrpc"],
    cmdclass={'protoc': protoc},
    entry_points={"console_scripts": [
        "protoc-gen-pynrpc=nrpc.gen:main",
    ]},
)
