from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

with open('README.md') as f:
    long_description = f.readline()

setup(
    name='gcmon',
    version='1.0.0',
    author='Ian Laird',
    author_email='irlaird@gmail.com',
    url='https://github.com/irlaird/gcmon',
    description='Monitor Google Cast events and publish them to the message broker.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gcmon = gcmon.entry:main'
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=requirements,
)
