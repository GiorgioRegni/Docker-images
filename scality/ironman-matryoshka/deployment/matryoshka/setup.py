#from distutils.core import setup
from setuptools import setup
setup(
    name='matryoshka',
    version='1.0',
    scripts=['matryoshka/matryoshka.py'],
    install_requires=[
          'docker-py',
          'pyyaml',
    ],
    extras_require={
        'security': ['pyOpenSSL>=0.13', 'ndg-httpsclient', 'pyasn1'],
    },
)
