from pathlib import Path
from zipfile import ZipFile
import json
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
ZIP_PATH = Path("/Users/tico/Downloads/proyecto_carolina.zip")
PUBLIC = ROOT / "public" / "assets"
CONTENT_PATH = ROOT / "src" / "data" / "content.json"

STAGES = {
    1: "periodo1_dic25-ene25",
    2: "periodo2_ene25-feb15",
    3: "periodo3_feb15-mar15",
    4: "periodo4_mar15-abr15",
    5: "periodo5_abr15-may15",
}

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def stage_for_name(name: str) -> int | None:
    for stage, marker in STAGES.items():
        if f"/{marker}/" in name:
            return stage
    return None


def is_image(name: str) -> bool:
    path = Path(name)
    if "__MACOSX" in path.parts or path.name.startswith("._") or path.name == ".DS_Store":
        return False
    return path.suffix.lower() in IMAGE_SUFFIXES


def convert_to_jpg(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "sips",
            "-Z",
            "1920",
            "-s",
            "format",
            "jpeg",
            "-s",
            "formatOptions",
            "78",
            str(source),
            "--out",
            str(destination),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main() -> None:
    grouped: dict[int, list[str]] = {stage: [] for stage in STAGES}

    with ZipFile(ZIP_PATH) as archive:
        for name in archive.namelist():
            stage = stage_for_name(name)
            if stage and is_image(name):
                grouped[stage].append(name)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)

            for stage, names in grouped.items():
                photos_dir = PUBLIC / f"ep{stage}" / "photos"
                if photos_dir.exists():
                    shutil.rmtree(photos_dir)
                photos_dir.mkdir(parents=True, exist_ok=True)

                for index, name in enumerate(sorted(names), start=1):
                    raw = temp / f"stage-{stage}-{index}{Path(name).suffix.lower()}"
                    with archive.open(name) as source, raw.open("wb") as target:
                        shutil.copyfileobj(source, target)
                    convert_to_jpg(raw, photos_dir / f"{index:03}.jpg")

                first_photo = photos_dir / "001.jpg"
                thumb = PUBLIC / f"ep{stage}" / "thumb.jpg"
                if first_photo.exists():
                    shutil.copyfile(first_photo, thumb)

    hero = PUBLIC / "hero.jpg"
    ep1_thumb = PUBLIC / "ep1" / "thumb.jpg"
    if ep1_thumb.exists():
        shutil.copyfile(ep1_thumb, hero)

    content = json.loads(CONTENT_PATH.read_text(encoding="utf-8"))
    for episode in content["episodes"]:
        stage = int(episode["id"])
        photos_dir = PUBLIC / f"ep{stage}" / "photos"
        photos = sorted(photos_dir.glob("*.jpg"))
        episode["thumbnail"] = f"/assets/ep{stage}/thumb.jpg"
        episode["photos"] = [f"/assets/ep{stage}/photos/{photo.name}" for photo in photos]

    CONTENT_PATH.write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
