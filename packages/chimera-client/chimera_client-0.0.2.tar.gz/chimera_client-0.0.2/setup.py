from setuptools import setup
from os import path


# read the contents of the README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='chimera_client',
    packages=['chimera_client'],
    description='Client for communication using chimera channels.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.0.2',
    url="https://gitlab.inspr.com/chimera/client",
    install_requires=['requests', 'avro-python3', 'confluent_kafka']
)
