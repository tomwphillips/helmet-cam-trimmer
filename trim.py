from typing import List, Tuple

import click
import ffmpeg

FFMPEG_PRESETS = [
    "ultrafast",
    "superfast",
    "veryfast",
    "faster",
    "fast",
    "medium",
    "slow",
    "slower",
    "veryslow",
]


def timestamp_to_seconds(timestamp: str) -> int:
    sign = 1
    if timestamp.startswith("-"):
        timestamp = timestamp[1:]
        sign = -1
    parts = timestamp.split(":")[::-1]
    return sign * sum(int(part) * 60**i for i, part in enumerate(parts))


def seconds_to_timestamp(seconds: int) -> str:
    sign = ""
    if seconds < 0:
        sign = "-"
        seconds = abs(seconds)
    hours = seconds // (60 * 60)
    seconds -= hours * 60 * 60
    minutes = seconds // 60
    seconds -= minutes * 60
    return f"{sign}{hours:02}:{minutes:02}:{seconds:02}"


def get_trim_timestamps(*timestamps: int, padding: int = 60) -> Tuple[int, int]:
    start = max(timestamps[0] - padding, 0)
    end = timestamps[-1] + padding
    return start, end


@click.command()
@click.argument("input_file")
@click.argument("timestamps", nargs=-1)
@click.argument("output_file")
@click.option(
    "--padding",
    default=60,
    help="Padding around timestamps in seconds",
    show_default=True,
)
@click.option(
    "--preset",
    default="medium",
    help="FFMPEG preset (slower provides better compression but takes longer)",
    type=click.Choice(FFMPEG_PRESETS),
    show_default=True,
)
def main(
    input_file: str, output_file: str, timestamps: List[str], padding: int, preset: str
) -> None:
    timestamps_seconds = [timestamp_to_seconds(timestamp) for timestamp in timestamps]
    start_timestamp, end_timestamp = get_trim_timestamps(
        *timestamps_seconds, padding=padding
    )
    (
        ffmpeg.input(input_file, ss=start_timestamp, to=end_timestamp)
        .output(output_file, preset=preset)
        .run()
    )


if __name__ == "__main__":
    main()
