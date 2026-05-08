from pathlib import Path
import json
import subprocess
import tempfile
import textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
CONTENT_PATH = ROOT / "src" / "data" / "content.json"
SOURCE_ROOT = Path("/Users/tico/Downloads/proyecto_carolina/proyecto carolina meses")
RENDERS = ROOT / "renders"
FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
SECONDS_PER_PHOTO = 1.55
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_SUFFIXES = {".mp4", ".mov"}
STAGES = {
    1: "periodo1_dic25-ene25",
    2: "periodo2_ene25-feb15",
    3: "periodo3_feb15-mar15",
    4: "periodo4_mar15-abr15",
    5: "periodo5_abr15-may15",
}


def wrap(value: str, width: int = 32) -> str:
    return "\n".join(textwrap.wrap(value, width=width, break_long_words=False))


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size=size)


def text_block(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, size: int, fill: str, spacing: int = 12) -> None:
    draw.multiline_text(xy, text, font=font(size), fill=fill, spacing=spacing)


def make_card(path: Path, *, title: str, subtitle: str, dates: str, body: str, eyebrow: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (1080, 1920), "#141414")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1080, 1920), fill="#141414")
    draw.rectangle((0, 0, 1080, 420), fill="#0a0a0a")
    draw.rectangle((0, 1500, 1080, 1920), fill="#050505")
    draw.text((60, 64), "NETFLIX", font=font(58), fill="#e50914")
    text_block(draw, (60, 178), eyebrow, 38, "#d2d2d2")
    text_block(draw, (60, 284), wrap(title, 20), 76, "#ffffff", spacing=8)
    if subtitle:
        text_block(draw, (60, 500), wrap(subtitle, 28), 42, "#d2d2d2")
    if dates:
        text_block(draw, (60, 1518), dates.upper(), 34, "#808080")
    if body:
        text_block(draw, (60, 1596), wrap(body, 34), 36, "#ffffff", spacing=12)
    image.save(path, "JPEG", quality=88)


def media_for_stage(stage: int) -> list[Path]:
    folder = SOURCE_ROOT / STAGES[stage]
    media = [
        path
        for path in folder.iterdir()
        if path.is_file()
        and not path.name.startswith("._")
        and path.name != ".DS_Store"
        and path.suffix.lower() in IMAGE_SUFFIXES | VIDEO_SUFFIXES
    ]
    return sorted(media, key=lambda path: (path.stat().st_mtime, path.name.lower()))


def can_decode_video(path: Path) -> bool:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height",
            "-of",
            "csv=p=0",
            str(path),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def render_visual_segment(source: Path, destination: Path, *, duration: float | None = None) -> bool:
    destination.parent.mkdir(parents=True, exist_ok=True)
    is_image = source.suffix.lower() in IMAGE_SUFFIXES
    if not is_image and not can_decode_video(source):
        print(f"skipping unreadable video: {source}")
        return False

    command = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    if is_image:
        command += ["-loop", "1", "-t", str(duration or SECONDS_PER_PHOTO)]
    command += ["-i", str(source)]

    filter_graph = (
        "[0:v]split=2[bg][fg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,gblur=sigma=28,eq=brightness=-0.14:saturation=0.82[bg];"
        "[fg]scale=1080:1920:force_original_aspect_ratio=decrease[fg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2,"
        "fps=30,setsar=1,format=yuv420p[out]"
    )

    command += [
        "-filter_complex",
        filter_graph,
        "-map",
        "[out]",
        "-an",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "24",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(destination),
    ]

    subprocess.run(command, check=True)
    return True


def main() -> None:
    RENDERS.mkdir(parents=True, exist_ok=True)
    cards = RENDERS / "cards"
    cards.mkdir(parents=True, exist_ok=True)
    content = json.loads(CONTENT_PATH.read_text(encoding="utf-8"))
    opening = content.get("miniMovies", {}).get("openingLine", "")
    closing = content.get("miniMovies", {}).get("closingLine", "")

    for episode in content["episodes"]:
        stage = int(episode["id"])
        media = media_for_stage(stage)
        if not media:
            continue

        out = RENDERS / f"etapa-{episode['id']}.mp4"
        segment_dir = RENDERS / "segments" / f"etapa-{episode['id']}"
        segment_dir.mkdir(parents=True, exist_ok=True)
        intro_card = cards / f"etapa-{episode['id']}-intro.jpg"
        end_card = cards / f"etapa-{episode['id']}-final.jpg"
        make_card(
            intro_card,
            title=episode["title"],
            subtitle=episode["subtitle"],
            dates=episode["dateRange"],
            body="",
            eyebrow=opening,
        )
        make_card(
            end_card,
            title=episode["title"],
            subtitle="",
            dates=episode["dateRange"],
            body=f"{episode['description']}\n\n{closing}",
            eyebrow="",
        )

        segments: list[Path] = []
        intro_segment = segment_dir / "000-intro.mp4"
        render_visual_segment(intro_card, intro_segment, duration=3)
        segments.append(intro_segment)

        for index, item in enumerate(media, start=1):
            segment = segment_dir / f"{index:03}-{item.stem[:48]}.mp4"
            if render_visual_segment(item, segment, duration=SECONDS_PER_PHOTO):
                segments.append(segment)

        final_segment = segment_dir / "999-final.mp4"
        render_visual_segment(end_card, final_segment, duration=4.5)
        segments.append(final_segment)

        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as list_file:
            for segment in segments:
                list_file.write(f"file '{segment.as_posix()}'\n")
            list_path = Path(list_file.name)

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(list_path),
                "-c:v",
                "copy",
                "-movflags",
                "+faststart",
                str(out),
            ],
            check=True,
        )
        list_path.unlink(missing_ok=True)
        print(out)


if __name__ == "__main__":
    main()
