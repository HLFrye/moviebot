#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Moviebot',
    version='0.1',
    description='Movie Interest Tracker',
    author='Harvey Frye',
    url='https://www.github.com/HLFrye/moviebot',
    packages=['moviebot', 'moviebot.bot', 'moviebot.web'],
    install_requires=[
        "asyncpg==0.26.0",
        "discord.py==1.7.3",
        "python-dotenv==0.20.0",
        "aioimdb @ git+https://github.com/HLFrye/aioimdb.git@master",        
    ],
    entry_points = {
        'console_scripts': [
            'bot-run=moviebot.bot.main:main',
            'show_info=moviebot.bot.show_info:main',
        ],        
    }
)
