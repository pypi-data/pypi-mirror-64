from setuptools import setup, find_packages

# fetch readme for pypi
with open('README.rst', 'r') as file:
    readme = file.read()

name = 'simple_plotter_qt'
install_requires = [
    'simple-plotter',
    'setuptools_scm',
    'matplotlib>=2',
    'PyQt5'
]

license = 'GPL3'
summary = "Qt-based GUI front-end for simple-plotter"
git_source = "https://gitlab.com/thecker/simple-plotter-qt/"
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
        'gui_scripts': [
            'simple-plotter-qt = simple_plotter_qt.gui:main',
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
    keywords="plot plotting matplotlib gui",
    url=home,
    project_urls={
        "Documentation": doc_url,
        "Source Code": git_source,
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ]
)
