from setuptools import setup, find_packages

setup(
    name="drive-thru-ai",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "streamlit",
    ],
    python_requires=">=3.10",
    author="Jake Silver",
    description="A drive-thru AI ordering system",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
)
