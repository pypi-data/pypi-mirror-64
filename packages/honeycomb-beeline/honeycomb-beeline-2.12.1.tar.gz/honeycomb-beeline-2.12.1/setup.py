from setuptools import setup, find_packages

setup(
    python_requires='>=2.7',
    name='honeycomb-beeline',
    version='2.12.1',
    description='Honeycomb library for easy instrumentation',
    url='https://github.com/honeycombio/beeline-python',
    author='Honeycomb.io',
    author_email='feedback@honeycomb.io',
    license='Apache',
    packages=find_packages(),
    install_requires=[
        'libhoney>=1.7.0',
        'wrapt',
    ],
    tests_require=[
   	    'Jinja2',
        'mock',
        'flask',
        'tornado==5',
        'django<2; python_version == "2.7"',
        'django>=2; python_version >= "3.0"',
    ],
    test_suite='beeline.test_suite.get_test_suite',
    zip_safe=False
)
