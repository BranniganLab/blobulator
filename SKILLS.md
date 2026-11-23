---
name: backend-refactoring
description: Safely refactor the blobulator backend (legacy code) by mapping the codebase, tracing data flow, and establishing characterization tests before changing implementation.
---

# Backend Refactoring Skills

## Purpose

Assist with refactoring the backend of an existing scientific codebase while preserving its established behavior unless a change is explicitly requested and validated.

The primary focus is understanding the existing implementation before modifying it. Treat the current code as the source of truth for observed behavior, not as proof that its scientific logic is correct.

## Core Principles

- Investigate before modifying.
- Prefer evidence from the code over assumptions.
- Preserve existing behavior by default.
- Separate observed behavior from intended behavior.
- Do not silently fix bugs during refactoring.
- Keep changes focused and avoid unnecessary rewrites.
- Make the code easier to understand, test, and maintain without altering its scientific meaning.
- Clearly communicate uncertainties, assumptions, and unverified behavior.

---

# Skill 1: Codebase Mapping

## Objective

Build a map of the codebase that allows a researcher to understand how inputs are processed, which functions are responsible for each operation, how intermediate data are transformed, and how final results are produced.

## Workflow

### 1. Identify the entry points

Determine how the code is executed, including:

- Main scripts and entry-point functions
- Command-line arguments
- Configuration files
- Input files and formats
- Output files and formats
- Relevant dependencies
- Backend modules called during execution

Do not assume the primary script is the only entry point.

### 2. Trace the data flow

Follow the data through the program from input to output.

For each major step, identify:

- The function or module responsible
- The input data it receives
- The transformations it performs
- Intermediate values or data structures it creates
- The functions it calls next
- The outputs it produces or modifies

Trace actual function calls and variable flow rather than relying solely on function names or documentation.

### 3. Map function responsibilities

For each relevant function, document:

- Function name and location
- Purpose
- Arguments and their expected structure
- Return values
- Side effects, including file I/O or state modification
- Dependencies on other functions
- Whether it contains scientific calculations, data processing, validation, or presentation logic

Identify functions with multiple responsibilities, duplicated logic, tightly coupled dependencies, or unclear boundaries that may be refactoring candidates.

### 4. Trace from specific inputs or outputs

When investigating a particular result, file, calculation, or unexpected behavior, use it as the starting point.

Trace backward to identify where it originates and forward to determine how it is used.

The map should be specific enough that a researcher can follow the code and independently verify the trace.

### 5. Identify uncertainties

Do not invent connections when the code path is unclear or incomplete.

Mark uncertain relationships and explain:

- What is currently known
- What has not been traced
- Why the connection is uncertain
- What additional investigation would resolve it

Examples include error-handling paths, failed input loading, optional branches, fallback behavior, and conditional execution.

## Deliverables

Produce a concise codebase map containing:

1. Entry points and execution flow
2. Input-to-output pipeline
3. Major functions and their responsibilities
4. Intermediate data structures and transformations
5. Function dependencies
6. Error-handling and alternate execution paths
7. Potential refactoring boundaries
8. Unresolved questions or uncertain connections

Use diagrams, tables, or call graphs when they make the architecture easier to understand.

Do not modify code during the initial mapping stage.

---

# Skill 2: Legacy Code Characterization Tests

## Objective

Establish a repeatable record of the existing program's behavior before refactoring. These tests should document what the code currently does without assuming that the observed behavior is scientifically or logically correct.

## Definitions

**Legacy code:** Existing or inherited code whose behavior, assumptions, and checks must be investigated before modification.

**Characterization test:** A repeatable test that captures the existing program's observed behavior for a specific input. It documents behavior rather than asserting that the behavior is correct.

## Workflow

### 1. Identify testable behaviors

Use the codebase map to identify important functions and behaviors that should be preserved.

Prioritize:

- Input parsing and validation
- Data transformations
- Scientific calculations
- Indexing and residue mapping
- Boundary conditions
- File generation
- Error and exception handling
- Known bugs
- Behaviors that may be affected by the refactor

### 2. Select minimal, representative inputs

Prefer small test inputs that exercise specific behaviors.

Tests should be:

- Easy to understand
- Fast to run
- Reproducible
- Focused on a single behavior when possible
- Independent of unnecessary external resources

