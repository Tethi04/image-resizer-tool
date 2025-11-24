from setuptools import setup, find_packages

setup(
    name="cute-image-resizer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "Pillow>=10.0.1",
        "Flask>=2.3.3",
        "Werkzeug>=2.3.7"
    ],
    python_requires=">=3.7",
)
