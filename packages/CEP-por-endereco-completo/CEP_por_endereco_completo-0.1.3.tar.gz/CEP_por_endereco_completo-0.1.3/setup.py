# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='CEP_por_endereco_completo',
    version='0.1.3',
    url='https://github.com/rodrigobercini/CEP-por-endereco-completo',
    license='MIT License',
    author='Rodrigo Bercini Martins',
    author_email='rodrigobercinimartins@gmail.com',
    keywords='cep endereço completo zip code brazil address correios',
    description=u'Encontrando CEP a partir de endereços completos',
    long_description=long_description,
    long_description_content_type='text/markdown',  # This is important!
    packages=['CEP_por_endereco_completo'],
    install_requires=["beautifulsoup4"],
)