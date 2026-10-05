# Reviewing the GitHub submission

The repository is the complete public reproducibility package. Start with the root README, the Markdown empirical report, AI-use disclosure and DATA_ACCESS.md. Relative figure links in the report point to the aggregate images under results/.

## Download or clone

Use the repository's **Code → Download ZIP** action and extract it, or clone the repository. Open a terminal in the extracted repository folder. Obtain authorized course Package 01 and place the unchanged input at `01_DID/data/public.csv` as described in DATA_ACCESS.md.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe run_all.py --data "01_DID\data\public.csv"
```

For the clickable interface, start `.\.venv\Scripts\python.exe local_app.py` and visit the local address printed in that terminal. The GitHub repository hosts files; it does not itself execute the Python analysis or host the local browser page.

Run the workflow before checking its manifest in a new checkout. Four required processed datasets are intentionally excluded from public distribution and must be regenerated from authorized inputs. Bundled workflow records retain the paths and environment of their original run and are historical evidence, not a claim that the new checkout has already been run.

`.gitattributes` disables automatic line-ending conversion so downloads and clones preserve the exact source and aggregate-output bytes. This supports checksum comparisons across machines; it does not guarantee identical generated graphics across library versions.

## Commit history

Git tracking began after the empirical implementation had already been completed. The first commit imports that verified snapshot explicitly. Subsequent commits record actual reviewer-documentation, packaging and publication checks performed from that point onward. These commits do not reconstruct or backdate earlier work. The chronological AI-use log documents earlier activities separately.

## Access and submission

The intended teaching-team submission is the repository URL. Raw and store-level data are not included publicly. Confirm authorized input access and any separate private processed-data delivery with the teaching team. Repository publication, anonymous access and actual remote download checks must be verified before claiming these steps complete.
