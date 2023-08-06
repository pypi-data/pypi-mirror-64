from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='play_in_bots_vk',
      version='0.1.6'
              '',
      description='Бот, который играет за вас',
      packages=['play_in_bots_vk'],
      author_email='ruslan@rym9n.ru',
      zip_safe=False)
