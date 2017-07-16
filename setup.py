import setuptools

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setuptools.setup(
    name="django-lrucache-backend",
    version="0.2.1",
    url="https://github.com/kogan/django-lrucache-backend",

    author="Josh Smeaton",
    author_email="josh.smeaton@gmail.com",

    description="A smarter local memory cache backend for Django",
    long_description=readme + '\n\n' + history,

    packages=setuptools.find_packages(exclude=('benchmarking', )),
    include_package_data=True,
    install_requires=['lru-dict', 'Django'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
    ],
)
