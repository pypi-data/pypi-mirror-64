from setuptools import setup, find_packages


long_description = 'A simple script to create a Django-backed React app, all in one.'

setup(
    name='create-django-react-app',
    version='0.0.1',
    author='Matthew Smith Burlage',
    author_email='matt@msb.dev',
    url='https://github.com/mattburlage/create-django-react-app',
    description='A simple script to create a Django-backed React app, all in one.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'create-django-react-app=create_django_react_app.create_django_react_app:main'
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    keywords='django react jwt create-django-react-app create-react-django-app',
    install_requires=None,
    zip_safe=False
)