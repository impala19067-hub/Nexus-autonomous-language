# Sapphire Industrial Readiness

This document separates working code from roadmap items. Claims in older marketing material are not proof of production readiness.

## Implemented and Testable

- Lexer, parser, and tree-walk interpreter: `sapphire_lang/src/`
- CLI execution with nonzero failure status: `sapphire_lang/src/cli.py`
- Workspace-confined file and subprocess sandbox: `sapphire_lang/src/industrial/sandbox.py`
- Transactional SQLite persistence with WAL: `sapphire_lang/src/industrial/persistence.py`
- Durable FTS5 retrieval-augmented memory: `sapphire_lang/src/industrial/memory.py`
- Bounded retry and recovery events: `sapphire_lang/src/industrial/agent_loop.py`
- AI-generated planning: `agent.planning.create_plan` parses validated JSON, fenced JSON, and numbered model responses into executable `PlanTask` objects.
- Regression and industrial tests: `sapphire_lang/tests/`
- Reproducible benchmark harness: `benchmarks/benchmark_runtime.py`
- Runnable applications: `apps/system_health_monitor.sp` and `apps/backup_manifest.sp`
- Windows packaged GUI builds and `.sp` file association: release artifacts

## Explicit Limitations and Planned Work

- The default interpreter is a tree-walk interpreter, not a native machine-code compiler.
- Distributed modules currently calculate plans and generate code; they do not execute a verified multi-node training job here.
- FTS5 retrieval is local lexical retrieval with context assembly. Neural embeddings and vector databases are planned, not claimed.
- The sandbox is a workspace and command allow-list boundary, not an OS-level security sandbox. Production isolation requires containers, job objects, or a dedicated service account.
- Agent loops are bounded and retry-aware, but do not yet provide durable distributed scheduling or human approval workflows. Planning falls back to one review task when every configured AI backend returns unusable output.
- Security results in this repository are regression checks, not an independent security audit.
- There is no independent user or external project validation included in this repository yet.

## Reproducible Release Procedure

1. Use the pinned Python version recorded by the build manifest.
2. Set `SOURCE_DATE_EPOCH` to the release commit timestamp.
3. Run `python build_reproducible.py`.
4. Archive the generated `release_manifest.json` and SHA-256 hashes with the GitHub release.
5. Run `python -m unittest discover -s sapphire_lang/tests -v` and `python benchmarks/benchmark_runtime.py`.

## Validation Commands

```powershell
python -m unittest discover -s sapphire_lang/tests -v
python benchmarks/benchmark_runtime.py
python security_audit.py
python sapphire_lang/src/cli.py run apps/system_health_monitor.sp
```
