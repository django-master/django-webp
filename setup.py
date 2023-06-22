import setuptools


with open('README.rst') as file:
    long_description = file.read()


setuptools.setup(
    name='django-webp',
    version='2.0.1',
    author=u'Andre Farzat',
    author_email='andrefarzat@gmail.com',
    packages=setuptools.find_packages(),
    url='http://pypi.python.org/pypi/django-webp/',
    license='MIT',
    description='Returns a webp image instead of jpg, gif or png to browsers',
    long_description=long_description,
    install_requires=open('requirements.txt').readlines(),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.5',
)
