from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

repo_url = 'https://bitbucket.org/vsipchenko/vsipc_tools/'

setup_args = dict(
    name='vsipc_tools',
    version='1.2',
    description='Useful tools implemented by Vitalii Sipchenko',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Vitalii Sipchenko',
    author_email='vitaliisipchenko@gmail.com',
    keywords=['VsipcTools', 'vsipctools'],
    url=repo_url,
    download_url=repo_url
)

install_requires = [
    'pytest==5.4.1',
    'aiohttp==3.6.2'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
