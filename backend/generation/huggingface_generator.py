
from pathlib import Path
from uuid import uuid4
from shutil import copy2

from gradio_client import Client

from backend.generation.generator import TextTo3DGenerator


class HuggingFaceGenerator(TextTo3DGenerator):

    def __init__(self, client: Client | None = None):
        self.space_id = "tencent/Hunyuan3D-2"
        self.client = client

    def _get_client(self):
        if self.client is None:
            self.client = Client(self.space_id)

        return self.client

    def _validate_file(self, file_path, label: str) -> Path:

        if not file_path:
            raise RuntimeError(f"{label} was not returned.")

        path = Path(file_path)

        if not path.is_file():
            raise RuntimeError(f"{label} does not exist: {path}")

        if path.suffix.lower() != ".glb":
            raise RuntimeError(
                f"{label} must be a GLB file, got {path.suffix}"
            )

        return path

    def generate(self, prompt: str, output_dir: Path) -> Path:

        if not isinstance(prompt, str) or len(prompt.strip()) < 5:
            raise ValueError(
                "Prompt must contain at least 5 characters."
            )

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        client = self._get_client()

        # Step 1: Generate both meshes
        result = client.predict(
            caption=prompt.strip(),
            image=None,
            mv_image_front=None,
            mv_image_back=None,
            mv_image_left=None,
            mv_image_right=None,
            steps=5,
            guidance_scale=5.0,
            seed=1234,
            octree_resolution=256,
            check_box_rembg=True,
            num_chunks=8000,
            randomize_seed=True,
            api_name="/generation_all"
        )

        if not isinstance(result, (tuple, list)) or len(result) < 2:
            raise RuntimeError(
                "Unexpected response from 3D generation API."
            )

        shape_file = self._validate_file(
            result[0], "Generated shape mesh"
        )

        textured_file = self._validate_file(
            result[1], "Generated textured mesh"
        )

        # Step 2: Export textured mesh as GLB
        export_result = client.predict(
            file_out=str(shape_file),
            file_out2=str(textured_file),
            file_type="glb",
            reduce_face=False,
            export_texture=True,
            target_face_num=10000,
            api_name="/on_export_click"
        )

        if (
            not isinstance(export_result, (tuple, list))
            or len(export_result) < 2
        ):
            raise RuntimeError(
                "Unexpected response from GLB export API."
            )

        exported_file = self._validate_file(
            export_result[1], "Exported GLB"
        )

        # Step 3: Store final asset locally
        destination = output_dir / f"polygen_{uuid4().hex[:12]}.glb"

        copy2(exported_file, destination)

        return destination
