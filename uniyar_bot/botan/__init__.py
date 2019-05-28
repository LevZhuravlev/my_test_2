import os
import yaml
import logging
import logging.config
from munch import DefaultMunch, DefaultFactoryMunch

from dependency_injector import containers
from dependency_injector import providers

class Core(containers.DeclarativeContainer):
	"""IoC container of core component providers."""

	config = providers.Configuration('config')

def _read_config(default_path):
	if os.path.exists(default_path):
		with open(default_path, 'rt') as f:
			config = yaml.safe_load(f.read())
			return DefaultMunch.fromDict(config, None)
	else:
		print('Config does not exist: "{}"\nExiting.'.format(default_path))
		exit(1)

def configure(config_filepath):
	config = _read_config(config_filepath)
		
	if "CHATSCRIPT_HOST" in os.environ.keys():
		config.chatscript.host = os.environ["CHATSCRIPT_HOST"]
	if "CHATSCRIPT_PORT" in os.environ.keys():
		config.chatscript.port = os.environ["CHATSCRIPT_PORT"]

	Core.config.override(config)

	if config == None:
		return
	if config.logging == None:
		return

	if  ( 
		config.logging.handlers != None and
		config.logging.handlers.logfile and 
		config.logging.handlers.logfile.filename
		):
			basedir = os.path.dirname(config.logging.handlers.logfile.filename)
			if not os.path.exists(basedir):
				os.makedirs(basedir)
	logging.config.dictConfig(config.logging)

	