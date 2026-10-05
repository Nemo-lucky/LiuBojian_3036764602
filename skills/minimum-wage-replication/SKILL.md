---
name: minimum-wage-replication
description: "Run or explain the ECO6067 Card and Krueger minimum wage replication and ownership extension using an existing Python project and course public.csv. Use for 最低工资论文复现、所有权拓展、检查表图 or interpreting this project results; not for arbitrary papers or new causal designs."
---

# Minimum wage replication and ownership extension

Turn a natural-language request into a checked run of the existing analysis, or a grounded explanation of its current outputs. Answer in the user's language. The skill supplies instructions to an AI agent; the Python project supplies the calculations. A plain terminal cannot execute a natural-language prompt or a SKILL.md file.

## Resolve the requested task and inputs

- For “复现全部结果”, “生成表图” or an explicit rerun, execute the full workflow below.
- For “解释结果”, “检查工作流是否成功” or a named existing table, inspect and explain existing outputs first. Do not rerun merely to answer a question. A requested single stage can use its existing run_table2.py, run_figure1.py, run_table3.py, run_table4.py or run_extension.py entry point.
- Use the user's supplied project path, then the active project directory if it contains run_all.py and src/course_data.py. A portable copy of this skill at project/skills/minimum-wage-replication can also identify its enclosing project. An installed skill must not assume the creator's Desktop path. If no project is established, ask for the project folder; the skill alone is not the analysis package.
- Use an explicit data path when supplied. Otherwise inspect the two documented locations: project/01_DID/data/public.csv, then project.parent/data/public.csv. If both exist and differ, ask which input to use. If neither exists, request its location; do not invent data or silently substitute another archive.

## Execute the existing workflow

1. Read the project's README and requirements files. Establish a Python interpreter: prefer an existing project .venv, then the interpreter already used successfully for this project. Check required modules before installing anything. If setup is needed, create a project-local virtual environment and use requirements-lock.txt when available, otherwise requirements.txt. Use the environment's normal permission mechanisms for installation/network access; do not change system Python or execution policy.
2. From the project directory, invoke the selected interpreter with run_all.py --data followed by the resolved CSV path. Quote paths using the host's shell rules. The fixed analytical sequence is Table 2, Figure 1, Table 3, Table 4, ownership extension. Reuse the existing implementations; do not generate replacement regressions from memory.
3. Follow the exit code and results/workflow_run.json. On failure, inspect its error and logs/workflow.log. Fix a demonstrated path or dependency issue when authorized and retry after that correction; do not cycle through models or alter data to obtain a successful or significant result. A scientific/code change outside the requested reproduction needs to be identified as such. Never claim completion from partial outputs.
4. For a successful full run, execute this skill's scripts/summarize_run.py with --project and --data using the resolved paths. It verifies recorded hashes of the current analytical sources and outputs, reads numeric results, and checks the current input checksum. Its return code must be zero before claiming all recorded files are intact. Read the stage reports for explanations; summary JSON alone is not a causal assessment.

The ordinary runner command in a Windows desktop project is:

```powershell
python run_all.py --data "..\data\public.csv"
```

An installed skill's helper is resolved relative to this SKILL.md directory, not relative to the user's project. With a known interpreter, its arguments are:

```text
scripts/summarize_run.py --project PROJECT_FOLDER --data CSV_PATH
```

For a single-stage request, state that only that stage was executed. Its rerun can make an earlier all-stage manifest stale; do not relabel the full run as verified. For explanation-only requests, if the helper reports stale hashes, explain what is stale and use clearly labeled available results or ask whether to refresh; do not silently rerun.

## Explain and deliver

Read [references/interpretation.md](references/interpretation.md) when interpreting estimates, discrepancies or statistical significance. Preserve the distinction between the Table 4 reproduction's conventional SE and the extension's store-level HC3 SE.

Report the operation performed, actual sample sizes, calculation status, relevant publication differences and output locations. For a full run, summarize the paired employment DID, Table 4 NJ estimates, and the primary ownership interaction with its interval and approximate p value from generated CSVs. Cite the corresponding local result files. Do not use the reference's historical numbers as current results.

Show users how to inspect the generated table reports and figures. View generated figures when checking presentation; no image generation is needed. If runtime supports opening files, open the most relevant report or figure. The skill does not automatically revise the narrative Word report, create Git history, publish a repository, submit coursework, or message others.

Raw inputs are preserved. Course raw and store-level processed data stay out of public distribution; aggregate outputs and documentation may be shared. Computation checks, integrity checks and matching printed cells are separate from causal assumptions. Never claim an insignificant ownership interaction proves equal effects or a positive coefficient establishes a universally beneficial policy.
