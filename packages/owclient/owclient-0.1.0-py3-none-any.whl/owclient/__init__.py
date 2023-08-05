"""
This package holds the abstraction libraries for 1 wire.
"""
import importlib
import logging
from typing import Optional
from typing import Tuple

import pyownet

from .devices import Device
from .exc import CouldNotConnectError
from .exc import CouldNotLoadDeviceError
from .exc import CouldNotLoadDevicesError
from .exc import UnrecognizedDeviceError


class OwClient:
    """
    An OWFS abstraction layer

    A light layer to use OWFS and pyownet with a more OOP approach.

    Parameters
    ----------
    host: str, optional:
        (Default value = 'localhost')
        Owserver host name or Ip addres to connect.
    port: int, optional:
        (Default value = 4034)
        Port the owserver is listening in.
    unchached: bool, optional:
        (Default value = True)
        Ignore the owfs server cache.
    """
    def __init__(self,
                 host: str = 'localhost',
                 port: int = 4304,
                 uncached: bool = True) -> None:
        self.host: str = host
        self.port: int = port
        self.uncached: bool = uncached
        self.__proxy: Optional[pyownet.protocol.__proxy] = None
        self.logger: logging.Logger = logging.getLogger(
            f'{__name__}.{type(self).__name__}')
        self.logger.debug(f'Initializing. {self}')

    def __repr__(self) -> str:
        return (f'<{type(self).__name__}('
                f'host={self.host}, '
                f'port={self.port}, '
                f'uncached={self.uncached} '
                f')>')

    def __connect(self) -> pyownet.protocol._Proxy:
        """
        Connect to the owserver.

        Creates or returns the proxy object in self.__proxy

        Returns
        -------
        __proxy:
            The pyownet proxy object.

        Raises
        ------
        CouldNotConnectError:
            When the owserver is unreachable.
        """
        if self.__proxy is None:
            try:
                self.logger.info('Trying to connect to owServer.')
                self.__proxy = pyownet.protocol.proxy(self.host, self.port)
                return self.__proxy
            except pyownet.protocol.ConnError as ex:
                error_message = (f'Could not connect to owserver in '
                                 f'<{self.host}:{self.port}>')
                self.logger.exception(error_message)
                raise CouldNotConnectError(error_message) from ex

        else:
            return self.__proxy

    def load_device(self,
                    path: str,
                    throw_on_unrecognized: bool = False) -> Device:
        """
        Load a device.

        Parameters
        ----------
        path : str:
            Path where the device is on the owfs virtual file system.

        throw_on_unrecognized : bool, optional:
             (Default value = False)
             Raise an exception if the device type is not in the .devices
             package

        Returns
        -------
        Device:
            A subclass of the Device class found in the .devices package

        Raises
        ------
        CouldNotLoadDeviceError:
            Raises when there is an OwnetError, for example when trying to load
            a non connected device

        UnrecognizedDeviceError:
            Raises when the device type module is not found on the .devices
            package
        """

        try:
            proxy = self.__connect()
            self.logger.debug(f'Trying to read device type device at {path}.')
            device_type = proxy.read(f'{path}type').decode('ascii')
            self.logger.debug(
                f'Trying to load class for device type: {device_type}')
            device_module = importlib.import_module(
                f'owclient.devices.{device_type.lower()}')
            device_class = getattr(device_module, device_type.upper())
            result = device_class(proxy, path, self.uncached)
            self.logger.debug(f'Device class loaded: {result.__class__}')
            return result
        except pyownet.protocol.OwnetError as ex:
            error_message = f'Could not load device at path {path}.'
            self.logger.exception(error_message)
            raise CouldNotLoadDeviceError(error_message) from ex
        except (ModuleNotFoundError, AttributeError) as ex:
            self.logger.debug('Device class not found. ')
            if throw_on_unrecognized:
                self.logger.exception('UnrecognizedDeviceError thrown.')
                raise UnrecognizedDeviceError() from ex
            else:
                self.logger.debug('Basic Device loaded.')
                return Device(proxy, path, self.uncached)

    @property
    def devices(self) -> Tuple[Device, ...]:
        """
        List all the devices in owserver root folder

        Returns
        -------
        Tuple[Device]:
            The list of devices found

        Raises
        ------
        CouldNotLoadDevicesError
            Raises when a generic pywonet.protocol.Error exception is raised
        """
        self.logger.info('Trying to list all devices on the bus.')

        if self.uncached is True:
            dir_path = '/uncached/'
        else:
            dir_path = '/'

        proxy = self.__connect()

        try:
            return tuple(
                self.load_device(f'/{device_path.split("/")[-1]}/')
                for device_path in proxy.dir(dir_path, slash=False))
        except pyownet.protocol.Error as ex:
            error_message = 'Could not load the devices on the bus.'
            self.logger.exception(error_message)
            raise CouldNotLoadDevicesError(error_message) from ex


__version__ = '0.1.1'
__all__ = ['OwClient']
