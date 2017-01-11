from setuptools import setup, find_packages

setup(
    name='richtypo',
    version='0.1',
    description="The only web-typograf thet doesn't make your text a mess. Russian and Eglish supported.",
    url="https://github.com/f213/richtypo.py",
    author="Fedor Borshev",
    author_email="f@f213.in",
    license="MIT",
    packages=find_packages(),
    setup_requires=['setuptools-git'],
    install_requires=[
        'six',
        'PyYAML',
    ],
    include_package_data=True,
    zip_safe=False,
)
