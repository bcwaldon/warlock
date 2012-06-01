import setuptools


setuptools.setup(
    name='warlock',
    version='0.0.1',
    description='Python object model built on top of JSON schema',
    author='Brian Waldon',
    author_email='bcwaldon@gmail.com',
    url='http://github.com/bcwaldon/warlock',
    packages=['warlock'],
    install_requires=['jsonschema'],
)
