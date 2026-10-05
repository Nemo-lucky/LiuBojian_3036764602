"""Run all assigned replications and the ownership extension from one CSV.

Uses the current interpreter; never installs dependencies or edits raw inputs.
Each analysis stage keeps its own validation and documented publication gaps.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib
from importlib import metadata
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
STAGES = [
    ('Table 2', '02_table2.py', [
        'results/table2_numeric.csv', 'results/table2_replication.md',
        'results/table2_wage_denominators.csv', 'results/table2_audit_cells.csv',
        'results/table2_t_method_checks.csv', 'results/table2_audit_中文.md',
        'data/processed/course_analysis.csv', 'docs/course_data_validation.json']),
    ('Figure 1', '03_figure1.py', [
        'results/figure1.png', 'results/figure1.svg', 'results/figure1_bin_counts.csv',
        'results/figure1_sample_checks.csv', 'results/figure1_validation.json',
        'results/figure1_中文说明.md']),
    ('Table 3', '04_table3.py', [
        'results/table3_numeric.csv', 'results/table3_audit_cells.csv',
        'results/table3_samples.csv', 'results/table3_replication.md',
        'results/table3_validation.json', 'data/processed/table3_analysis.csv']),
    ('Table 4', '05_table4.py', [
        'results/table4_numeric.csv', 'results/table4_all_coefficients.csv',
        'results/table4_audit_cells.csv', 'results/table4_author_sas_comparison.csv',
        'results/table4_sample_flow.csv', 'results/table4_validation.json',
        'results/table4_replication.md', 'data/processed/table4_analysis.csv']),
    ('Ownership extension', '06_extension_ownership.py', [
        'results/extension_ownership_effects.csv', 'results/extension_ownership_groups.csv',
        'results/extension_ownership_coefficients.csv', 'results/extension_ownership_brand_counts.csv',
        'results/extension_ownership_changes.png', 'results/extension_ownership_changes.svg',
        'results/extension_ownership_effects.png', 'results/extension_ownership_effects.svg',
        'results/extension_ownership_validation.json', 'results/extension_ownership_report.md',
        'data/processed/extension_ownership_analysis.csv']),
]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_path(explicit):
    if explicit is not None:
        path = explicit.expanduser().resolve()
    else:
        candidates = [ROOT/'01_DID'/'data'/'public.csv', ROOT.parent/'data'/'public.csv']
        path = next((p for p in candidates if p.is_file()), candidates[0])
    if not path.is_file():
        raise ValueError('Input CSV not found. Use --data with the path to Package 01 public.csv.')
    return path


def environment():
    if sys.version_info < (3, 10):
        raise ValueError('Python 3.10 or newer is required.')
    versions = {}
    bounds = {'pandas': ((2, 2), (4, 0)), 'numpy': ((1, 26), (3, 0)),
              'matplotlib': ((3, 8), (4, 0)), 'scipy': ((1, 11), (2, 0))}
    for name, (lower, upper) in bounds.items():
        try:
            module = importlib.import_module(name)
            version = metadata.version(name)
            release = tuple(int(x) for x in version.split('.')[:2])
            if not lower <= release < upper:
                raise ValueError(f'{name} {version} is outside requirements.txt bounds')
            versions[name] = version
        except (ImportError, metadata.PackageNotFoundError) as error:
            raise ValueError(f'Dependency {name} unavailable. Run: python -m pip install -r requirements.txt') from error
        if not getattr(module, '__file__', None):
            raise ValueError(f'{name} could not be loaded completely')
    return {'python': platform.python_version(), 'platform': platform.platform(), 'packages': versions}


def main():
    parser = argparse.ArgumentParser(description='Generate Tables 2–4, Figure 1 and ownership extension')
    parser.add_argument('--data', type=Path, help='Package 01 CSV; relative paths resolve from your terminal folder')
    args = parser.parse_args()
    results = ROOT/'results'
    results.mkdir(exist_ok=True)
    # Write a running/failed state immediately so a prior success is not mistaken
    # for the current run. Existing aggregate outputs are overwritten by stages.
    manifest_path = results/'workflow_run.json'
    manifest = {'status': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(),
                'stages': [], 'expected_output_count': sum(len(s[2]) for s in STAGES)}
    log = None
    try:
        path = input_path(args.data)
        env = environment()
        sys.path.insert(0, str(ROOT/'src'))
        from course_data import load_course
        raw, _ = load_course(path)  # Preflight input validation before any stage.
        initial_hash = sha256(path)
        manifest.update(input_filename=path.name, input_sha256=initial_hash,
                        input_shape=list(raw.shape), environment=env,
                        source_sha256={f'src/{script}': sha256(ROOT/'src'/script) for _, script, _ in STAGES})
        manifest['source_sha256']['src/course_data.py'] = sha256(ROOT/'src'/'course_data.py')
        manifest['source_sha256']['src/audit_table2.py'] = sha256(ROOT/'src'/'audit_table2.py')
        manifest['source_sha256']['run_all.py'] = sha256(Path(__file__))
        logs = ROOT/'logs'
        logs.mkdir(exist_ok=True)
        log_path = logs/'workflow.log'
        log = log_path.open('w', encoding='utf-8')
        print(f'Input validated: {raw.shape[0]} restaurants, {raw.shape[1]} columns.')
        print('Running five analysis stages with the current Python environment.')
        for index, (label, script, outputs) in enumerate(STAGES, 1):
            print(f'[{index}/5] {label} ...', flush=True)
            start = time.time()
            log.write(f'\n[{index}/5] {label}\n'); log.flush()
            completed = subprocess.run([sys.executable, str(ROOT/'src'/script), '--data', str(path)],
                                       cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
            if completed.returncode != 0:
                raise RuntimeError(f'{label} failed (exit {completed.returncode}); see logs/workflow.log')
            verified = []
            for relative in outputs:
                target = ROOT/relative
                if not target.is_file() or target.stat().st_size == 0:
                    raise RuntimeError(f'{label} did not produce required output: {relative}')
                if target.stat().st_mtime < start-1:
                    raise RuntimeError(f'{label} output was not regenerated: {relative}')
                verified.append({'path': relative, 'sha256': sha256(target), 'bytes': target.stat().st_size})
            manifest['stages'].append({'name': label, 'status': 'passed',
                                       'seconds': round(time.time()-start, 3), 'outputs': verified})
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
            print(f'      Passed; {len(outputs)} outputs regenerated.', flush=True)
        if sha256(path) != initial_hash:
            raise RuntimeError('Raw input checksum changed during workflow')
        manifest.update(status='success', finished_utc=datetime.now(timezone.utc).isoformat(),
                        raw_input_unchanged=True, generated_output_count=sum(len(s['outputs']) for s in manifest['stages']),
                        original_publication_exact_match=False,
                        publication_audits={'Table 2': '82/88', 'Table 3': '66/80', 'Table 4': '16/18',
                                            'Figure 1': 'exact original bars not verified'})
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
        summary = ['# Unified workflow run', '', 'Status: success.',
                   f"Generated outputs: {manifest['generated_output_count']}.",
                   'Raw input unchanged: yes.', '',
                   'All five analysis stages and their embedded calculation checks passed.',
                   'Publication discrepancies remain documented; success does not mean exact replication or causal validation.', '',
                   'Main results: table2_replication.md; figure1.png; table3_replication.md; table4_replication.md; extension_ownership_report.md.',
                   'Logs: logs/workflow.log (local, Git ignored). Environment and output hashes: results/workflow_run.json.']
        (results/'workflow_summary.md').write_text('\n'.join(summary)+'\n', encoding='utf-8')
        print(f"Success: all 5 stages passed; {manifest['generated_output_count']} outputs regenerated; raw data unchanged.")
        print('See results/workflow_summary.md and results/workflow_run.json.')
        return 0
    except Exception as error:
        manifest.update(status='failed', finished_utc=datetime.now(timezone.utc).isoformat(), error=str(error))
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
        (results/'workflow_summary.md').write_text('# Unified workflow run\n\nStatus: failed.\n\n'+str(error)+'\n', encoding='utf-8')
        print(f'Workflow failed: {error}', file=sys.stderr)
        return 1
    finally:
        if log:
            log.close()


if __name__ == '__main__':
    raise SystemExit(main())
