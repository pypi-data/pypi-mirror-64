import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfreewheel",
    version="0.1.0",
    author="Michael Meyer",
    author_email="me@entrez.cc",
    description="Communicate with the Freewheel inbound API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/entrez/pyfreewheel",
    packages=setuptools.find_packages(),
    keywords='api freewheel adtech',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    python_requires='>=3.5',
)
