from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="DXC_AI_Test",
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
    packages=["DXC_AI_Test"],
    include_package_data=True,
    install_requires=["json","pandas","doctest","requests","datetime","pymongo","auto_ml","sklearn","os","pickle",
                      "Algorithmia","shutil","urllib","flatten_json","janitor","ftfy","nltk","scrubadub","arrow",
                      "numpy","seaborn","math","datacleaner","JIRA","gitpython","pyjanitor","yellowbrick",
                      "missingno"],
    entry_points={
        "console_scripts": [
            "DXC-AI-Test=DXC_AI_Test.ai:main",
        ]
    },
)