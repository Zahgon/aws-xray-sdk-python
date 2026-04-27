import os

from .exceptions.exceptions import InvalidDaemonAddressException

DAEMON_ADDRESS_KEY = "AWS_XRAY_DAEMON_ADDRESS"
DEFAULT_ADDRESS = '127.0.0.1:2000'


class DaemonConfig:
    """The class that stores X-Ray daemon configuration about
    the ip address and port for UDP and TCP port. It gets the address
    string from ``AWS_TRACING_DAEMON_ADDRESS`` and then from recorder's
    configuration for ``daemon_address``.
    A notation of '127.0.0.1:2000' or 'tcp:127.0.0.1:2000 udp:127.0.0.2:2001'
    are both acceptable. The former one means UDP and TCP are running at
    the same address.
    By default it assumes a X-Ray daemon running at 127.0.0.1:2000
    listening to both UDP and TCP traffic.
    """
    def __init__(self, daemon_address=DEFAULT_ADDRESS):
        if daemon_address is None:
            daemon_address = DEFAULT_ADDRESS

        val = os.getenv(DAEMON_ADDRESS_KEY, daemon_address)
        configs = val.split(' ')
        if len(configs) == 1:
            self._parse_single_form(configs[0])
        elif len(configs) == 2:
            self._parse_double_form(configs[0], configs[1], val)
        else:
            raise InvalidDaemonAddressException('Invalid daemon address %s specified.' % val)

    def _parse_single_form(self, val):
        pass

    def _parse_double_form(self, val1, val2, origin):
        pass

    @property
    def udp_ip(self):
        pass

    @property
    def udp_port(self):
        pass

    @property
    def tcp_ip(self):
        pass

    @property
    def tcp_port(self):
        pass
