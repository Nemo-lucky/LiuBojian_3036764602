# Minimum-wage replication and ownership extension

**Liu Bojian | 3036764602 | ECO6067 individual project**

This project reproduces Tables 2–4 and Figure 1 of Card and Krueger (1994) and tests whether the employment response differs by restaurant ownership. Liu Bojian is the sole student author. AI assistance is documented separately.

- [Final research report (PDF)](report.pdf)
- [Editable report source (Markdown)](report/ECO6067_Empirical_Report.md)
- [AI-use disclosure](AI_USE_DISCLOSURE.md)
- [Data access](DATA_ACCESS.md)
- [Submission checklist](SUBMISSION_CHECKLIST.md)

## Repository structure

```text
README.md
report.pdf
AI_USE_DISCLOSURE.md
requirements.txt
requirements-lock.txt
code/
  run_all.py
  run_table2.py, run_figure1.py, run_table3.py, run_table4.py, run_extension.py
  local_app.py
  src/                         analytical implementations
data/
  raw/README.md                authorized input placement instructions
  processed/README.md          four CSVs regenerated locally
outputs/
  tables/                     tables, numeric audits and run records
  figures/                    PNG and SVG figures
skills/
  SKILL.md
  scripts/summarize_run.py
  references/interpretation.md
  agents/openai.yaml
report/                       Markdown report and reading guide
docs/                         provenance and validation evidence
ui/                           English local-page assets
```

The layout follows the teaching team's example. Restricted raw and store-level processed data are not published. They are generated or supplied locally under the directories shown above.

## Reproduce all analytical results

Open a terminal at the repository root. Install Python and obtain authorized course Package 01. Extract it under `data/raw/`, preserving `01_DID/data/public.csv`.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe code/run_all.py --data "data/raw/01_DID/data/public.csv"
```

Alternatively, provide the existing course CSV location. In the student's desktop folder `01_DID/Table2_Python`:

```powershell
python code/run_all.py --data "..\data\public.csv"
```

Use the same interpreter for installation and execution. `requirements.txt` supplies broader supported version ranges; `requirements-lock.txt` records the tested environment. Python 3.10+ is required; the locked Windows environment was tested on Python 3.12.3. No activation or execution-policy change is necessary. Relative `--data` paths resolve from the terminal directory, not the script directory.

The single entry point validates 410 restaurants and 46 columns, executes five stages and confirms all 39 declared outputs are regenerated. It stops at the first failure and verifies that the original input hash remains unchanged. It does not require an AI account or network access after dependency installation. Without `--data`, it checks `data/raw/01_DID/data/public.csv`, `data/raw/public.csv`, the legacy `01_DID/data/public.csv`, then `../data/public.csv`.

## Inspect and verify results

- [Table 2](outputs/tables/table2_replication.md)
- [Figure 1](outputs/figures/figure1.png)
- [Table 3](outputs/tables/table3_replication.md)
- [Table 4](outputs/tables/table4_replication.md)
- [Ownership extension](outputs/tables/extension_ownership_report.md)
- [Current execution summary](outputs/tables/workflow_summary.md)

`outputs/tables/workflow_run.json` records the current environment and input/source/output hashes. Four store-level CSVs are generated in `data/processed/`; local logs are in `logs/workflow.log`.

```powershell
python skills/scripts/summarize_run.py --project . --data "data/raw/01_DID/data/public.csv"
```

This read-only check must return `status: verified` and 39 checked outputs. It requires the locally regenerated processed files. Bundled aggregate outputs alone do not certify a new machine's execution. Single-stage runners in `code/` accept the same `--data` argument; rerunning one stage can make an earlier complete-run record stale.

## Findings and remaining publication differences

The paired-sample DID is 2.75 FTE. Table 4 uses 357 restaurants; its NJ estimates are 2.33 without controls and 2.30 with brand and ownership controls. The ownership interaction is about -0.94 FTE (HC3 SE 2.64; approximate 95% interval [-6.14, 4.25]; p=.721): insufficient evidence of different ownership responses, not proof of equal effects.

Publication audits match 82/88 cells in Table 2, 66/80 in Table 3 and 16/18 in the Table 4 paper-note specification. Figure 1's exact original bars remain unverified. The Table 4 author-SAS fifth model is exported separately. Calculation checks do not establish causal identification; one pre-policy wave and only two states limit inference.

## Local browser page and reusable AI skill

```powershell
.\.venv\Scripts\python.exe code/local_app.py
```

Or double-click `启动本地页面.bat`. The English page runs on the reviewer's own computer, accepts the course CSV, runs or verifies the same workflow, and displays aggregate outputs. See [LOCAL_PAGE.md](LOCAL_PAGE.md). Keep the server terminal open.

[skills/SKILL.md](skills/SKILL.md) gives reusable AI instructions for running, verifying and explaining this fixed project. To install it in a compatible agent, copy the contents of `skills/` into that agent's `minimum-wage-replication` skill folder. A reviewer can also ask an agent to read the repository's SKILL.md directly. The skill is optional for Python and browser execution.

## Validation history and current delivery status

The earlier layout passed a fresh-directory, fresh-virtual-environment check and an anonymous GitHub-clone check on this Windows host. Historical JSON evidence retains its original paths and dates. The reorganized layout is tested separately; see [layout validation](docs/layout_validation.json). No second-computer validation is claimed. Git tracking began after implementation; no retrospective commit history is claimed.

Current remote: https://github.com/Nemo-lucky/LiuBojian_3036764602 . The repository uses the required Name_StudentID format. Formal submission is tracked in the checklist. No collaborators were added during this revision.

## Sources

Card and Krueger (1994), American Economic Review 84(4), 772–793. [Published paper](https://davidcard.berkeley.edu/papers/njmin-aer.pdf), [author data page](https://davidcard.berkeley.edu/data_sets.html).

Course Package 01 is the analytical input. The optional author archive was independently compared with it; all numeric values and missing positions matched. See `docs/author_data_crosscheck_historical.json`. Reviewers need authorized course data access; see DATA_ACCESS.md. The narrative report is maintained separately from numerical output generation.

## Published layout verification

The renamed public repository and its reorganized submission were verified anonymously on 13 October 2026. Uploaded files matched local Git blob hashes, and direct PDF, README, runner and skill downloads matched their local files. See [delivery verification](docs/github_layout_delivery.json). No collaborator invitations or submission emails were sent.
