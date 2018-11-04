from distutils.core import setup

setup(
    name="crizzle",
    version="0.0.1",
    packages=["crizzle", ],
    description="Python library for algorithmic trading on cryptocurrency exchanges",
    install_requires=[
        'numpy',
        'pandas',
        'bokeh',
        'requests',
        'backoff',
        'nose', 'ratelimit', 'scipy', 'opencv-python', 'networkx'
    ],
    author="Krishna Penukonda"
)
