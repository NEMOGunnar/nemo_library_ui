from setuptools import setup, find_packages

setup(
    name="nemo_library_ui",
    version="0.1.0",
    author="Gunnar Schug",
    author_email="gunnar.schug@nemo-ai.com",
    description="UI for the NEMO Python library",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NEMOGunnar/nemo_library_ui",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "jinja2",
        "nemo_library",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: FastAPI",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13",
    entry_points={
        "console_scripts": [
            "nemo-library-ui = nemo_library_ui.ui:main"
        ]
    }
)