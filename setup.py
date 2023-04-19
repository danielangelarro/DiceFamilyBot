from setuptools import setup, find_packages
from tgbot.config import *

f = open('README.md', 'r')

setup(
    name = 'DiceFamilyBot',
    version = '1.0',
    description = 'Bot de Apuestas',
    long_description = f.read(),
    long_description_content_type = "text/markdown",
    author = 'danielangelarro',
    author_email = 'danielangelarro@gmail.com',
    url = 'https://github.com/danielangelarro/Study-Organizer',
    scripts = ['bot.py'],
    packages = find_packages(),
    keywords = 'telegram bot betting',
    install_requires = ['pyTelegramBotAPI'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Environment :: Console',
        'License :: MIT-LICENSE',
    ]
)
