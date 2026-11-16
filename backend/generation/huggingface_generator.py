
from pathlib import Path
from gradio_client import Client
from backend.generation.generator import TextTo3DGenerator


class HuggingFaceGenerator(TextTo3DGenerator):

    def __init__(self):
        self.space_id = "tencent/Hunyuan3D-2"

    def generate(self, prompt: str, output_dir: Path) -> Path:

        if not prompt or len(prompt.strip()) < 5:
            raise ValueError("Prompt must contain at least 5 characters.")

        output_dir.mkdir(parents=True, exist_ok=True)

        client = Client(self.space_id)

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

        if not result or not result[0]:
            raise RuntimeError("3D generation did not return an output file.")

        generated_file = Path(result[0])

        if not generated_file.is_file():
            raise RuntimeError("Generated 3D file was not found.")

        destination = output_dir / f"{generated_file.stem}.glb"

        if generated_file.suffix.lower() != ".glb":
            raise RuntimeError(
                f"Expected GLB output, received {generated_file.suffix}"
            )

        import shutil
        shutil.copy2(generated_file, destination)

        return destination
