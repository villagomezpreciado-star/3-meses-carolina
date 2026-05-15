from pathlib import Path
import tempfile
import subprocess

import importlib.util
spec = importlib.util.spec_from_file_location("render_pro_movies", Path(__file__).with_name("render-pro-movies.py"))
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)


OUTPUT = base.ROOT / "final-renders-clean"
PUBLIC_CLEAN = base.ROOT / "public" / "assets" / "clean"


def concat(segments: list[Path], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
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
            "-fflags",
            "+genpts",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_path),
            "-vf",
            "fps=30,setsar=1,format=yuv420p",
            "-af",
            "aresample=async=1000:first_pts=0,aformat=sample_rates=44100:channel_layouts=stereo",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "23",
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
            str(output),
        ],
        check=True,
    )
    list_path.unlink(missing_ok=True)


def render_stage(stage: int) -> Path:
    stage_dir = OUTPUT / "segments" / f"etapa-{stage}"
    segments: list[Path] = []
    for index, item in enumerate(base.media_for_stage(stage), start=1):
        segment = stage_dir / f"{index:03}-{item.stem[:44]}.mp4"
        if base.render_segment(item, segment, duration=base.SECONDS_PER_PHOTO, caption=None):
            segments.append(segment)
    stage_output = OUTPUT / f"etapa-{stage}.mp4"
    concat(segments, stage_output)
    public_output = PUBLIC_CLEAN / f"etapa-{stage}-sin-subtitulos.mp4"
    base.public_encode(stage_output, public_output, music_path=base.STAGE_MUSIC.get(stage))
    return public_output


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    PUBLIC_CLEAN.mkdir(parents=True, exist_ok=True)
    public_outputs = [render_stage(stage) for stage in sorted(base.STAGES)]
    complete = PUBLIC_CLEAN / "3-meses-sin-subtitulos.mp4"
    concat(public_outputs, complete)
    print(complete)


if __name__ == "__main__":
    main()
