from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="aws2-wrap2",
    version="2.0.1",
    description="A wrapper for executing a command with AWS CLI v2 and SSO",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bigwheel/aws2-wrap",
    author="Philip Colmer",
    author_email="k.bigwheel+eng@gmail.com",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent'
    ],
    license="GNU General Public License v3 (GPLv3)",
    keywords="aws profile sso assume role",
    packages=[
        "aws2wrap"
    ],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'aws2-wrap2 = aws2wrap:main',
        ]
    },
    python_requires=">=3.6",
)
