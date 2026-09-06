#!/usr/bin/env python3
"""Read-only effective ARE/CRE/BCS census for the SoD filler audit.

Only CSV metadata and hashes are written to --output; extracted/decompiled game
resources and WeiDU diagnostics stay in --work (an ignored research directory).
Offsets: IESDP ARE V1 and CRE V1, cross-checked with local bg-modding references.
The local ie-areas.md spawn-point +0xAC/+0xB4 note is incorrect: use the primary
specification's +0x84 max, +0x86 enabled, +0x88 appearance schedule.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import struct
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from verify_ending import ResourceStore, VerificationError, cstring, section


HOUR_MASK = 0x00FFFFFF
CRE_SCRIPTS = {"override": 0x248, "class": 0x250, "race": 0x258,
               "general": 0x260, "default": 0x268}
ACTOR_SCRIPTS = {"override": 0x50, "general": 0x58, "class": 0x60,
                 "race": 0x68, "default": 0x70, "specific": 0x78}
CREATE_RE = re.compile(r'\b(CreateCreature\w*|CreateRandomCreature)\s*\(\s*"([^"]+)"', re.I)
FIRST_CRE_ACTIONS = {name.casefold() for name in (
    "CreateCreature", "CreateCreatureEffect", "CreateCreatureObject", "CreateCreatureObjectEffect",
    "CreateCreatureImpassable", "CreateCreatureImpassableEffect", "CreateCreatureDoor",
    "CreateCreatureObjectDoor", "CreateCreatureObjectOffScreen", "CreateCreatureOffScreen",
    "CreateCreatureObjectCopy", "CreateCreatureObjectCopyEffect", "CreateCreatureObjectOffset",
    "CreateCreatureCopyPoint", "CreateCreatureImpassableAllowOverlap", "CreateCreatureImpassableAllowOverlapEffect")}
CUT_RE = re.compile(r'OUTER_SPRINT\s+\$csr_cut_(bd\w+)\(~([^~]+)~\)', re.I)


def u16(data: bytes, offset: int) -> int:
    return struct.unpack_from("<H", data, offset)[0]


def u32(data: bytes, offset: int) -> int:
    return struct.unpack_from("<I", data, offset)[0]


def ref(data: bytes, offset: int, size: int = 8) -> str:
    return cstring(data[offset:offset + size])


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def creation_calls(text: str) -> list[dict]:
    calls = []
    for match in CREATE_RE.finditer(text):
        action, cre = match.groups()
        # Native action 246 has location-name, scope, CRE; all other literal
        # creation actions encountered in this corpus take CRE first.
        kind = "cre"
        if action.casefold() == "createcreatureatlocation":
            tail = re.match(r'\s*,\s*"[^"]*"\s*,\s*"([^"]+)"', text[match.end():])
            if not tail:
                raise VerificationError("unrecognized CreateCreatureAtLocation arguments")
            cre = tail[1]
        elif action.casefold() == "createrandomcreature":
            kind = "group"
        elif action.casefold() not in FIRST_CRE_ACTIONS:
            raise VerificationError(f"unhandled creation action signature: {action}")
        calls.append({"line": text.count("\n", 0, match.start()) + 1,
                      "action": action, "cre_or_group": cre.upper(), "reference_kind": kind})
    return calls


def schedule(value: int) -> dict:
    mask = value & HOUR_MASK
    return {"schedule_hex": f"0x{value:08X}", "scheduled_hours": mask.bit_count(),
            "schedule_active": int(bool(mask)),
            "hours": "|".join(str(hour) for hour in range(24) if mask & (1 << hour))}


def creature(data: bytes) -> dict:
    if len(data) < 0x2D4 or data[:8] != b"CRE V1.0":
        raise VerificationError("CRE is truncated or not CRE V1.0")
    io, ic = u32(data, 0x2BC), u32(data, 0x2C0)
    section(data, io, ic, 0x14, "CRE items")
    items = [{"index": i, "item": ref(data, io + i * 0x14).upper(),
              "flags_hex": f"0x{u32(data, io + i * 0x14 + 0x10):08X}",
              "undroppable": int(bool(u32(data, io + i * 0x14 + 0x10) & 8)),
              "charges1": u16(data, io + i * 0x14 + 0xA),
              "charges2": u16(data, io + i * 0x14 + 0xC),
              "charges3": u16(data, io + i * 0x14 + 0xE)} for i in range(ic)]
    return {"kill_xp": u32(data, 0x14), "ea": data[0x270],
            "name_strref": u32(data, 8), "current_hp": u16(data, 0x24), "max_hp": u16(data, 0x26),
            "state_hex": f"0x{u32(data, 0x20):08X}", "state_dead": int(bool(u32(data, 0x20) & 0x800)),
            "deathvar": ref(data, 0x280, 32), "dialogue": ref(data, 0x2CC).upper(),
            **{f"cre_{slot}": ref(data, off).upper() for slot, off in CRE_SCRIPTS.items()},
            "items": items}


def area(data: bytes, name: str) -> dict:
    if len(data) < 0xC4 or data[:8] != b"AREAV1.0":
        raise VerificationError(f"{name}: truncated or unsupported ARE signature")
    ao, ac = u32(data, 0x54), u16(data, 0x58)
    so, sc = u32(data, 0x60), u32(data, 0x64)
    ro, rc = u32(data, 0x5C), u16(data, 0x5A)
    for offset, count, size, label in ((ao, ac, 0x110, "actors"),
                                     (so, sc, 0xC8, "spawn points"),
                                     (ro, rc, 0xC4, "regions")):
        section(data, offset, count, size, f"{name} {label}")
    actors = []
    for i in range(ac):
        b = ao + i * 0x110
        embedded_off, embedded_size = u32(data, b + 0x88), u32(data, b + 0x8C)
        # An attached CRE is addressed by the explicit offset/size. Keep flags
        # separately visible: external resource lookup must not replace it.
        if embedded_size:
            section(data, embedded_off, 1, embedded_size, f"{name} actor {i} embedded CRE")
            if not embedded_off:
                raise VerificationError(f"{name} actor {i}: null embedded CRE offset")
        actors.append({"area": name, "index": i, "actor_name": ref(data, b, 32),
                       "x": u16(data, b + 0x20), "y": u16(data, b + 0x22),
                       "flags_hex": f"0x{u32(data, b + 0x28):08X}",
                       **schedule(u32(data, b + 0x40)),
                       "cre": ref(data, b + 0x80).upper(),
                       "actor_dialogue": ref(data, b + 0x48).upper(),
                       **{f"actor_{slot}": ref(data, b + off).upper()
                          for slot, off in ACTOR_SCRIPTS.items()},
                       "embedded_offset": embedded_off, "embedded_size": embedded_size})
    spawns = []
    for i in range(sc):
        b = so + i * 0xC8
        count, maximum, enabled = u16(data, b + 0x74), u16(data, b + 0x84), u16(data, b + 0x86)
        if count > 10:
            raise VerificationError(f"{name} spawn {i}: table count {count} exceeds 10")
        refs = [ref(data, b + 0x24 + j * 8).upper() for j in range(10)]
        sch = schedule(u32(data, b + 0x88))
        method = u16(data, b + 0x7A)
        spawns.append({"area": name, "index": i, "spawn_name": ref(data, b, 32),
                       "x": u16(data, b + 0x20), "y": u16(data, b + 0x22),
                       "table_count": count, "table": "|".join(refs[:count]),
                       "all_slots": "|".join(refs), "difficulty": u16(data, b + 0x76),
                       "frequency_seconds": u16(data, b + 0x78),
                       "method_hex": f"0x{method:04X}", "one_time": int(bool(method & 2)),
                       "temporarily_disabled": int(bool(method & 4)),
                       "max_spawn": maximum, "enabled": enabled, **sch,
                       "day_chance": u16(data, b + 0x8C), "night_chance": u16(data, b + 0x8E),
                       "ee_frequency": u32(data, b + 0x90),
                       "ee_countdown": u32(data, b + 0x94),
                       "weights": "|".join(str(v) for v in data[b + 0x98:b + 0xA2]),
                       "configured_and_scheduled": int(bool(count and maximum and enabled and sch["schedule_active"]))})
    regions = []
    for i in range(rc):
        b = ro + i * 0xC4
        flags = u32(data, b + 0x60)
        regions.append({"area": name, "index": i, "region_name": ref(data, b, 32),
                        "type": u16(data, b + 0x20),
                        **{key: u16(data, b + off) for key, off in
                           (("x1", 0x22), ("y1", 0x24), ("x2", 0x26), ("y2", 0x28))},
                        "destination": ref(data, b + 0x38).upper(),
                        "entrance": ref(data, b + 0x40, 32),
                        "flags_hex": f"0x{flags:08X}", "deactivated": int(bool(flags & 0x100)),
                        "trapped": u16(data, b + 0x6C), "script": ref(data, b + 0x7C).upper()})
    rest_off = u32(data, 0xC0)
    rest = {"area": name, "present": int(bool(rest_off))}
    if rest_off:
        section(data, rest_off, 1, 0xAC, f"{name} rest header")
        count = u16(data, rest_off + 0x98)
        if count > 10:
            raise VerificationError(f"{name} rest: table count {count} exceeds 10")
        refs = [ref(data, rest_off + 0x48 + j * 8).upper() for j in range(10)]
        rest.update({"table_count": count, "table": "|".join(refs[:count]),
                     "all_slots": "|".join(refs), "difficulty": u16(data, rest_off + 0x9A),
                     "max_spawn": u16(data, rest_off + 0xA4), "enabled": u16(data, rest_off + 0xA6),
                     "day_chance": u16(data, rest_off + 0xA8), "night_chance": u16(data, rest_off + 0xAA)})
        rest["configured"] = int(bool(count and rest["max_spawn"] and rest["enabled"]))
        rest["has_bdnorest"] = int("BDNOREST" in refs[:count])
    return {"area": name, "script": ref(data, 0x94).upper(),
            "flags_hex": f"0x{u32(data, 0x14):08X}",
            "type_hex": f"0x{u16(data, 0x48):04X}",
            "actors": actors, "spawn_points": spawns, "regions": regions, "rest": rest}


class AuditStore(ResourceStore):
    """Use the ending verifier's safe extraction, with a cached loose index."""

    def __init__(self, game: Path, work: Path):
        super().__init__(game, work)
        self.loose = {p.name.upper(): p for p in self.override.iterdir() if p.is_file()}
        self.records = {}

    def loose_path(self, resource: str) -> Path | None:
        return self.loose.get(resource.upper())

    def read_bytes(self, resource: str) -> bytes:
        resource = resource.upper()
        path = self.materialize(resource)
        data = path.read_bytes()
        self.records[resource] = {"resource": resource, "source": "override" if resource in self.loose else "KEY/BIFF",
                                  "bytes": len(data), "sha256": digest(data)}
        return data

    def names(self, extension: str) -> set[str]:
        return {f"{r}.{e}" for r, e in self.inventory if e == extension} | {
            name for name in self.loose if name.endswith("." + extension)}


