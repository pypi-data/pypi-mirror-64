from setuptools import setup
from setuptools import find_packages
import os

setup(
    name='PcnnLib',
    packages=find_packages(),
    version=os.environ['CI_COMMIT_TAG'],
    license='MIT',
    description='Pulse-coupled neural network library',
    author='Anton Zotov',
    author_email='anton@zotov.online',
    url='https://gitlab.com/trikster/pcnnlib',
    download_url='https://gitlab.com/trikster/pcnnlib',
    keywords=['pcnn', 'pulse', 'neural', 'impulse'],
    install_requires=[
        'pillow',
        'numpy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8'
    ],
)
