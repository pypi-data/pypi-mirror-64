from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="DXC_AI_Test_3",
    version="1.0.0",
    description="A Python package to add two numbers.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    #url="",
    author="DXC",
    author_email="pulagamnkr@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["DXC_AI_Test_3"],
    include_package_data=True,
    install_requires=["JIRA","auto_ml","Algorithmia","gitpython","flatten_json","pyjanitor","ftfy","arrow",
                      "scrubadub","yellowbrick","datacleaner","missingno"],
    entry_points={
        "console_scripts": [
            "DXC-AI-Test3=DXC_AI_Test_3.ai:main",
        ]
    },
)