import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ssr_rts_api",  # Replace with your own username
    version="0.0.2",
    author="Renato Diaz (rouj)",
    author_email="renatojour@gmail.com",
    description="Connect with ease to the public rts/ssr public API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rerouj/ssr_rts_api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)