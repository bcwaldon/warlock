import setuptools


def parse_requirements():
    fap = open('requirements.txt', 'r')
    raw_req = fap.read()
    fap.close()
    return raw_req.split('\n')
    return ['jsonschema']


setuptools.setup(
    name='warlock',
    version='0.5.0',
    description='Python object model built on top of JSON schema',
    author='Brian Waldon',
    author_email='bcwaldon@gmail.com',
    url='http://github.com/bcwaldon/warlock',
    packages=['warlock'],
    install_requires=parse_requirements(),
)
