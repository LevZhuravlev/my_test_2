from setuptools import setup

requirements = [
	'plumbum',
	'PyYAML',
	'munch',
	'pytest',
	'colorlog',
	'aiogram',
	'dependency_injector',
	'yandex.translate',
	'mock'
]

setup(
	# Metadata
	name='uniyar_botan',
	version='0.0',
	description='uniyar helper bot',
	install_requires=requirements,
	entry_points={
		'console_scripts':
			['bot = botan.main:BotanApp.run']
		}
)
