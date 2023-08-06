import setuptools

with open('README.md', 'r') as fh:
    readme = fh.read()

setuptools.setup(
    name='mysqlx_connector',
    version='0.0.8',
    author='Kalle Kankaanpää',
    author_email='kallekan11@gmail.com',
    description='Mysql connector skeleton for the x protocol',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/KnoxZZ/mysqlx_connector',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6'
)
