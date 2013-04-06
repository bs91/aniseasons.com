from setuptools import setup

setup(
    name='aniseasons',
    version='0.1',
    long_description=__doc__,
    packages=['aniseasons'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-pymongo',
        'flask-script',
        'PIL'
    ]
)
