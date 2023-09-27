import setuptools

with open("requirements.txt") as f:
    reqs = f.read().splitlines()

setuptools.setup(
    name="cryptography_pmf",
    version="0.1",
    description="University Cryptography course package",
    author="Nadir Bašić",
    install_requires=reqs,
    author_email="basicnadir@gmail.com",
    packages=setuptools.find_packages(),
    zip_safe=False,
)
