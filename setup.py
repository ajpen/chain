import setuptools

setuptools.setup(
    name="chain-py",
    version="0.1.7",
    url="https://github.com/ajpen/chain",

    author="Anfernee Jervis",
    author_email="anferneejervis@gmail.com",

    description="An expressive clean way to interact with RESTful APIs.",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=['requests'],
    tests_require=['responses'],
    test_suite='tests',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
