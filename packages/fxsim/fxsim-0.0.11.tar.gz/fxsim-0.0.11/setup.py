"""
@author: Alejandro Cuartas
"""

from setuptools import setup

setup(
    name="fxsim",
    version="0.0.11",
    description="Simulador de operacion en mercado forex",
    author="Alejandro Cuartas",
    author_email="alejandro.cuartas@yahoo.com",
    url="http://www.alejandrocuartas.com/",
    packages=["fxsim"],
    license="MIT",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    entry_points={
        "console_scripts": ["fxsim=fxsim.simulator:imp"]
    },
)