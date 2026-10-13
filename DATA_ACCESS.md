# Data access and processed-data delivery

## Required course input

Obtain **ECO6067 Package 01** through the course's authorized download page. Access is restricted to teaching and coursework; neither the input nor the restricted download URL is redistributed here. The published assignment says access remains available through 22 October 2026, 23:59 Hong Kong time. Obtain and retain the authorized input before access closes.

Keep `01_DID`, `data` and `public.csv` unchanged. In the repository folder, use this layout:

```text
project/
  run_all.py
  01_DID/
    data/
      public.csv
```

The checked input has 410 restaurants and 46 columns; its SHA-256 is `45e6f4ac4928f7c9fcc2585a45e0467ecaa039f0b241f4c5a26cd290fd8e772b`. Do not edit it to match reported results. A local path can also be supplied using `--data` or selected in the local browser page. The current student's `../data/public.csv` layout is supported.

## Generate the final processed datasets

After installing the dependencies described in README, run:

```powershell
.\.venv\Scripts\python.exe run_all.py --data "01_DID\data\public.csv"
```

The workflow regenerates these four **store-level** files under `data/processed/`:

| File | Purpose |
|---|---|
| `course_analysis.csv` | Constructed variables used for descriptive replication and wages |
| `table3_analysis.csv` | Employment changes and Table 3 sample/closure definitions |
| `table4_analysis.csv` | Common regression sample, policy exposure and controls |
| `extension_ownership_analysis.csv` | Ownership extension sample and constructed variables |

These files derive from restricted course inputs and are excluded from the public package and Git. The legacy `initial_analysis.csv` is not a final-workflow dataset. Aggregate tables, figures, cell audits and documentation are included.

## Teaching-team review and separate delivery

The assignment requests the processed data used in the final analysis. Generation instructions document them but do not claim a separate transfer has already happened. Reviewers with authorized Package 01 access can reproduce all four files. If a separate processed-data submission is required, provide these four generated files directly through an authorized teaching-team channel; do not place them in a public GitHub repository. Confirm the team's input access and delivery arrangement before submission. No private transfer or access verification has yet been completed.

The optional author-hosted archive was acquired independently for a source comparison. See `docs/data_provenance.json`. It is not a substitute for the documented course input and is not bundled in the public package.


## Local processed-data package prepared

On 13 October 2026 the four final processed datasets were packaged locally in ECO6067_Processed_Data_PRIVATE.zip with row counts and SHA-256 hashes. The archive is excluded from public distribution and has not been transferred to the teaching team. A full final rerun and integrity check passed; see docs/final_content_validation.json. The authorized private delivery channel remains to be confirmed.
