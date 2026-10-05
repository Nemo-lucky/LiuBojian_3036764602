# Reusable minimum wage replication workflow

## Purpose and scope

Reconstruct Card and Krueger Tables 2–4 and Figure 1, then test restaurant ownership heterogeneity. `run_all.py` is a reusable command-line workflow, not an installed AI skill. It generates analytical results and stage reports; it does not regenerate or edit the narrative Word report.

## Input contract

Use the unmodified course Package 01 `public.csv`: 410 rows, 46 columns, numeric source values and missing entries preserved. Retain `01_DID/data/public.csv` within the project, or pass an explicit path. The existing desktop arrangement is also supported by `--data "../data/public.csv"` from `01_DID/Table2_Python`.

No author archive is required for the main workflow. If `data/raw/author/public.dat` and its `codebook` are present, Table 2 additionally compares them with the course input. Their absence is reported as a skipped optional comparison, not a calculation failure.

## Setup and execution

Python 3.10 or later is required. The clean validation uses the precise Python and Windows versions recorded in `docs/clean_reproduction_validation.json`; it is not a test of every platform.

Windows PowerShell, from the project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe run_all.py --data "01_DID\data\public.csv"
```

`requirements.txt` provides compatible version ranges. `requirements-lock.txt` pins the versions installed in the successful clean validation, including transitive dependencies. Installing into a new virtual environment avoids relying on the student's existing packages. Activation is optional, and no change to PowerShell execution policy is required.

## Stages and outputs

| Order | Stage | Inputs and sample | Main outputs |
|---|---|---|---|
| 1 | Table 2 | Variable-specific available records; wage indicators use all stores | Descriptive statistics, denominators and publication audits |
| 2 | Figure 1 | Valid starting wages by state and wave | PNG, SVG, interval counts and validation |
| 3 | Table 3 | Available means, paired changes and closure sensitivity | State and wage-group changes, samples, audits and validation |
| 4 | Table 4 | Common 357-store employment and wage sample with closure exception | Five models, all coefficients, author-SAS alternative and audits |
| 5 | Ownership extension | Primary 357-store sample; 384-store employment sensitivity | Ownership interactions, HC3 intervals, figures and validation |

The input loader verifies dimensions, required variables, category codes, nonnegative employment and the observed `(state, sheet)` key. Source row order is retained. Missing employment components remain missing; permanent closures have zero follow-up employment; temporary closures stay missing except in the separately labeled Table 3 sensitivity.

## Validation and failure behavior

Before analysis, the workflow checks the interpreter, package versions, CSV validity and SHA-256 checksum. It runs each stage with the same interpreter and records its detailed output in local `logs/workflow.log`.

A stage must exit successfully and regenerate every declared nonempty output. The first failure stops the workflow with a nonzero exit status. `results/workflow_run.json` and `workflow_summary.md` are marked failed so that an old success cannot be mistaken for the current attempt. Already completed output files may remain after a failure; they are not evidence of full completion.

On success, all stage validations pass, all declared files are regenerated and the raw input checksum is unchanged. The run manifest records environment versions, source hashes and output hashes. Original-publication mismatches are still disclosed: Table 2 82/88, Table 3 66/80, Table 4 16/18; exact Figure 1 bars are unverified. This status does not certify causal identification.

## Interpretation rules

Keep the Table 4 paper-note model and its author-code fifth-model alternative separate. Table 3's unbalanced-row SE is a transparent reconstruction, not a verified original algorithm. The ownership extension's primary interaction and all supplementary specifications are reported, including non-significant results. Store-level HC3 does not handle arbitrary common state shocks with only two states.

## Data access and delivery

Do not publish course input files or restricted course download links. `01_DID/`, `data/raw/`, `data/processed/`, `.venv/` and local logs are excluded from Git. Four store-level processed CSVs are generated automatically and may be supplied to the teaching team through a permitted access route or reproduced from their course input. Public aggregate figures, tables, audits, code and documentation can be distributed with the repository.

Before submission, confirm the teaching team can access the required input and GitHub repository. The project still needs a reviewed final report and real Git history; this workflow does not create either automatically.

## Companion AI skill

`skills/minimum-wage-replication/SKILL.md` adds natural-language task routing, input resolution, execution, integrity verification and interpretation around this runner. The root Chinese skill guide explains personal installation and usage. The runner remains the deterministic analytical engine.

## Local operation page

Run `python local_app.py` or the Windows launcher to open the Chinese local interface. It reuses this analytical workflow and the packaged skill integrity helper. Choosing a CSV keeps a local copy under ignored logs/ui_inputs. The page exposes aggregate results only and requires no AI account. Failure and changed inputs do not display prior results as a newly verified success. See the root Chinese page guide and docs/local_page_validation.json.
