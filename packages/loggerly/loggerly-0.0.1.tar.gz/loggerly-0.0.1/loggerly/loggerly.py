import json
import logging
import requests


LOGGLY_CRITICAL = 'CRITICAL'
LOGGLY_WARNING = 'WARNING'


class Logger(logging.Logger):
    def __init__(self, module, url, log_level, env=None):
        self.url = url
        self.log_level = log_level        
        self.env = env
        super().__init__(module)

    def send_to_loggly(self, log_entry, loggly_error_level):
        # Log the error locally too
        self.emit_loggly_error_locally(log_entry, loggly_error_level)

        body = self.build_loggly_request_body(log_entry, loggly_error_level)

        response = requests.post(
            url=self.url,
            data=body,
            headers={'Content-Type': 'text/plain'})

        # Ensure log was received by loggly
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            self.critical('logs not sent to loggly: {}'.format(error))

        self.info('log sent to loggly: {}'.format(body))
        return response

    def emit_loggly_error_locally(self, log_entry, loggly_error_level):
        # A loggly WARNING is equivalent to this application's ERROR
        if loggly_error_level == LOGGLY_WARNING:
            self.error(log_entry)
        # And a loggly ERROR == this application's CRITICAL
        elif loggly_error_level == LOGGLY_CRITICAL:
            self.critical(log_entry)

    def build_loggly_request_body(self, log_entry, loggly_error_level):
        body = json.dumps({
            'env': self.env.upper(),
            'component': self.name,
            'message': '{} - {}'.format(loggly_error_level, log_entry),
            'level': loggly_error_level
        })

        return body


def get_logger(module_name, url, log_level, env):
    logger = Logger(module_name, url, log_level, env)
    logger.setLevel(logger.log_level)

    # Log to stderr
    sh = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    sh.setFormatter(formatter)

    sh.setLevel(logger.log_level)
    logger.addHandler(sh)

    return logger
