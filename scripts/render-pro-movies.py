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
OUTPUT = ROOT / "final-renders-pro-v2"
PUBLIC_MOVIES = ROOT / "public" / "assets" / "mini-movies"
MUSIC_PATH = Path("/Users/tico/Downloads/Taylor Swift - Out Of The Woods.mp3")
FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
SECONDS_PER_PHOTO = 1.65
MAX_VIDEO_SECONDS = 10
PUBLIC_WIDTH = 720
PUBLIC_HEIGHT = 1280
PUBLIC_MAXRATE = "1600k"
PUBLIC_BUFSIZE = "3200k"
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_SUFFIXES = {".mp4", ".mov"}
STAGES = {
    1: "periodo1_dic25-ene25",
    2: "periodo2_ene25-feb15",
    3: "periodo3_feb15-mar15",
    4: "periodo4_mar15-abr15",
    5: "periodo5_abr15-may15",
}

STAGE_QUOTES = {
    1: "De una invitación salió nuestra historia.",
    2: "La primera vez que todo se sintió real.",
    3: "Dos días, mil nervios y cero ganas de irme.",
    4: "Me hiciste sentir como la persona más especial del mundo.",
    5: "Incluso en lo difícil, te sigo escogiendo.",
}


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size=size)


def wrap(value: str, width: int = 31) -> str:
    return "\n".join(textwrap.wrap(value, width=width, break_long_words=False))


def text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, size: int, fill: str, spacing: int = 12) -> None:
    draw.multiline_text(xy, value, font=font(size), fill=fill, spacing=spacing)


def card(path: Path, *, title: str, subtitle: str, dates: str, body: str, eyebrow: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (1080, 1920), "#080808")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1080, 1920), fill="#080808")
    for y in range(1920):
        shade = int(8 + (y / 1920) * 18)
        draw.line((0, y, 1080, y), fill=(shade, shade, shade))
    draw.rectangle((0, 0, 1080, 520), fill="#030303")
    draw.rectangle((0, 1450, 1080, 1920), fill="#030303")
    draw.rectangle((60, 182, 68, 438), fill="#e50914")
    draw.text((60, 64), "NETFLIX", font=font(58), fill="#e50914")
    if eyebrow:
        text(draw, (92, 178), eyebrow.upper(), 30, "#bdbdbd")
    text(draw, (92, 260), wrap(title, 19), 78, "#ffffff", spacing=8)
    if subtitle:
        text(draw, (92, 540), wrap(subtitle, 28), 42, "#d2d2d2")
    if dates:
        text(draw, (60, 1518), dates.upper(), 32, "#808080")
    if body:
        text(draw, (60, 1596), wrap(body, 34), 34, "#ffffff", spacing=12)
    draw.line((60, 1438, 1020, 1438), fill="#282828", width=2)
    image.save(path, "JPEG", quality=90)


def quote_card(path: Path, *, episode: dict[str, str], quote: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (1080, 1920), "#050505")
    draw = ImageDraw.Draw(image)
    for y in range(1920):
        shade = int(5 + (y / 1920) * 22)
        draw.line((0, y, 1080, y), fill=(shade, shade, shade))
    draw.rectangle((72, 292, 88, 716), fill="#e50914")
    text(draw, (116, 292), "NUESTRA HISTORIA", 28, "#808080")
    text(draw, (116, 370), wrap(quote, 18), 72, "#ffffff", spacing=8)
    draw.line((116, 752, 880, 752), fill="#2a2a2a", width=2)
    text(draw, (116, 812), wrap(episode["description"], 31), 36, "#d2d2d2", spacing=12)
    text(draw, (116, 1516), episode["dateRange"].upper(), 30, "#808080")
    text(draw, (116, 1580), episode["title"], 44, "#ffffff")
    image.save(path, "JPEG", quality=90)


def credits_card(path: Path, credits: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (1080, 1920), "#000000")
    draw = ImageDraw.Draw(image)
    draw.text((60, 64), "NETFLIX", font=font(58), fill="#e50914")
    text(draw, (60, 240), "Creditos finales", 72, "#ffffff")
    draw.line((60, 350, 1020, 350), fill="#262626", width=2)
    y = 430
    for credit in credits:
        text(draw, (60, y), credit["role"].upper(), 28, "#808080")
        text(draw, (60, y + 48), credit["name"], 52, "#ffffff")
        y += 180
    text(draw, (60, 1630), "3 meses", 64, "#ffffff")
    text(draw, (60, 1720), "Cada dia me enamoro mas de ti.", 34, "#d2d2d2")
    text(draw, (60, 1784), "Continuara...", 34, "#808080")
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


def has_audio(path: Path) -> bool:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0 and "audio" in result.stdout


