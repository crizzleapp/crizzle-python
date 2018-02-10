from distutils.core import setup

setup(
    name="crizzle",
    version="0.0.1",
    packages=["crizzle",],
    description="Python algorithmic trading for cryptocurrencies",
    long_description="A Python3 library for backtesting and trading cryptocurrencies",
    install_requires=["numpy",
                      "pandas",
                      "bokeh",
                      "requests"],
)