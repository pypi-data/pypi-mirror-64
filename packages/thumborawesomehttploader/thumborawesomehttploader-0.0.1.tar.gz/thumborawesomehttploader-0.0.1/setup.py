from setuptools import setup, find_packages

with open('LICENSE') as f:
    license = f.read()

setup(
    name='thumborawesomehttploader',
    version='0.0.1',
    description='Thumbor Awesome HTTP loader',
    long_description="""
Simple HTTP loader for Thumbor

This loader also allows passing querying strings to URL
""",
    long_description_content_type="text/markdown",
    author='Alexandru Pinca',
    author_email='github@alexandru-pinca.me',
    # url='https://github.com/pinkahd/thumbor-awesome-http-loader',
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
)
