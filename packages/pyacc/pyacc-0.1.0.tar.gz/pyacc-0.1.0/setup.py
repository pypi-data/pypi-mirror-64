from setuptools import setup, find_packages


setup(
    name='pyacc',
    version='0.1.0',
    author='Robert Forkel',
    author_email='forkel@shh.mpg.de',
    description='Python library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='',
    license='Apache 2.0',
    url='https://github.com/atlas-comp-cog/pyacc',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'acc=pyacc.__main__:main',
        ],
    },
    platforms='any',
    python_requires='>=3.5',
    install_requires=[
        'csvw>=1.5.6',
        'clldutils>=3.5',
        'openpyxl',
        'attrs',
        'nameparser',
    ],
    extras_require={
        'dev': ['flake8', 'wheel', 'twine'],
        'test': [
            'mock',
            'pytest>=3.6',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
