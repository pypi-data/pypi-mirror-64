from setuptools import setup,find_packages
with open("README.md","r") as fh:
    long_description = fh.read()
setup(
    name="GoogleVerify",
    version=1.2,
    description="Main.py in start program.",
    author="Zhang Boxuan",
    author_email="capture1969@hotmail.com",
    maintainer="Zhang Boxuan",
    maintainer_email="capture1969@hotmail.com",
    url="https://github.com/PoisonCap159753",
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    license="MIT license",
    platforms=["any"],
    install_requires=["PyQt5", "pyotp","qrcode"]
)