import os
import sys
import traceback
from yachalk import chalk

class ConsoleOutput:
    def __init__(self) -> None:
        os.system('color')

    def begin(self) -> None:
        print('')
        print(self.format_message('Begin monitoring NextUp ERP window. Type stop or press Ctrl+C to stop...'))

    def monitor_stop_requested(self) -> None:
        print(self.format_message(chalk.yellow_bright('Stop requested...')))

    def monitor_stopped(self) -> None:
        print(self.format_message(chalk.green('Successfully stopped.')))

    def no_more_input(self) -> None:
        print(self.format_message(chalk.yellow_bright('No longer accepting input due to SIGINT stop request')))

    def current_error_info(self, message: str) -> None:
        error_info = sys.exc_info()
        print(self.format_message(chalk.red(message + '. Error is: %s, details: %s' % (error_info[0], error_info[1]))))

    def error_message(self, message) -> None:
        print(self.format_message(chalk.red(message)))

    def attempting_to_start_server(self) -> None:
        print(self.format_message(chalk.yellow_bright('Server is not started. Attempting to start...')))

    def server_successfully_started(self) -> None:
        print(self.format_message(chalk.green('Server successfully started.')))

    def server_start_requested(self) -> None:
        self.generic_info('Server start requested...')

    def server_stop_requested(self) -> None:
        self.generic_info('Server stop requested...')

    def generic_info(self, message: str) -> None:
        print(self.format_message(chalk.yellow_bright(message)))

    def end(self) -> None:
        print(chalk.reset(''))

    def format_message(self, message:str) -> None:
        return "\t" + message