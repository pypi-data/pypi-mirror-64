from setuptools import setup, find_packages
from os import path
from aweme import VERSION


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()


setup(
    name='aweme',
    version=VERSION,
    url='https://github.com/maguowei/aweme',
    license='MIT',
    author='maguowei',
    author_email='imaguowei@gmail.com',
    keywords='Douyin CLI, Douyin API',
    description='Douyin Command Line Interface',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    platforms='any',
    python_requires='>=3.6',
    install_requires=[
        'requests==2.22.0',
        'fire==0.2.1',
    ],
    entry_points={
        'console_scripts': [
            'aweme=aweme.aweme:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)