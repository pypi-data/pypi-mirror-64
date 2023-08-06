import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlinnate",
    version="1.1.3",
    author="Frederic Magniette",
    author_email="magniette@llr.in2p3.fr",
    description="Innate stands for Integrated Neural Network Automatic Trainer and Evaluator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://llrgit.in2p3.fr/online/innate",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'dill',
        'rpyc',
        'IPython',
        'h5py',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