def write_csv(path: Path, rows: list[dict]) -> None:
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def decompile(store: AuditStore, names: set[str], output: Path) -> dict[str, str]:
    output.mkdir(exist_ok=True)
    existing = sorted(name for name in names if store.exists(name))
    for start in range(0, len(existing), 30):
        chunk = existing[start:start + 30]
        for name in chunk:
            store.read_bytes(name)
        result = subprocess.run([str(store.weidu), "--game", str(store.game_dir),
                                 *[str(store.materialize(name)) for name in chunk], "--no-exit-pause"],
                                cwd=output, capture_output=True, text=True, errors="replace", timeout=180)
        (output / f"batch-{start // 30:03d}.log").write_text(result.stdout + result.stderr, encoding="utf-8")
        if result.returncode:
            raise VerificationError(f"WeiDU decompile failed: see {output / f'batch-{start // 30:03d}.log'}")
    paths = {p.name.upper(): p for p in output.glob("*.baf")}
    texts = {}
    for name in existing:
        out = paths.get(Path(name).stem + ".BAF")
        if not out:
            raise VerificationError(f"WeiDU did not produce {name}")
        texts[name] = out.read_text(encoding="utf-8", errors="replace")
    return texts


def cut_checks(repo: Path, actors: list[dict]) -> list[dict]:
    lookup = {}
    for row in actors:
        key = (row["area"], f'{row["cre"]}@{row["x"]}@{row["y"]}')
        lookup.setdefault(key, []).append(row)
    checks = []
    for path in sorted((repo / "chriz-sod-remix/lib").glob("comp*_lists.tpa")):
        for area_name, key in CUT_RE.findall(path.read_text(encoding="utf-8")):
            matches = lookup.get((area_name.upper(), key.upper()), [])
            checks.append({"source": path.name, "area": area_name.upper(), "key": key.upper(),
                           "matches": len(matches), "indices": "|".join(str(r["index"]) for r in matches),
                           "schedules": "|".join(r["schedule_hex"] for r in matches),
                           "pass": int(len(matches) == 1 and not matches[0]["schedule_active"])})
    return checks


