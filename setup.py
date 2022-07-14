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
        "pyyaml",
        "asyncpg",
        "discord.py",
    ],
    entry_points = {
        'console_scripts': ['bot-run=moviebot.bot.main:main'],        
    }
)