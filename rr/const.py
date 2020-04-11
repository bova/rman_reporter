import os
from pathlib import Path


CONF_FILE_CANDIDATES = ['/etc/rman_reporter/rman_reporter.ini',
                        'c:\\rman_reporter\\rman_reporter.ini',
                        os.path.join(Path.home(), 'PycharmProjects', 'rman_reporter', 'rman_reporter.ini')]