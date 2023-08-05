from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip
from setuptools import setup, find_packages


pipfile = Project(chdir=False).parsed_pipfile
requirements = convert_deps_to_pip(pipfile['packages'], r=False)
test_requirements = convert_deps_to_pip(pipfile['dev-packages'], r=False)

name = pipfile['source'][0]['name']
version = pipfile['source'][0]['version']
python_version = pipfile['requires']['python_version']

with open('README.rst') as fl:
    readme = fl.read()


setup(
    name=name,
    version=version,
    description='Create beautiful QR-codes with perfectly fitting logos!',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['qrpic = qrpic.main:run'],
    },
    platforms='any',
    install_requires=requirements,
    setup_requires=test_requirements,
    python_requires=f'>={python_version}',
    license='MIT',

    author='Mischa Krueger',
    author_email='makmanx64@gmail.com',
    long_description=readme,
    long_description_content_type='text/x-rst',
    keywords='qr-code logo imaging',
    url='https://gitlab.com/Makman2/qrpic',
    project_urls={
        'Bug Tracker': 'https://gitlab.com/Makman2/qrpic/issues',
        'Source Code': 'https://gitlab.com/Makman2/qrpic/-/tree/master',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        f'Programming Language :: Python :: {python_version}',
        'Topic :: Artistic Software',
        'Topic :: Printing',
    ],
)
