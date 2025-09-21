from src.config_manager import ConfigManager
from src.ATEM import PyAtemMax
from src.LabelController import LabelController

config = ConfigManager()
[host, port] = config.get_connection_information()
atem = PyAtemMax(host, port)
labels = LabelController(atem, config)

def main():
    try:
        # ui.run(storage_secret="hi", title='Multiview Labels', dark=True, reload=False)
        atem.connect()
        id = 1
        name = "Nick"
        print(f"Setting operator name to: {name} for input {id}")
        status_msg = labels.assign_camera_operator(id, name)
        print(status_msg)

        id = 2
        name = "Tristan"
        print(f"Setting operator name to: {name} for input {id}")
        status_msg = labels.assign_camera_operator(id, name)
        print(status_msg)
        atem.disconnect()
    except KeyboardInterrupt:
        print("\nExiting on keyboard interrupt.")

if __name__ == '__main__':
    main()

