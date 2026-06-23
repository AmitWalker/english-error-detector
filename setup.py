"""
Setup configuration for English Error Detector
"""

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="english-error-detector",
    version="1.0.0",
    author="AmitWalker",
    author_email="your.email@example.com",
    description="A professional English error detection desktop application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AmitWalker/english-error-detector",
    py_modules=["error_detector"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "error-detector=error_detector:main",
        ],
    },
)
