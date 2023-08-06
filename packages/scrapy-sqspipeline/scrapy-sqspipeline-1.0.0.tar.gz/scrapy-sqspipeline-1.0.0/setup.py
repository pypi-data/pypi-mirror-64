from setuptools import setup
from pathlib import Path

readme_path = Path(__file__).absolute().parent.joinpath('README.md')
long_description = readme_path.read_text(encoding='utf-8')

setup(
    name='scrapy-sqspipeline',
    version='1.0.0',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Scrapy',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='scrapy pipeline aws sqs',
    url='https://github.com/d-yoshi/scrapy-sqspipeline',
    author='d-yoshi',
    author_email='keisuke.yoshida.job@gmail.com',
    license='MIT',
    packages=['sqspipeline'],
    install_requires=[
        'Scrapy>=1.1',
        'boto3',
    ],
)
