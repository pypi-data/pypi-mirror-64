from setuptools import find_packages, setup

install_requires = ["requests>=2.18.4", "click", "click-default-group"]

docs_require = ["sphinx>=1.4.0"]

tests_require = [
    "coverage[toml]==5.0.3",
    "requests-mock==1.3.0",
    "pytest-cov>=2.2.0",
    "pytest>=2.8.3",
    "pytest-click",
    # Linting
    "isort[pyproject]==4.3.21",
    "flake8==3.0.3",
    "flake8-blind-except==0.1.1",
    "flake8-debugger==1.4.0",
    "flake8-imports",
]

setup(
    name="folge-cli",
    version="0.1.0",
    description="Client for the folge project",
    long_description=open("README.rst", "r").read(),
    url="https://github.com/labd/folge-cli",
    author="Lab Digital",
    author_email="opensource@labdigital.nl",
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={"docs": docs_require, "test": tests_require},
    use_scm_version=True,
    entry_points={"console_scripts": ["folge-cli=folge_cli.cmd:main",],},
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    zip_safe=False,
)
