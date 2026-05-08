from pathlib import Path
import json
import shutil
import subprocess
import tempfile
import textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path("/Users/tico/Downloads/proyecto_carolina/proyecto carolina meses")
CONTENT_PATH = ROOT / "src" / "data" / "content.json"
OUTPUT = ROOT / "final-renders"
PUBLIC_MOVIES = ROOT / "public" / "assets" / "mini-movies"
FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
SECONDS_PER_PHOTO = 1.45
MAX_VIDEO_SECONDS = 12
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_SUFFIXES = {".mp4", ".mov"}
STAGES = {
    1: "periodo1_dic25-ene25",
    2: "periodo2_ene25-feb15",
    3: "periodo3_feb15-mar15",
    4: "periodo4_mar15-abr15",
    5: "periodo5_abr15-may15",
}


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size=size)


def wrap(value: str, width: int = 31) -> str:
    return "\n".join(textwrap.wrap(value, width=width, break_long_words=False))


def text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, size: int, fill: str, spacing: int = 12) -> None:
    draw.multiline_text(xy, value, font=font(size), fill=fill, spacing=spacing)


def card(path: Path, *, title: str, subtitle: str, dates: str, body: str, eyebrow: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (1080, 1920), "#141414")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1080, 1920), fill="#141414")
    draw.rectangle((0, 0, 1080, 430), fill="#050505")
    draw.rectangle((0, 1480, 1080, 1920), fill="#050505")
    draw.text((60, 64), "NETFLIX", font=font(58), fill="#e50914")
    if eyebrow:
        text(draw, (60, 180), eyebrow, 38, "#d2d2d2")
    text(draw, (60, 290), wrap(title, 20), 74, "#ffffff", spacing=8)
    if subtitle:
        text(draw, (60, 508), wrap(subtitle, 28), 42, "#d2d2d2")
    if dates:
        text(draw, (60, 1518), dates.upper(), 34, "#808080")
    if body:
        text(draw, (60, 1596), wrap(body, 33), 36, "#ffffff", spacing=12)
    image.save(path, "JPEG", quality=90)


def credits_card(path: Path, credits: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (1080, 1920), "#000000")
    draw = ImageDraw.Draw(image)
    draw.text((60, 64), "NETFLIX", font=font(58), fill="#e50914")
    text(draw, (60, 240), "Creditos", 76, "#ffffff")
    y = 430
    for credit in credits:
        text(draw, (60, y), credit["role"].upper(), 28, "#808080")
        text(draw, (60, y + 48), credit["name"], 52, "#ffffff")
        y += 180
    text(draw, (60, 1660), "3 meses", 64, "#ffffff")
    text(draw, (60, 1748), "Una historia que apenas empieza.", 34, "#d2d2d2")
    image.save(path, "JPEG", quality=90)


def media_for_stage(stage: int) -> list[Path]:
    folder = SOURCE_ROOT / STAGES[stage]
    return sorted(
        [
            path
            for path in folder.iterdir()
            if path.is_file()
            and not path.name.startswith("._")
            and path.name != ".DS_Store"
            and path.suffix.lower() in IMAGE_SUFFIXES | VIDEO_SUFFIXES
        ],
        key=lambda path: (path.stat().st_mtime, path.name.lower()),
    )


def video_duration(path: Path) -> float | None:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    try:
        return float(result.stdout.strip())
    except ValueError:
        return None


def render_segment(source: Path, destination: Path, *, duration: float | None = None) -> bool:
    if destination.exists() and destination.stat().st_size > 0:
        return True
    is_image = source.suffix.lower() in IMAGE_SUFFIXES
    is_gif = source.suffix.lower() == ".gif"
    if not is_image and video_duration(source) is None:
        print(f"Skipping unreadable video: {source.name}")
        return False

    destination.parent.mkdir(parents=True, exist_ok=True)
    command = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    if is_image and not is_gif:
        command += ["-loop", "1", "-t", str(duration or SECONDS_PER_PHOTO)]
    elif is_gif:
        command += ["-t", str(duration or SECONDS_PER_PHOTO)]
    else:
        command += ["-t", str(min(video_duration(source) or MAX_VIDEO_SECONDS, MAX_VIDEO_SECONDS))]
    command += ["-i", str(source)]
    filter_graph = (
        "[0:v]split=2[bg][fg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,gblur=sigma=30,eq=brightness=-0.16:saturation=0.82[bg];"
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
        "ultrafast",
        "-crf",
        "25",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(destination),
    ]
    subprocess.run(command, check=True)
    return True


def concat(segments: list[Path], output: Path) -> None:
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
            "-c",
            "copy",
            str(output),
        ],
        check=True,
    )
    list_path.unlink(missing_ok=True)


def main() -> None:
    content = json.loads(CONTENT_PATH.read_text(encoding="utf-8"))
    opening = content.get("miniMovies", {}).get("openingLine", "")
    closing = content.get("miniMovies", {}).get("closingLine", "")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    PUBLIC_MOVIES.mkdir(parents=True, exist_ok=True)

    stage_outputs: list[Path] = []
    for episode in content["episodes"]:
        stage = int(episode["id"])
        stage_dir = OUTPUT / "segments" / f"etapa-{stage}"
        cards = OUTPUT / "cards"
        intro = cards / f"etapa-{stage}-intro.jpg"
        final = cards / f"etapa-{stage}-final.jpg"
        card(intro, title=episode["title"], subtitle=episode["subtitle"], dates=episode["dateRange"], body="", eyebrow=opening)
        card(
            final,
            title=episode["title"],
            subtitle="",
            dates=episode["dateRange"],
            body=f"{episode['description']}\n\n{closing}",
            eyebrow="",
        )

        segments: list[Path] = []
        intro_segment = stage_dir / "000-intro.mp4"
        render_segment(intro, intro_segment, duration=3)
        segments.append(intro_segment)
        for index, item in enumerate(media_for_stage(stage), start=1):
            segment = stage_dir / f"{index:03}-{item.stem[:44]}.mp4"
            if render_segment(item, segment, duration=SECONDS_PER_PHOTO):
                segments.append(segment)
        final_segment = stage_dir / "999-final.mp4"
        render_segment(final, final_segment, duration=4.5)
        segments.append(final_segment)

        stage_output = OUTPUT / f"etapa-{stage}.mp4"
        concat(segments, stage_output)
        shutil.copy(stage_output, PUBLIC_MOVIES / f"etapa-{stage}.mp4")
        stage_outputs.append(stage_output)
        print(stage_output)

    credits = OUTPUT / "cards" / "end-credits.jpg"
    credits_segment = OUTPUT / "segments" / "credits.mp4"
    credits_card(credits, content["credits"])
    render_segment(credits, credits_segment, duration=7)

    complete = OUTPUT / "3-meses-completo.mp4"
    concat(stage_outputs + [credits_segment], complete)
    shutil.copy(complete, PUBLIC_MOVIES / "3-meses-completo.mp4")
    print(complete)


if __name__ == "__main__":
    main()
