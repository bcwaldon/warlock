# Copyright 2012 Brian Waldon
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools
import io
import os


def parse_requirements():
    fap = io.open("requirements.txt", "r", encoding="utf-8")
    raw_req = fap.read()
    fap.close()
    return raw_req.split("\n")


def read(fname):
    with io.open(
        os.path.join(os.path.dirname(__file__), fname), "r", encoding="utf-8"
    ) as fp:
        return fp.read()


setuptools.setup(
    name="warlock",
    version="1.3.3",
    description="Python object model built on JSON schema and JSON patch.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    keywords=["JSON schema", "JSON patch", "model validation"],
    author="Brian Waldon",
    author_email="bcwaldon@gmail.com",
    maintainer="Jan Willhaus",
    maintainer_email="mail@janwillhaus.de",
    url="http://github.com/bcwaldon/warlock",
    packages=["warlock"],
    install_requires=parse_requirements(),
    license="Apache-2.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
