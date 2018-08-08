"""
Main entry point.

Responsible for configuration and prepare components
and start main loop from Runner.
"""
import argparse
import logging
import os
from pkg_resources import get_distribution, DistributionNotFound

from rmi import components
from rmi import config
from rmi import logger

log = logging.getLogger(__name__)


def get_rmi_version():
    try:
        version = get_distribution('rmi').version
    except DistributionNotFound:
        log.warning("Version is not available.")
        return None

    return version


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--config',
        help="Configuration", default=None, required=True)
    parser.add_argument(
        '-l', '--log-level',
        help="log levels:  CRITICAL,ERROR,WARNING,INFO,DEBUG,TRACE", default='INFO')
    parser.add_argument(
        '-r', '--register', action='append', dest='components',
        help="Register additional components in config", default=[])
    parser.add_argument(
        '-v', '--version', action='version', version=get_rmi_version(),
        help="Show version")

    args = parser.parse_args()

    # Initialize logging subsystem.
    logger.init_logging(args.log_level, package_name='rmi')
    log.debug('started PID=%r', os.getpid())
    log.info('Version rmi: %s', get_rmi_version())

    # Register internal & external components.
    components.register_components(extra_components=args.components)

    # Initialize all necessary objects.
    try:
        configuration = config.load_config(args.config)
    except config.ConfigLoadError as e:
        log.error('Error: Cannot load config file %r: %s', args.config, e)
        exit(1)

    # Extract main loop component.
    runner = configuration['runner']

    # Prepare and run the "main loop".
    runner.run()


if __name__ == '__main__':
    main()
