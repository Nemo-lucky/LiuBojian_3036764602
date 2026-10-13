"""Read-only integrity check and numeric summary of an existing full workflow run."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import sys


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def within(root, relative):
    path = (root/relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f'Recorded path escapes project: {relative}')
    return path


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


def one(rows, **criteria):
    selected = [r for r in rows if all(r.get(k) == v for k, v in criteria.items())]
    if len(selected) != 1:
        raise ValueError(f'Expected one numeric record for {criteria}, found {len(selected)}')
    return selected[0]


def number(row, key):
    value = float(row[key])
    if not math.isfinite(value):
        raise ValueError(f'Nonfinite estimate: {key}')
    return value


def summarize(root, data=None):
    manifest_path = root/'outputs/tables/workflow_run.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('status') != 'success':
        raise ValueError(f"Full workflow is not successful: {manifest.get('status')}; {manifest.get('error', '')}")
    expected = ['Table 2', 'Figure 1', 'Table 3', 'Table 4', 'Ownership extension']
    stages = manifest.get('stages', [])
    if [s.get('name') for s in stages] != expected or any(s.get('status') != 'passed' for s in stages):
        raise ValueError('Full five-stage completion is not recorded')
    checked = 0
    for stage in stages:
        for output in stage['outputs']:
            path = within(root, output['path'])
            if not path.is_file() or digest(path) != output['sha256']:
                raise ValueError(f"Output missing or changed since recorded run: {output['path']}")
            checked += 1
    if checked != manifest.get('generated_output_count') or checked != manifest.get('expected_output_count'):
        raise ValueError('Manifest output counts disagree')
    for relative, checksum in manifest.get('source_sha256', {}).items():
        path = within(root, relative)
        if not path.is_file() or digest(path) != checksum:
            raise ValueError(f'Source changed since recorded run: {relative}')
    if not manifest.get('source_sha256'):
        raise ValueError('Source hashes absent from run record')
    if manifest.get('raw_input_unchanged') is not True:
        raise ValueError('Run did not confirm unchanged raw input')
    input_now_checked = False
    if data is not None:
        if not data.is_file() or digest(data) != manifest['input_sha256']:
            raise ValueError('Provided input differs from the recorded run')
        input_now_checked = True
    results = root/'outputs/tables'
    t3 = one(read_csv(results/'table3_numeric.csv'), row='4', column='NJ-PA')
    t4 = read_csv(results/'table4_numeric.csv')
    nj0 = one(t4, model='i')
    nj1 = one(t4, model='ii')
    primary = one(read_csv(results/'extension_ownership_effects.csv'),
                  model='NJ_brands_primary', contrast='company_minus_franchise')
    audits = {}
    for name, filename, field in [('Table 2', 'table2_audit_cells.csv', 'matches'),
                                  ('Table 3', 'table3_audit_cells.csv', 'matches'),
                                  ('Table 4', 'table4_audit_cells.csv', 'match_at_precision')]:
        rows = read_csv(results/filename)
        audits[name] = {'matched': sum(r[field].strip().lower() == 'true' for r in rows), 'checked': len(rows)}
    extension = {key: number(primary, key) for key in ['estimate', 'se_hc3', 'ci95_low', 'ci95_high', 'p']}
    return {'status': 'verified', 'mode': 'read_only_existing_full_run',
            'files_hash_checked': checked, 'analytical_sources_hash_checked': True,
            'recorded_input_unchanged': True, 'current_input_hash_checked': input_now_checked,
            'run_finished_utc': manifest.get('finished_utc'), 'environment': manifest.get('environment'),
            'paired_did': {'estimate': number(t3, 'estimate'), 'se': number(t3, 'se')},
            'table4_n': int(nj0['n']),
            'table4_nj_no_controls': {'estimate': number(nj0, 'estimate'), 'se': number(nj0, 'se')},
            'table4_nj_controls': {'estimate': number(nj1, 'estimate'), 'se': number(nj1, 'se')},
            'primary_ownership_difference': extension,
            'publication_audits_from_current_csvs': audits,
            'interpretation': 'Insufficient evidence of ownership difference' if extension['p'] >= .05
                              else 'Ownership difference under conditional store-level HC3 inference',
            'limitations': ['Only two states; HC3 does not handle arbitrary state-level dependence.',
                            'Publication discrepancies remain; exact original Figure 1 bars unverified.',
                            'Integrity checks do not establish causal assumptions.']}


def main():
    parser = argparse.ArgumentParser(description='Verify current full-run files and summarize numeric results')
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--data', type=Path, help='Optional CSV path for checking its current hash')
    args = parser.parse_args()
    try:
        summary = summarize(args.project.expanduser().resolve(),
                            args.data.expanduser().resolve() if args.data is not None else None)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({'status': 'not_verified', 'error': str(error)}, ensure_ascii=False, indent=2))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
