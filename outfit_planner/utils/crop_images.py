import os
import tempfile
from pathlib import Path

from PIL import Image


TARGET_SIZE = (1240, 2160)


def crop_image(image_path: Path) -> bool:
    with Image.open(image_path) as image:
        if image.size == TARGET_SIZE:
            return False

        width, height = image.size
        left = (width - TARGET_SIZE[0]) // 2
        top = (height - TARGET_SIZE[1]) // 2
        cropped_image = image.crop(
            (left, top, left + TARGET_SIZE[0], top + TARGET_SIZE[1])
        )
        image_format = image.format

    if image_format is None:
        raise ValueError(f"Could not determine image format: {image_path}")

    with tempfile.NamedTemporaryFile(
        dir=image_path.parent, suffix=image_path.suffix, delete=False
    ) as temporary_file:
        temporary_path = Path(temporary_file.name)

    try:
        cropped_image.save(temporary_path, format=image_format)
        os.chmod(temporary_path, image_path.stat().st_mode)
        os.replace(temporary_path, image_path)
    finally:
        temporary_path.unlink(missing_ok=True)

    return True


def main() -> None:
    images_dir = Path(__file__).resolve().parent.parent / "images"
    if not images_dir.is_dir():
        raise FileNotFoundError(f"Images folder not found: {images_dir}")

    supported_extensions = Image.registered_extensions()
    image_paths = sorted(
        path
        for path in images_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in supported_extensions
    )

    cropped_count = sum(crop_image(path) for path in image_paths)
    skipped_count = len(image_paths) - cropped_count
    print(f"Cropped {cropped_count} image(s); left {skipped_count} unchanged.")


if __name__ == "__main__":
    main()