def public_encode(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    duration = video_duration(source) or 0
    video_filter = (
        f"[0:v]scale={PUBLIC_WIDTH}:{PUBLIC_HEIGHT}:force_original_aspect_ratio=decrease,"
        f"pad={PUBLIC_WIDTH}:{PUBLIC_HEIGHT}:(ow-iw)/2:(oh-ih)/2:black,"
        "fps=30,setsar=1,format=yuv420p[v]"
    )
    command = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(source)]
    if MUSIC_PATH.exists() and duration > 0:
        fade_start = max(0.0, duration - 2.5)
        command += ["-stream_loop", "-1", "-i", str(MUSIC_PATH)]
        audio_filter = (
            "[0:a]volume=1.18,aformat=sample_rates=44100:channel_layouts=stereo[a0];"
            f"[1:a]atrim=0:{duration},asetpts=PTS-STARTPTS,volume=0.13,"
            f"afade=t=in:st=0:d=1.2,afade=t=out:st={fade_start}:d=2.5[music];"
            "[a0][music]amix=inputs=2:duration=first:dropout_transition=2,"
            "alimiter=limit=0.92,aresample=async=1:first_pts=0[a]"
        )
        command += ["-filter_complex", f"{video_filter};{audio_filter}", "-map", "[v]", "-map", "[a]"]
    else:
        command += ["-filter_complex", video_filter, "-map", "[v]", "-map", "0:a:0"]
    command += [
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "30",
        "-maxrate",
        PUBLIC_MAXRATE,
        "-bufsize",
        PUBLIC_BUFSIZE,
        "-profile:v",
        "main",
        "-level",
        "3.1",
        "-r",
        "30",
        "-g",
        "60",
        "-c:a",
        "aac",
        "-ar",
        "44100",
        "-ac",
        "2",
        "-b:a",
        "128k",
        "-avoid_negative_ts",
        "make_zero",
        "-movflags",
        "+faststart",
        str(destination),
    ]
    subprocess.run(command, check=True)


def render_segment(source: Path, destination: Path, *, duration: float | None = None) -> bool:
    if destination.exists() and destination.stat().st_size > 0:
        return True
    is_image = source.suffix.lower() in IMAGE_SUFFIXES
    is_gif = source.suffix.lower() == ".gif"
    if not is_image and video_duration(source) is None:
        print(f"Skipping unreadable video: {source.name}")
        return False

    destination.parent.mkdir(parents=True, exist_ok=True)
    segment_duration = duration or SECONDS_PER_PHOTO
    command = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    if is_image and not is_gif:
        command += ["-loop", "1", "-t", str(segment_duration)]
    elif is_gif:
        command += ["-t", str(segment_duration)]
    else:
        segment_duration = min(video_duration(source) or MAX_VIDEO_SECONDS, MAX_VIDEO_SECONDS)
        command += ["-t", str(segment_duration)]
    command += ["-i", str(source), "-f", "lavfi", "-t", str(segment_duration), "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
    audio_source = "0:a:0" if (not is_image and has_audio(source)) else "1:a:0"
    out_fade_start = max(0.0, segment_duration - 0.22)
    audio_fade_start = max(0.0, segment_duration - 0.25)
    filter_graph = (
        "[0:v]split=2[bg][fg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,gblur=sigma=36,eq=brightness=-0.20:saturation=0.86[bg];"
        "[fg]scale=1000:1780:force_original_aspect_ratio=decrease,"
        "eq=contrast=1.05:saturation=1.08[fg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2,"
        "noise=alls=3:allf=t+u,"
        f"fade=t=in:st=0:d=0.18,fade=t=out:st={out_fade_start}:d=0.22,"
        "fps=30,setsar=1,format=yuv420p[out];"
        f"[{audio_source}]aformat=sample_rates=44100:channel_layouts=stereo,"
        f"afade=t=in:st=0:d=0.12,afade=t=out:st={audio_fade_start}:d=0.25[aout]"
    )
    command += [
        "-filter_complex",
        filter_graph,
        "-map",
        "[out]",
        "-map",
        "[aout]",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "23",
        "-c:a",
        "aac",
        "-ar",
        "44100",
        "-ac",
        "2",
        "-b:a",
        "128k",
        "-shortest",
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
        quote = cards / f"etapa-{stage}-quote.jpg"
        card(intro, title=episode["title"], subtitle=episode["subtitle"], dates=episode["dateRange"], body="", eyebrow=opening)
        quote_card(quote, episode=episode, quote=STAGE_QUOTES.get(stage, episode["subtitle"]))
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
        render_segment(intro, intro_segment, duration=3.2)
        segments.append(intro_segment)
        media_items = media_for_stage(stage)
        middle_index = max(1, len(media_items) // 2)
        for index, item in enumerate(media_items, start=1):
            segment = stage_dir / f"{index:03}-{item.stem[:44]}.mp4"
            if render_segment(item, segment, duration=SECONDS_PER_PHOTO):
                segments.append(segment)
            if index == middle_index:
                quote_segment = stage_dir / "500-story-text.mp4"
                render_segment(quote, quote_segment, duration=3.4)
                segments.append(quote_segment)
        final_segment = stage_dir / "999-final.mp4"
        render_segment(final, final_segment, duration=4.8)
        segments.append(final_segment)

        stage_output = OUTPUT / f"etapa-{stage}.mp4"
        concat(segments, stage_output)
        public_encode(stage_output, PUBLIC_MOVIES / f"etapa-{stage}.mp4")
        stage_outputs.append(stage_output)
        print(stage_output)

    credits = OUTPUT / "cards" / "end-credits.jpg"
    credits_segment = OUTPUT / "segments" / "credits.mp4"
    credits_card(credits, content["credits"])
    render_segment(credits, credits_segment, duration=7)

    complete = OUTPUT / "3-meses-completo.mp4"
    concat(stage_outputs + [credits_segment], complete)
    public_encode(complete, PUBLIC_MOVIES / "3-meses-completo.mp4")
    print(complete)


if __name__ == "__main__":
    main()
