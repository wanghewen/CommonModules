from setuptools import setup, find_packages
setup(
    name = 'CommonModules',
    packages = find_packages(where = '.'), # this must be the same as the name above
    version = '0.1.19',
    description = 'Common Python modules/functionalities used in practice.',
    author = 'Wang Hewen',
    author_email = 'wanghewen2@sina.com',
    url = 'https://github.com/wanghewen/CommonModules', # use the URL to the github repo
    keywords = ['library'], # arbitrary keywords
    license='MIT',
    install_requires=["wget"],
	extras_require = {
        'Advance DataStructureOperations':  ['scipy', 'numpy'],
		'Advance DataStructure IO':  ['networkx', 'numpy', 'scipy']
    }
)