Use existing fixtures or create small fixtures when practical. Avoid large production datasets when a minimal input can exercise the same code path.

### 3. Capture the current behavior

Run the existing implementation against the selected inputs.

Record relevant observations, including:

- Return values
- Numerical results
- Output files and their contents
- Data shapes and dimensions
- Ordering
- Printed messages, if relevant
- Exceptions and failure behavior

Use the actual observed results as the baseline. Do not derive expected values solely by reading the implementation.

### 4. Convert observations into tests

Create automated tests that reproduce and check the observed behavior.

Tests should be deterministic and avoid unnecessary brittleness. Use exact comparisons when appropriate and tolerances for floating-point values when justified.

Where possible, test functions directly rather than invoking the entire application. Use integration tests when behavior depends on interactions between multiple functions or modules.

### 5. Document known bugs explicitly

Known bugs are part of the observed baseline and must not be silently corrected during characterization.

For example, if the current implementation incorrectly counts Sequence 5's K44 when reporting residue 43, characterize that behavior explicitly.

- Record the observed behavior.
- Label the expectation as a known bug.
- Ensure the test reproduces the existing behavior.
- Do not treat the behavior as scientifically correct.
- Do not silently change the expected result during refactoring.

If the bug is intentionally corrected, update the relevant test only after the researcher approves the behavior change. Preserve tests for unrelated behaviors that should remain unchanged.

### 6. Validate the baseline

Before refactoring:

- Run the characterization tests.
- Confirm that they pass against the unmodified implementation.
- Verify that the tests genuinely exercise the intended code paths.
- Document tests that cannot be run and why.
- Record any nondeterministic behavior and how it is handled.

If a test fails against the original implementation, investigate it rather than assuming the test or code is correct.

## Deliverables

Produce:

1. A characterization test suite
2. Minimal test fixtures
3. A record of captured baseline behavior
4. Documentation of known bugs and anomalies
5. A test execution summary
6. A list of uncharacterized or unverified behaviors

---

# Refactoring Workflow

Follow this sequence for backend refactoring tasks:

## Phase 1 — Investigate

- Map the relevant code.
- Identify the execution path.
- Understand function responsibilities.
- Trace the relevant data.
- Identify dependencies and side effects.
- Report uncertainties.

## Phase 2 — Characterize

- Identify behavior affected by the proposed changes.
- Create minimal reproducible inputs.
- Capture current outputs.
- Build characterization tests.
- Validate the tests against the existing implementation.
- Document known bugs.

Do not proceed with behavior-changing refactoring until the baseline is understood.

## Phase 3 — Plan

Before modifying code, describe:

- What needs to change
- Why it needs to change
- Which functions or modules are affected
- What behavior must be preserved
- What known bugs must remain untouched
- What tests will validate the refactor

Prefer small, incremental changes over large rewrites.

## Phase 4 — Refactor

- Make the smallest changes necessary to achieve the goal.
- Preserve established behavior.
- Keep scientific calculations unchanged unless explicitly requested.
- Avoid unrelated cleanup.
- Do not change test expectations merely to make tests pass.
- Maintain or improve function boundaries, naming, and readability.
- Add tests for new behavior when appropriate.

## Phase 5 — Verify

After each meaningful change:

- Run the relevant characterization tests.
- Compare outputs against the baseline.
- Investigate differences.
- Confirm that changes are intentional.
- Run broader tests when available.
- Report test failures honestly.

## Phase 6 — Report

Summarize:

- What was changed
- Which modules and functions were affected
- What behavior was preserved
- Any behavior that changed
- Tests run and their results
- Known bugs retained
- Remaining uncertainties or recommended next steps

---

# Constraints

- Never assume that a cleaner implementation is scientifically equivalent.
- Never silently change numerical methods, units, indexing conventions, or data interpretation.
- Never remove existing checks without explaining why.
- Never replace observed baseline behavior with assumed correct behavior.
- Never label an untested change as verified.
- Never perform a large refactor before establishing how the existing code behaves.
- Ask the researcher when an ambiguous behavior requires a decision about intended scientific behavior.

The goal is a maintainable backend with transparent, verified behavior—not merely a cleaner codebase.

