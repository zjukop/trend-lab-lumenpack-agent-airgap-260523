from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Frame:
    transfer_id: str
    index: int
    total: int
    payload: str
    checksum: str


def checksum(text: str) -> str:
    """Return a short SHA-256 checksum for display in optical frames."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def pack_text(text: str, chunk_size: int = 512) -> list[Frame]:
    if chunk_size < 1:
        raise ValueError("chunk_size must be positive")

    chunks = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)] or [""]
    transfer_id = checksum(text)
    return [
        Frame(
            transfer_id=transfer_id,
            index=i,
            total=len(chunks),
            payload=chunk,
            checksum=checksum(chunk),
        )
        for i, chunk in enumerate(chunks)
    ]


def unpack_frames(frames: list[Frame]) -> str:
    ordered = sorted(frames, key=lambda frame: frame.index)
    if not ordered:
        return ""
    if any(frame.total != len(ordered) for frame in ordered):
        raise ValueError("missing frames")
    if any(frame.checksum != checksum(frame.payload) for frame in ordered):
        raise ValueError("checksum mismatch")
    text = "".join(frame.payload for frame in ordered)
    if ordered[0].transfer_id != checksum(text):
        raise ValueError("transfer checksum mismatch")
    return text


def frames_as_json_lines(text: str, chunk_size: int) -> str:
    return "\n".join(json.dumps(asdict(frame), separators=(",", ":")) for frame in pack_text(text, chunk_size))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create LumenPack checksummed context frames.")
    parser.add_argument("text", nargs="?", help="Text to pack. Use --text for explicit input.")
    parser.add_argument("--text", dest="text_option", help="Text to pack.")
    parser.add_argument("--chunk-size", type=int, default=512, help="Characters per frame.")
    args = parser.parse_args(argv)

    text = args.text_option if args.text_option is not None else args.text
    if text is None:
        parser.error("provide text as an argument or with --text")

    print(frames_as_json_lines(text, args.chunk_size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
