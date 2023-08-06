from setuptools import setup, find_packages

setup(
    name='nuyidao',
    version='v0.0.3',
    description='Astro support',
    long_description="NU YI DAO utils support + SVG",
    url='https://nuyidao.com',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
    ],
    install_requires="ephem==3.7.6.0",
    python_requires='>3.7',
)
