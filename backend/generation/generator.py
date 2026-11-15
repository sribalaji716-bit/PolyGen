
from abc import ABC, abstractmethod
from pathlib import Path


class TextTo3DGenerator(ABC):

    @abstractmethod
    def generate(self, prompt: str, output_dir: Path) -> Path:
        """
        Generate a 3D asset from a text prompt.

        Args:
            prompt: Description of the required 3D asset.
            output_dir: Directory to save the generated asset.

        Returns:
            Path to the generated 3D asset.
        """
        pass
