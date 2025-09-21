from .ATEM import ATEM_Abstract
from .config_manager import ConfigManager

class LabelController:
    """Handles logic for assigning and managing source labels on an ATEM switcher."""

    def __init__(self, atem: ATEM_Abstract, config: ConfigManager):
        self.atem: ATEM_Abstract = atem
        self.config: ConfigManager = config

    def assign_camera_operator(self, input_id: int, operator_name: str) -> str:
        """Assign a camera operator's name to a given input."""

        label = ""

        if(self.config.is_prefix_enabled()):
            prefix = self.config.get_label_prefix(f"input{input_id}")
            label += f"{prefix}"

        label += f"{operator_name}"

        if(self.config.is_suffix_enabled()):
            suffix = self.config.get_label_suffix(f"input{input_id}")
            label += f"{suffix}"
        try:
            # Only set the label, do not connect/disconnect here
            self.atem.set_input_long_name(input_id, label)
        except Exception as e:
            return str(e)
        
        return (f"Updated label for input ID {input_id} to {label}")