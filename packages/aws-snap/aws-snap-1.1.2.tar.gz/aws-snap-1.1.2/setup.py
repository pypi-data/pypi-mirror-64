import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aws-snap",
    version="1.1.2",
    author="Andy Klier",
    author_email="andyklier@gmail.com",
    description="CLI (simple command line client) for making snapshots of AWS EC2 instances",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/shindagger/aws-snap-python",
    packages = ['awssnap'],
    install_requires= ['setuptools', 'string-color>=0.2.7', 'boto3'],
    python_requires='>=3.6',
    entry_points = {
        'console_scripts': ['aws-snap=awssnap.main:main', 'snapit=awssnap.main:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
