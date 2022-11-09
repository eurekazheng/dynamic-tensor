from setuptools import setup, find_packages
from pathlib import Path


setup(
    name="dynamic-tensor",                  # This is the name of the package
    version="0.0.2",                        # The release version
    author="Shaoming Zheng",                # Full name of the author
    author_email='zhengeureka@gmail.com',
    maintainer="Shaoming Zheng",  # Full name of the author
    maintainer_email='zhengeureka@gmail.com',
    license='MIT',
    url='https://github.com/eurekazheng/dynamic-tensor',
    description="Automatically and minimally expanding tensor for __setitem()__ operations based on NumPy.",
    long_description=Path("README.md").read_text(encoding="utf-8"),      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    keywords=['tensor', 'numpy', 'array'],
    platforms="any",
    packages=find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["densor"],          # Name of the python package
    package_dir={'': 'src'},     # Directory of the source code of the package
    install_requires=['numpy>=1.16'],              # Install other dependencies if any
    extras_require={}
)
