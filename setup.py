import setuptools


def parse_requirements():
    fap = open('requirements.txt', 'r')
    raw_req = fap.read()
    fap.close()
    return raw_req.split('\n')


setuptools.setup(
    name='warlock',
    version='0.7.0',
    description='Python object model built on JSON schema and JSON patch.',
    author='Brian Waldon',
    author_email='bcwaldon@gmail.com',
    url='http://github.com/bcwaldon/warlock',
    packages=['warlock'],
    install_requires=parse_requirements(),
)
