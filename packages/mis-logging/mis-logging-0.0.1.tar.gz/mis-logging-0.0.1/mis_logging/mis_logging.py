import psutil
import datetime


class FlaskLogger(object):
    """Provides MIS Flask applications with consistent logging across micro-services."""

    def __init__(self, app_name, logger):
        """Initiate the logger with the app name and the logger."""
        self.app_name = app_name
        self.logger = logger

    def log_server(self):
        """Logs server information such as CPU and memory, allows us to see server usage."""

        # Server CPU percent with datetime
        self.logger.logger.info('App:' + str(self.app_name) +
                                ' CPU: ' + str(psutil.cpu_percent()) +
                                '% Datetime: ' + str(datetime.datetime.now()))

        # Server memory percent with datetime
        self.logger.logger.info('App:' + str(self.app_name) +
                                ' Memory: ' + str(psutil.virtual_memory().percent) +
                                '% Datetime: ' + str(datetime.datetime.now()))

    def log_action(self, action, ):
        """Logs specific actions in code, like requesting information from a website."""

        # Action name with datetime
        self.logger.logger.info('App:' + str(self.app_name) +
                                ' Action: ' + str(action) +
                                ' Datetime: ' + str(datetime.datetime.now()))
