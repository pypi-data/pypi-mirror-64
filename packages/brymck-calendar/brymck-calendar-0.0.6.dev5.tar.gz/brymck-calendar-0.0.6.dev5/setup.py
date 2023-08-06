from setuptools import find_packages, setup

setup(
    name='brymck-calendar',
    version='0.0.6.dev5',
    author='Bryan Lee McKelvey',
    author_email='bryan.mckelvey@gmail.com',
    url='https://github.com/brymck/proto',
    description='',
    long_description='',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'grpcio>=1.0,<2.0',
        'grpcio-tools>=1.0,<2.0',
        'protobuf>=3.0,<4.0',
        'brymck-dates',
    ],
)