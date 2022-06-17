from setuptools import setup, find_packages

setup(
    name='namu-wiki-extractor',
    version='0.2.3',
    description='A library to extract plaintexts from the namu wiki dump',
    url='https://github.com/hyeon0145/namu-wiki-extractor',
    author='Jonghwan Hyeon',
    author_email='hyeon0145@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Markup',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords='namu wiki plaintext extractor',
    packages=find_packages(),
    install_requires=[],
)