def run(args: argparse.Namespace) -> None:
    game, work, output = args.game.resolve(), args.work.resolve(), args.output.resolve()
    for target in (work, output):
        if target == game or game in target.parents:
            raise VerificationError("audit outputs must be outside the read-only game directory")
    if work.exists():
        raise VerificationError("--work must be fresh; choose a new directory to prevent stale decompiles")
    work.mkdir(parents=True)
    output.mkdir(parents=True, exist_ok=True)
    store = AuditStore(game, work)
    log_path = game / "WeiDU.log"
    log_before = log_path.read_bytes()
    key_before = (game / "chitin.key").read_bytes()
    historical = {row["area"].upper(): row for row in csv.DictReader(args.dataset.open(encoding="utf-8-sig"))}
    names = sorted(set(historical) | {Path(n).stem for n in store.names("ARE") if n.startswith("BD")})
    area_rows, actors, spawns, rests, regions, cre_rows, cre_items = [], [], [], [], [], [], []
    cre_cache, scripts, missing_scripts = {}, set(), set()

    def add_script(name: str) -> None:
        if name and name.upper() != "NONE":
            scripts.add(name.upper() + ".BCS")

    def get_cre(name: str, raw: bytes | None = None) -> dict:
        name = name.upper()
        if name in cre_cache:
            return cre_cache[name]
        if raw is None and not store.exists(name + ".CRE"):
            result = {"cre_key": name, "cre_status": "missing_or_spawn_group"}
        else:
            raw = raw if raw is not None else store.read_bytes(name + ".CRE")
            parsed = creature(raw)
            for slot in CRE_SCRIPTS:
                add_script(parsed[f"cre_{slot}"])
            for item in parsed.pop("items"):
                cre_items.append({"cre_key": name, **item})
            result = {"cre_key": name, "cre_status": "ok", "cre_sha256": digest(raw), **parsed}
        cre_cache[name] = result
        cre_rows.append(result)
        return result

    for name in names:
        resource = name + ".ARE"
        if not store.exists(resource):
            area_rows.append({"area": name, "historical_name": historical.get(name, {}).get("name", ""), "status": "missing"})
            continue
        raw = store.read_bytes(resource)
        parsed = area(raw, name)
        for actor in parsed["actors"]:
            embedded = actor["embedded_size"]
            cre_key = f'{name}:ACTOR:{actor["index"]}' if embedded else actor["cre"]
            cre_raw = raw[actor["embedded_offset"]:actor["embedded_offset"] + embedded] if embedded else None
            actor.update(get_cre(cre_key, cre_raw))
            for slot in ACTOR_SCRIPTS:
                add_script(actor[f"actor_{slot}"])
            actors.append(actor)
        for spawn in parsed["spawn_points"]:
            for cre in spawn["table"].split("|"):
                if cre:
                    get_cre(cre)
        for cre in parsed["rest"].get("table", "").split("|"):
            if cre:
                get_cre(cre)
        for region in parsed["regions"]:
            add_script(region["script"])
        add_script(parsed["script"])
        spawns.extend(parsed["spawn_points"])
        rests.append(parsed["rest"])
        regions.extend(parsed["regions"])
        active = [a for a in parsed["actors"] if a["schedule_active"]]
        area_rows.append({"area": name, "historical_name": historical.get(name, {}).get("name", ""),
                          "status": "ok", "in_historical_dataset": int(name in historical),
                          "area_script": parsed["script"], "flags_hex": parsed["flags_hex"], "type_hex": parsed["type_hex"],
                          "actors_total": len(parsed["actors"]), "actors_scheduled": len(active),
                          "actors_schedule_zero": len(parsed["actors"]) - len(active),
                          "ea255_scheduled": sum(a.get("ea") == 255 for a in active),
                          "ea_ge200_scheduled_not_dead": sum(a.get("ea", 0) >= 200 and not a.get("state_dead", 0) for a in active),
                          "scheduled_dead_state": sum(a.get("state_dead", 0) for a in active),
                          "scheduled_kill_xp_sum": sum(a.get("kill_xp", 0) for a in active),
                          "actors_cre_missing": sum(a["cre_status"] != "ok" for a in parsed["actors"]),
                          "spawn_points": len(parsed["spawn_points"]),
                          "spawn_points_configured_scheduled": sum(s["configured_and_scheduled"] for s in parsed["spawn_points"]),
                          "regions": len(parsed["regions"]), "rest_configured": parsed["rest"].get("configured", 0),
                          "rest_has_bdnorest": parsed["rest"].get("has_bdnorest", 0), "are_sha256": digest(raw)})

    checks = cut_checks(args.repo, actors)
    for filename, rows in (("areas.csv", area_rows), ("actors.csv", actors), ("spawn_points.csv", spawns),
                           ("rest.csv", rests), ("regions.csv", regions), ("cutlist_checks.csv", checks)):
        write_csv(output / filename, rows)
    write_csv(output / "creatures.csv", cre_rows)
    write_csv(output / "cre_items.csv", cre_items)
    print(f"Core census ready: {len(area_rows)} areas, {len(actors)} actors, {len(spawns)} spawn points -> {output}", flush=True)

    scripts |= {name for name in store.names("BCS") if name.startswith("BD")}
    missing_scripts |= {s for s in scripts if not store.exists(s)}
    print(f"Decompiling {len(scripts) - len(missing_scripts)} effective BCS resources", flush=True)
    texts = decompile(store, scripts, work / "baf")
    # One hop supplies current CRE metadata for direct literal creation calls in
    # the selected corpus, including templates absent from the placed census.
    for text in texts.values():
        for call in creation_calls(text):
            if call["reference_kind"] == "cre":
                get_cre(call["cre_or_group"])
    extra = {name for name in scripts - texts.keys() if store.exists(name)}
    if extra:
        print(f"Decompiling {len(extra)} scripts assigned to directly created CRE templates", flush=True)
        texts.update(decompile(store, extra, work / "baf-created-cre"))
    missing_scripts |= {s for s in scripts if not store.exists(s)}
    calls, script_rows = [], []
    for script, text in sorted(texts.items()):
        hits = creation_calls(text)
        script_rows.append({"script": script, "lines": len(text.splitlines()), "create_calls": len(hits),
                            "decompiled_sha256": digest(text.encode("utf-8")),
                            "corpus": "baf" if (work / "baf" / (Path(script).stem + ".baf")).exists() else "baf-created-cre"})
        for call in hits:
            calls.append({"script": script, **call,
                          "cre_available": int(store.exists(call["cre_or_group"] + ".CRE")) if call["reference_kind"] == "cre" else ""})
    for row in area_rows:
        text = texts.get(row.get("area_script", "") + ".BCS", "")
        row["area_script_literal_create_calls"] = len(creation_calls(text))
    for filename, rows in (("areas.csv", area_rows), ("creatures.csv", cre_rows), ("cre_items.csv", cre_items),
                           ("scripts.csv", script_rows), ("create_calls.csv", calls),
                           ("resources.csv", sorted(store.records.values(), key=lambda r: r["resource"]))):
        write_csv(output / filename, rows)

    changed = [name for name, row in store.records.items()
               if digest(store.materialize(name).read_bytes()) != row["sha256"]]
    log_after, key_after = log_path.read_bytes(), (game / "chitin.key").read_bytes()
    if changed or log_after != log_before or key_after != key_before:
        raise VerificationError(f"source changed during census; outputs are not a coherent snapshot: {changed}")
    log_lines = [line for line in log_before.decode("utf-8", "replace").splitlines() if line.startswith("~")]
    tp2 = game / "chriz-sod-remix/setup-chriz-sod-remix.tp2"
    source_version = re.search(r'^VERSION\s+~([^~]+)~', tp2.read_text(encoding="utf-8"), re.M).group(1) if tp2.exists() else "unavailable"
    git = subprocess.run(["git", "rev-parse", "HEAD"], cwd=args.repo, capture_output=True, text=True, check=True).stdout.strip()
    snapshot = {"utc": datetime.now(timezone.utc).isoformat(), "game": str(game), "repo_commit": git,
                "tool_sha256": digest(Path(__file__).read_bytes()), "weidu_sha256": digest(store.weidu.read_bytes()),
                "weidu_log_sha256": digest(log_before), "chitin_key_sha256": digest(key_before),
                "weidu_log_sha256_after": digest(log_after), "chitin_key_sha256_after": digest(key_after),
                "historical_dataset_sha256": digest(args.dataset.read_bytes()), "source_tree_tp2_version": source_version,
                "weidu_entries": len(log_lines), "last_entry": log_lines[-1],
                "remix_entries": [line for line in log_lines if "CHRIZ-SOD-REMIX" in line.upper()],
                "source_stable_at_end": True, "decompile_work_directory": str(work),
                "areas": len(area_rows), "historical_areas": len(historical),
                "missing_areas": [r["area"] for r in area_rows if r["status"] != "ok"],
                "actors": len(actors), "actors_scheduled": sum(a["schedule_active"] for a in actors),
                "actors_unscheduled": sum(not a["schedule_active"] for a in actors),
                "spawn_points": len(spawns), "spawn_points_configured_scheduled": sum(s["configured_and_scheduled"] for s in spawns),
                "rest_headers": len(rests), "rest_configured": sum(r.get("configured", 0) for r in rests),
                "creatures": len(cre_rows), "missing_cre_or_group": sorted(r["cre_key"] for r in cre_rows if r["cre_status"] != "ok"),
                "decompiled_scripts": len(texts), "missing_assigned_scripts": sorted(missing_scripts),
                "literal_create_calls": len(calls), "cutlist_checks": len(checks), "cutlist_failures": sum(not c["pass"] for c in checks),
                "creation_action_counts": dict(sorted(Counter(c["action"] for c in calls).items())),
                "group_creation_calls": sum(c["reference_kind"] == "group" for c in calls),
                "unhandled_creation_signatures": [],
                "cutlist_results": {source: {"total": sum(c["source"] == source for c in checks),
                                            "pass": sum(c["pass"] for c in checks if c["source"] == source)}
                                    for source in sorted({c["source"] for c in checks})},
                "format_sources": ["https://gibberlings3.github.io/iesdp/file_formats/ie_formats/are_v1.htm",
                                   "https://gibberlings3.github.io/iesdp/file_formats/ie_formats/cre_v1.htm"]}
    (output / "snapshot.json").write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: snapshot[k] for k in ("areas", "actors", "actors_scheduled", "actors_unscheduled", "spawn_points", "decompiled_scripts", "cutlist_checks", "cutlist_failures", "source_stable_at_end")}), flush=True)


def main() -> None:
    repo = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game", required=True, type=Path)
    parser.add_argument("--work", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=repo / "docs/research/issue16")
    parser.add_argument("--dataset", type=Path, default=repo / "docs/research/sod_areas_dataset.csv")
    parser.add_argument("--repo", type=Path, default=repo)
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
