from setuptools import setup, find_packages

setup(
    name='nuyidao',
    version='0.0.2',
    description='Astro support',
    url='https://gitlab.com/jorjun/nuyidao',
    license='MIT',
    packages=['nuyidao'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
    ],
    install_requires="ephem==3.7.6.0",
    python_requires='>3.7',
)
