from setuptools import setup
def readme():
    with open ("README.MD") as f:
        README = f.read()
    return README

setup(
    name='Bitcoin_Price',
    version='0.3',
    description='A package for bitcoin price notification in telegram',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='Abhishek Asarawa',
    author_email='aasarawa@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    packages=['BitcoinPrice'],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={"console_scripts": ['Bitcoin_Price=BitcoinPrice.Bitcoin_Price:main']
    },

)