import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ssr_rts_api",
    version="0.0.1",
    author="Renato Diaz (rouj)",
    author_email="renatojour@gmail.com",
    description="Connect with ease to the public rts/ssr public API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rerouj/ssr_rts_api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)