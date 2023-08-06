# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='CEP-por-endereco-completo',
    version='0.1.1',
    url='https://github.com/rodrigobercini/CEP-por-endereco-completo',
    license='MIT License',
    author='Rodrigo Bercini Martins',
    author_email='rodrigobercinimartins@gmail.com',
    keywords='cep endereço completo zip code brazil address correios',
    description=u'Encontrando CEP a partir de endereços completos',
    long_description='Encontrando CEP a partir de endereços completos usando o Site Oficial dos Correios como fonte',
    packages=['CEP-por-endereco-completo'],
    install_requires=["beautifulsoup4"],
)