from setuptools import find_packages, setup

install_requires = [
    "google-api-python-client>=1.8.0",
    "google-cloud-logging>=1.15.0",
    "Click>=7.0",
    "click-completion>=0.5.2",
    "termcolor>=1.1.0",
    "grpcio>=1.27.2",
    "dateparser>=0.7.4",
    "Jinja2>=2.11.1",
]


setup(
    name="gcplogs",
    version="0.0.3",
    url="https://github.com/zeyaddeeb/gcplogs",
    license="MIT",
    author="Zeyad Deeb",
    author_email="zeyad.deeb@icloud.com",
    description="gcplogs is a simple command line tool to read GCP Stackdriver logs.",
    long_description="gcplogs is a simple command line tool to read GCP Stackdriver logs.",
    keywords="gcp logs",
    packages=find_packages(),
    platforms="any",
    install_requires=install_requires,
    test_suite="tests",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    entry_points={"console_scripts": ["gcplogs = gcplogs.bin:cli"]},
    zip_safe=False,
)
