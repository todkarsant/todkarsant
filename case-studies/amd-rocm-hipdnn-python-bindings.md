# AMD ROCm Contribution: hipDNN Python Graph Lifecycle and Plan APIs

**Repository:** [ROCm / rocm-libraries](https://github.com/ROCm/rocm-libraries)  
**Pull request:** [#15453 — feat(hipdnn/python): expose Graph lifecycle and plan APIs](https://github.com/ROCm/rocm-libraries/pull/15453)  
**Target branch:** `develop`  
**Author:** `todkarsant`

> **Status at profile update (17 November 2026):** A maintainer posted an approval (LGTM), while GitHub still reported the pull request as open. This case study therefore describes an approved upstream contribution, not a merged PR.

## 1. Context

The hipDNN Python frontend exposed only part of the underlying Graph functionality. Several existing C++ Graph operations and lifecycle capabilities were not available through the Python bindings.

The contribution extends the Python interface so users can inspect graph tensors, build graphs through a one-shot lifecycle API, serialize compiled plans and configure supported runtime shape overrides.

The change is part of the upstream hipDNN frontend; it does not implement new GPU kernels.

## 2. What I contributed

The pull request adds nine Python binding entry points:

| API | Purpose |
| :-- | :-- |
| `build()` | One-shot graph validation, operation-graph construction, plan creation and finalization |
| `checkTensorUidsSet()` | Validate tensor UID assignment |
| `getTensorsByUid()` | Inspect graph tensors through a UID-keyed mapping |
| `getTensorsByName()` | Inspect named graph tensors |
| `to_compiled_plan_binary()` | Serialize an active compiled execution plan |
| `from_compiled_plan_binary()` | Restore a compiled plan from binary data |
| `set_override_shape_enabled()` | Enable or disable supported runtime shape/stride override mode |
| `is_override_shape_enabled()` | Query the override-mode setting |
| `execute()` overload | Execute with runtime tensor shape and stride overrides |

The implementation includes Python-to-native handle conversion, variant-pack and workspace handling, byte serialization, argument definitions and API documentation.

## 3. Test coverage

The PR adds tests covering:

- UID validation and tensor mapping consistency.
- Graph build success and invalid-graph behaviour.
- Compiled-plan serialization and round-trip restoration.
- Shape-override configuration and state.
- Guard behaviour and an SDPA override execution path.

**Important test boundary:** The PR description marks GPU tests as requiring AMD GPU CI and SDPA override tests as requiring a build with `HIPDNN_ENABLE_SDPA`. Do not interpret the existence of these tests as proof that all GPU-specific paths passed in CI.

## 4. Review and iteration

The upstream review involved concrete engineering feedback, including:

- Addressing clang-tidy's `performance-no-int-to-ptr` finding.
- Correcting the documented order of graph build operations.
- Adding missing override-execution test coverage.
- Applying Black formatting.
- Rebasing after upstream changes and resolving conflicts while preserving the required API and test changes.

The latest visible review from the maintainer was **“LGTM! Thanks for all the updates!”** on 17 November 2026. GitHub still reported the PR as open at the time this case study was prepared.

## 5. Engineering relevance

This contribution demonstrates work in:

- Python bindings over a native C++ API.
- API surface design and compatibility considerations.
- Graph lifecycle and execution interfaces.
- Serialization and restoration of compiled plans.
- Test design and review-driven iteration in a large upstream repository.

It is relevant to engineering roles involving Python APIs, ML/GPU software ecosystems, developer tooling, AI infrastructure and systems integration.

## 6. Scope and limitations

This contribution should be described precisely:

- It extends hipDNN's Python bindings; it is not a new GPU kernel implementation.
- It does not by itself demonstrate GPU performance optimisation.
- GPU-specific execution coverage depends on the appropriate AMD GPU and build configuration.
- The upstream PR's current state should be checked before describing it as merged.

## 7. Primary evidence

- [Pull request #15453](https://github.com/ROCm/rocm-libraries/pull/15453) — source changes, review discussion, CI context and current status.
- [Issue #10584](https://github.com/ROCm/rocm-libraries/issues/10584) — upstream issue referenced by the pull request.

For technical evaluation, use the upstream diff and review thread as the source of truth. This document is a summary of the contribution, not a substitute for the code.
