from setuptools import find_packages, setup

setup(
    name='richtypo',
    version='0.1',
    description="The only web typograph that don't make a mess out of your text. Russian and English supported.",
    keywords=['typography', 'spaces', 'nbsp', 'russian', 'markdown', ],
    url="https://github.com/f213/richtypo.py",
    classifiers=[
        'Topic :: Text Processing :: Filters',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    author="Fedor Borshev",
    author_email="f@f213.in",
    license="MIT",
    packages=find_packages(),
    setup_requires=['setuptools-git'],
    install_requires=[
        'six',
        'PyYAML',
        'backports.functools-lru-cache',
    ],
    include_package_data=True,
    zip_safe=False,
)
