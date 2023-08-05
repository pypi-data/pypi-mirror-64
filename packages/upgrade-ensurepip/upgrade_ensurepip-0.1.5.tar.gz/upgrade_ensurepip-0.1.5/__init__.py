# coding: utf-8

_package_data = dict(
    full_package_name='upgrade_ensurepip',
    version_info=(0, 1, 5),
    __version__='0.1.5',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='upgrade pip and setuptools versions used by venv',
    keywords='pip ensurepip upgrade',
    license='MIT',
    since=2018,
    python_requires='>=3.3',
    status=u'α',
    universal=True,
    install_requires=[],
    classifiers=[
            'Environment :: Console',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3 :: Only',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: Quality Assurance',
    ],
    oitnb=dict(
        multi_line_unwrap=True,
    ),
    print_allowed=True,
)


version_info = _package_data["version_info"]
__version__ = _package_data["__version__"]
