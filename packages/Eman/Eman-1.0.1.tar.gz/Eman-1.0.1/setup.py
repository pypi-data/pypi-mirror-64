from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="Eman",
    version="1.0.1",
    description="A Python package to get weather reports for any location.",
    long_description=readme(),
    url="https://github.com/nikhilkumarsingh/weather-reporter",
    author="eman",
    author_email="eman.za1996@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Eman"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "weather-reporter=weather_reporter.cli:main",
        ]
    },
)