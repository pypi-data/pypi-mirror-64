from setuptools import setup

setup(
    name='chimera_client',
    packages=['chimera_client'],
    description='Client for communication using chimera channels.',
    version='0.0.1',
    url="https://gitlab.inspr.com/chimera/client",
    install_requires=['requests', 'avro-python3', 'confluent_kafka']
)
