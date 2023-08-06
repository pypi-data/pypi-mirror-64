import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nextstep",
    version="0.0.6",
    author="Yang Yuesong",
    author_email="yangyuesongyys@gmail.com",
    description="USEP price prediction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YangYuesong0323/nextstep",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires = [
        'dataflows == 0.0.71',
        'wwo-hist == 0.0.4',
        'tenserflow == 2.1.0',
        'statsmodels == 0.11.0'
        ]
)
