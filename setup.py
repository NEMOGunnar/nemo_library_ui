from setuptools import setup, find_packages

setup(
    name="nemo_library_ui",
    version="0.1.0",
    description="UI for the nemo_library based on FastAPI",
    author="Gunnar Schug",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "jinja2",
        "nemo-library"
    ],
    entry_points={
        "console_scripts": [
            "nemo-ui = ui:start_ui"
        ]
    },
    python_requires=">=3.13",
)