from plumbum import cli
import logging
import botan
from . serve import ServeSubcmd

log = logging.getLogger(__name__)

class BotanApp(cli.Application):

	config_path = cli.SwitchAttr(
		['-c', '--config'],
		str, default='config.yaml',
		help="Settings file for Botan Application")
	
	def main(self):
		botan.configure(config_filepath='./'+self.config_path)
		
		log.info('run botan')

		if not self.nested_command:
			self.help()
			return 1
	
	@classmethod
	def run(cls, argv=None, exit=True):
		try:
			super(BotanApp, cls).run(argv=argv, exit=exit)
		except Exception as e:
			log.critical(e, exc_info=True)
			quit(1)

BotanApp.subcommand('serve', ServeSubcmd)
		
if __name__ == "__main__":
	BotanApp.unbind_switches('--help-all')
	BotanApp.run()