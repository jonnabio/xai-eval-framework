# Windows Worker Instructions

Use [docs/guides/WINDOWS_MULTI_WORKER_GUIDE.md](d:/Github/xai-eval-framework/docs/guides/WINDOWS_MULTI_WORKER_GUIDE.md) as the source of truth for adding or rehydrating a Windows worker node.

This repository already includes the Windows worker scripts:
- `scripts/managed_runner.ps1`: experiment worker/orchestrator
- `scripts/auto_push.ps1`: periodic results checkpoint sync
- `scripts/status_dashboard.ps1`: Windows terminal dashboard

If you are instructing another Windows machine through an LLM prompt, tell it to follow:

- [WINDOWS_MULTI_WORKER_GUIDE.md](d:/Github/xai-eval-framework/docs/guides/WINDOWS_MULTI_WORKER_GUIDE.md)

That guide contains:
- prerequisites
- environment setup
- model artifact validation
- safe launch commands
- dashboard monitoring commands
- troubleshooting notes for stalled or noisy workers
