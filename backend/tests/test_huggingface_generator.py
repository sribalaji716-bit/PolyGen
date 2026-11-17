
from pathlib import Path
from unittest.mock import Mock

import pytest

from backend.generation.huggingface_generator import HuggingFaceGenerator


def create_fake_glb(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"fake-glb-content")
    return str(path)


def test_generate_creates_glb(tmp_path):

    shape_file = create_fake_glb(tmp_path / "shape.glb")
    textured_file = create_fake_glb(tmp_path / "textured.glb")
    exported_file = create_fake_glb(tmp_path / "exported.glb")

    mock_client = Mock()

    mock_client.predict.side_effect = [
        (
            shape_file,
            textured_file,
            "Generation successful",
            {"vertices": 1000},
            1234
        ),
        (
            "Export successful",
            exported_file
        )
    ]

    generator = HuggingFaceGenerator(client=mock_client)

    result = generator.generate(
        "A futuristic sports car",
        tmp_path / "generated"
    )

    assert result.exists()
    assert result.suffix == ".glb"
    assert result.read_bytes() == b"fake-glb-content"

    assert mock_client.predict.call_count == 2


def test_invalid_prompt_does_not_call_api(tmp_path):

    mock_client = Mock()

    generator = HuggingFaceGenerator(client=mock_client)

    with pytest.raises(ValueError):
        generator.generate("Car", tmp_path)

    mock_client.predict.assert_not_called()


def test_missing_generation_output_fails(tmp_path):

    mock_client = Mock()
    mock_client.predict.return_value = None

    generator = HuggingFaceGenerator(client=mock_client)

    with pytest.raises(RuntimeError):
        generator.generate(
            "A futuristic sports car",
            tmp_path
        )

    assert mock_client.predict.call_count == 1
