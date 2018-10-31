import setuptools

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setuptools.setup(
    name="django-lrucache-backend",
    version="2.0.0",
    url="https://github.com/kogan/django-lrucache-backend",

    author="Josh Smeaton",
    author_email="josh.smeaton@gmail.com",

    description="A smarter local memory cache backend for Django",
    long_description=readme + '\n\n' + history,

    packages=setuptools.find_packages(exclude=('benchmarking', )),
    include_package_data=True,
    install_requires=['lru-dict', 'Django'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
    ],
)
