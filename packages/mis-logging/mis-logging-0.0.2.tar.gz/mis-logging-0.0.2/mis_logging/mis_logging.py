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

    def log_action(self, action):
        """Logs specific actions in code, like requesting information from a website."""

        # Action name with datetime
        self.logger.logger.info('App:' + str(self.app_name) +
                                ' Action: ' + str(action) +
                                ' Datetime: ' + str(datetime.datetime.now()))

    def log_success(self, location=''):
        """Logs success with a location if one is given"""

        # Success string
        success = 'App: ' + str(self.app_name)
        # If location string is provided
        if location:
            success += ' Location: ' + str(location)
        success += ' Datetime: ' + str(datetime.datetime.now())

        self.logger.logger.info(success)

    def log_failure(self, location=''):
        """Logs failure with a location if one is given"""

        # Failure string
        failure = 'App: ' + str(self.app_name)
        # If location string is provided
        if location:
            failure += ' Location: ' + str(location)
        failure += ' Datetime: ' + str(datetime.datetime.now())

        self.logger.logger.warning(failure)
