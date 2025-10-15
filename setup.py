# setup.py
from setuptools import setup, find_packages

setup(
    name="jhand-lang",
    version="0.1.0",
    author="Sadran",
    author_email="no-reply@jhand-lang.dev",
    description="JHAND Language – Galiyon mein likha, duniya mein chhaya 💥",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/asaad2691/jhand_lang",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: JHAND",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Compilers",
    ],
    license="MIT",
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "jhand=jhand.cli:main",
        ],
    },
    install_requires=[],
    zip_safe=False,
)
