from setuptools import setup, find_packages

# fetch readme for pypi
with open('README.rst', 'r') as file:
    readme = file.read()

name = 'simple_plotter'
install_requires = [
    'numpy',
    'setuptools_scm',
    'jinja2',
    # 'pytest'
]

license = 'MIT'
summary = "python code generator for plotting 2D line graphs"
git_source = "https://gitlab.com/thecker/simple-plotter/"
doc_url = "https://simple-plotter.readthedocs.io/"
home = "https://simple-plotter.readthedocs.io/en/latest/"

setup(
    name=name,
    # version=version,
    packages=find_packages(),

    include_package_data=True,

    use_scm_version=True,
    setup_requires=['setuptools_scm'],

    install_requires=install_requires,
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'simple-plotter = simple_plotter.cli:main'
        ]
    },

    package_data={
        'examples': ['*.json'],
        'templates': ['*.txt']
    },

    # metadata to display on PyPI
    author="Thies Hecker",
    author_email="thies.hecker@gmx.de",
    description=summary,
    long_description=readme,
    long_description_content_type='text/x-rst',
    license=license,
    keywords="plot plotting matplotlib numpy",
    url=home,
    project_urls={
        "Documentation": doc_url,
        "Source Code": git_source,
    },
    classifiers=[
        'License :: OSI Approved :: MIT License'
    ]
)
