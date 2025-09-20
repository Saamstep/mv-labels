from abc import ABC, abstractmethod
import PyATEMMax
import time

# Abstract base class for ATEM switcher control
class ATEM_Abstract(ABC):
    def __init__(self, host: str, port: int = 9910):
        self.host = host  # Host address as string
        self.port = port  # Default port as integer

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def get_all_video_sources(self) -> None:
        pass

    @abstractmethod
    def get_video_input(self, name) -> None:
        pass

    @abstractmethod
    def set_input_long_name(self, source: int, name: str) -> None:
        pass

# Concrete implementation using PyATEMMax
class PyAtemMax(ATEM_Abstract):
    def __init__(self, host: str, port: int = 9910):
        super().__init__(host, port)  # Pass host and port to base class
        self.switcher = PyATEMMax.ATEMMax()

    def connect(self) -> None:
        print("Connecting to switcher at ", self.host, ":", self.port, sep="")
        self.switcher.connect(self.host, self.port)

    def disconnect(self) -> None:
        self.switcher.disconnect()

    def get_all_video_sources(self) -> None:
        return PyATEMMax.ATEMVideoSources

    def get_video_input(self, id: int) -> None:
        print(f"Getting video input for ID {id}")
        return getattr(self.get_all_video_sources(), f"input{id}")    

    def set_input_long_name(self, id: int, name: str) -> None:
        self.connect()
        source = self.get_video_input(id)
        print(f"Waiting for connection...")
        connected = self.switcher.waitForConnection(infinite=False, timeout=5)
        print(f"waitForConnection returned: {connected}")
        if connected:
            print(f"Setting input {source} long name to '{name}'")
            self.switcher.setInputLongName(source, name)
            self.disconnect()
        else:
            print("Unable to connect to switcher")
        
