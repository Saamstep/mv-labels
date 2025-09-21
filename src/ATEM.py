from abc import ABC, abstractmethod
import PyATEMMax
import time

# Abstract base class for ATEM switcher control
class ATEM_Abstract(ABC):
    def __init__(self, host: str, port: int = 9910):
        self.host = host  # Host address as string
        self.port = port  # Default port as integer

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def get_all_video_sources(self):
        pass

    @abstractmethod
    def get_video_input(self, name):
        pass

    @abstractmethod
    def set_input_long_name(self, source: int, name: str):
        pass

# Concrete implementation using PyATEMMax
class PyAtemMax(ATEM_Abstract):
    def __init__(self, host: str, port: int = 9910):
        super().__init__(host, port)  # Pass host and port to base class
        self.switcher = PyATEMMax.ATEMMax()

    def connect(self) -> bool:
        print("Connecting to switcher at ", self.host, ":", self.port, sep="")
        # PyATEMMax.ATEMMax.connect expects (ip, connTimeout), not port
        self.switcher.connect(self.host, self.port)
        connected = self.switcher.waitForConnection(infinite=False, timeout=5)
        if connected:
            print(f"Connected to switcher")
            return True
        else:
            print(f"Unable to connect to the switcher")
            self.switcher.disconnect()
            return False

    def disconnect(self):
        print("Disconnecting from switcher")
        connected = self.switcher.waitForConnection(infinite=False, timeout=5)
        if connected:
            self.switcher.disconnect()
        else:
            print("ERROR_DISCONNECT")
            raise Exception("Unable to disconnect from switcher.")

    def get_all_video_sources(self) -> PyATEMMax.ATEMVideoSources:
        return PyATEMMax.ATEMVideoSources

    def get_video_input(self, id: int) -> None:
        print(f"Getting video input for ID {id}")
        return getattr(self.get_all_video_sources(), f"input{id}")    

    def set_input_long_name(self, id: int, name: str):
        # self.connect()

        # connected = self.switcher.waitForConnection(infinite=False, timeout=5)
        # if connected:
        source = self.get_video_input(id)
        print(f"Setting input {source} long name to '{name}'")
        self.switcher.setInputLongName(source, name)
            # self.disconnect()
        # else:
            # print("ERROR_SET_LONG_INPUT_NAME")
            # raise Exception("Unable to connect to switcher")

