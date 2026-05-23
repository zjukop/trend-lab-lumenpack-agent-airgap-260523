import json

from lumenpack_agent_airgap.main import frames_as_json_lines, pack_text, unpack_frames


def test_pack_round_trip():
    text = "agent context through light"
    frames = pack_text(text, chunk_size=7)

    assert len(frames) == 4
    assert unpack_frames(frames) == text


def test_json_lines_smoke():
    output = frames_as_json_lines("hello", chunk_size=2)
    rows = [json.loads(line) for line in output.splitlines()]

    assert rows[0]["transfer_id"]
    assert rows[-1]["total"] == 3
