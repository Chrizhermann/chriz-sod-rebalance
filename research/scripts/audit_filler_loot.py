"""Read-only item/dependency screen for #16's travel arenas and mimic cave.

This lists resource inventories, not guaranteed player drops. Randomiser tokens,
undroppable items, script rewards, and alternative spawn branches require triage.
Raw extracted game resources stay in the explicitly supplied scratch directory.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from ending_save_evidence import checked, item, number, parse_cre, signature, text
from verify_ending import DecompiledResources, ResourceStore

AREAS = ('BD0060', 'BD0061', 'BD0062', 'BD0063', 'BD0064', 'BD0066', 'BD0067', 'BD1010')
# Additional creatures in the reviewed area-script branches. Branches are not
# summed: these rows describe each template's inventory once per area.
SCRIPTED = {
    'BD0062': ('JELLOC', 'BDMCARRI', 'BDOTYG01', 'BDOTYG02', 'BDCCRAW1'),
    'BD0064': ('BDURE4D', 'BDURE4E'),
    'BD1010': ('BDMIMIC', 'JELLOC', 'BDOTYG01', 'SPIDPH', 'SPIDPHAS'),
}
FIELDS = ('area', 'kind', 'source', 'placed_count', 'ea', 'xp_per_creature',
          'item', 'charges', 'flags', 'instance_undroppable')


def placed_creatures(raw: bytes) -> dict[str, dict]:
    """Return scheduled templates; embedded records never fall back to a CRE file."""
    signature(raw, b'AREAV1.0')
    checked(raw, 0, 0xC4)
    ao, ac = number(raw, 0x54), number(raw, 0x58, 'H')
    checked(raw, ao, ac * 0x110)
    creatures = {}
    for i in range(ac):
        b = ao + i * 0x110
        if not number(raw, b + 0x40) & 0xFFFFFF:
            continue
        ref = text(raw, b + 0x80, 8).upper()
        embedded_offset, embedded_size = number(raw, b + 0x88), number(raw, b + 0x8C)
        if embedded_size:
            if not embedded_offset:
                raise ValueError(f'actor {i} has null embedded CRE offset')
            embedded = checked(raw, embedded_offset, embedded_size)
            creatures[f'actor:{i}:{ref}'] = {'count': 1, 'embedded': embedded}
        elif ref:
            creatures.setdefault(ref, {'count': 0, 'embedded': None})['count'] += 1
        else:
            raise ValueError(f'scheduled actor {i} has neither external nor embedded CRE')
    return creatures


def container_rows(raw: bytes, area: str) -> list[dict]:
    signature(raw, b'AREAV1.0')
    checked(raw, 0, 0xC4)
    co, cc = number(raw, 0x70), number(raw, 0x74, 'H')
    io, ic = number(raw, 0x78), number(raw, 0x76, 'H')
    checked(raw, co, cc * 0xC0)
    checked(raw, io, ic * 20)
    rows = []
    for i in range(cc):
        b = co + i * 0xC0
        first, count = number(raw, b + 0x40), number(raw, b + 0x44)
        if first + count > ic:
            raise ValueError(f'{area} container {i} exceeds item table')
        for j in range(first, first + count):
            entry = item(raw, io + j * 20)
            rows.append(dict(area=area, kind='container', source=text(raw, b, 32),
                placed_count=1, ea='', xp_per_creature='', item=entry['resref'],
                charges='|'.join(map(str, entry['charges'])),
                flags=entry['flags'], instance_undroppable=bool(entry['flags'] & 8)))
    return rows


def run(game: Path, scratch: Path, output: Path, areas: tuple[str, ...] = AREAS) -> None:
    game, scratch, output = game.resolve(), scratch.resolve(), output.resolve()
    if scratch.is_relative_to(game) or output.is_relative_to(game):
        raise ValueError('audit output must be outside the game directory')
    scratch.mkdir(parents=True, exist_ok=False)
    output.mkdir(parents=True, exist_ok=True)
    store = ResourceStore(game, scratch)
    rows, resources, hashes = [], set(), {}
    log_before = (game / 'WeiDU.log').read_bytes()
    key_before = (game / 'chitin.key').read_bytes()
    embedded_hashes = {}

    def read(resource: str) -> bytes:
        data = store.read_bytes(resource)
        hashes[resource.upper()] = hashlib.sha256(data).hexdigest()
        return data

    for area in areas:
        raw = read(area + '.ARE')
        creatures = placed_creatures(raw)
        for ref in SCRIPTED.get(area, ()):
            creatures.setdefault(ref, {'count': 0, 'embedded': None})
        for ref, details in sorted(creatures.items()):
            count, embedded = details['count'], details['embedded']
            cre = read(ref + '.CRE') if embedded is None else embedded
            if embedded is not None:
                embedded_hashes[f'{area}:{ref}'] = hashlib.sha256(cre).hexdigest()
            parsed = parse_cre(cre)
            for offset in (0x248, 0x250, 0x258, 0x260, 0x268):
                script = text(cre, offset, 8)
                if script and script.upper() != 'NONE':
                    resources.add(script.upper() + '.BCS')
            dialog = text(cre, 0x2CC, 8)
            if dialog and dialog.upper() != 'NONE':
                resources.add(dialog.upper() + '.DLG')
            for entry in parsed['items']:
                rows.append(dict(area=area, kind='creature', source=ref,
                    placed_count=count, ea=number(cre, 0x270, 'B'),
                    xp_per_creature=number(cre, 0x14),
                    item=entry['resref'], charges='|'.join(map(str, entry['charges'])),
                    flags=entry['flags'], instance_undroppable=bool(entry['flags'] & 8)))
        rows.extend(container_rows(raw, area))
    existing = {r for r in resources if store.exists(r)}
    for resource in existing:
        read(resource)
    texts = DecompiledResources(store, scratch).decompile(existing)
    changed = [resource for resource, original in hashes.items()
               if hashlib.sha256(store.read_bytes(resource)).hexdigest() != original]
    log_after, key_after = (game / 'WeiDU.log').read_bytes(), (game / 'chitin.key').read_bytes()
    if changed or log_before != log_after or key_before != key_after:
        raise ValueError(f'source changed during loot screen: {changed}')
    target = output / 'travel-and-mimic-items.csv'
    with target.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    manifest = {'areas': areas, 'item_rows': len(rows), 'sha256': hashes,
                'dependency_resources': sorted(texts),
                'missing_dependencies': sorted(resources - existing),
                'embedded_cre_sha256': embedded_hashes,
                'utc': datetime.now(timezone.utc).isoformat(), 'game': str(game),
                'scratch': str(scratch), 'tool_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'weidu_log_sha256_before': hashlib.sha256(log_before).hexdigest(),
                'weidu_log_sha256_after': hashlib.sha256(log_after).hexdigest(),
                'chitin_key_sha256_before': hashlib.sha256(key_before).hexdigest(),
                'chitin_key_sha256_after': hashlib.sha256(key_after).hexdigest(),
                'source_stable_at_end': True,
                'scope': {'cre_inventory': 'scheduled placed templates, including corpses, plus the explicit additional templates below',
                          'container_inventory': 'all item instances in the selected effective ARE containers',
                          'decompiled_dependencies': 'five script slots and dialogue on the selected CRE templates only',
                          'additional_templates': {area: SCRIPTED.get(area, ()) for area in areas},
                          'excluded': ['automatic or recursive script-created CRE discovery', 'actor/area/region/container script overrides',
                                       'ITM drop flags and effects', 'stores and randomiser resolution', 'runtime inventory changes']}}
    (output / 'travel-loot-screen.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'csv': str(target), 'item_rows': len(rows), 'decompiled_dependencies': len(texts),
                      'missing_dependencies': sorted(resources - existing), 'source_stable_at_end': True}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game', type=Path, required=True)
    parser.add_argument('--scratch', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--areas', nargs='+', default=AREAS)
    args = parser.parse_args()
    run(args.game.resolve(), args.scratch.resolve(), args.output.resolve(),
        tuple(area.upper() for area in args.areas))
