from setuptools import setup, find_packages


with open('README.md', 'r') as readme, open('production_requirements.txt', 'r') as dependencies:
    long_description = readme.read()
    dependencies = dependencies.read()

    kwargs = {
        'name': 'covid19-open-api',
        'version': '0.0.2',
        'author': 'Natworpong Loyswai',
        'author_email': 'Natworpong.Loyswai@mail.kmutt.ac.th',
        'description': 'Thai Covid-19 status',
        'long_description': long_description,
        'long_description_content_type': 'text/markdown',
        'url': 'https://github.com/rsxss/covid19-open-api',
        'packages': find_packages(),
        'classifiers': [
            'Programming Language :: Python :: 3'
        ],
        'keywords': ['covid19'],
        'install_requires': dependencies
    }

    setup(**kwargs)
