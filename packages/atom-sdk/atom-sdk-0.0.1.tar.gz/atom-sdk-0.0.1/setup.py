from setuptools import setup, find_packages

setup(
    name="atom-sdk",
    version="0.0.1",
    description="Atom Python SDK",
    url="https://pypi.org/project/atom-sdk",
    maintainer="Supremind Atom",
    maintainer_email="atom@supremind.com",
    packages=['atom', 'atom.github.com.envoyproxy.protoc_gen_validate.validate'],
    install_requires=[
        "grpcio"
    ],
)
