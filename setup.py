from setuptools import setup, find_packages

setup(
    name="MyBassTabTranscriber",
    version="0.1.0",
    package_dir={"": "src"},  # Source directory
    packages=find_packages(where="src"),  # Automatically find packages in src/
    description="A library for transcribe tabs out of bass lines.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Matteo Galletti (mgalletti)",
    license="MIT",
    url="https://github.com/mgalletti/MyBassTabTranscriber",
    python_requires=">=3.9",  # supported Python versions
    install_requires=[
        # Add runtime dependencies here, e.g., "requests>=2.25.1"
    ],
)
