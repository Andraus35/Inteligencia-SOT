PYTHON ?= python3
export UV_CACHE_DIR := $(CURDIR)/.cache/uv
export PRE_COMMIT_HOME := $(CURDIR)/.cache/pre-commit
OWNED_PYTHON = scripts tests .claude/hooks rag/traducao/harness/harness.py rag/traducao/harness/tests

.PHONY: setup lint typecheck format format-check test test-docker governance score score-check eval-a feedback check
setup:
	uv sync --locked --group dev
	uv run --frozen pre-commit install
lint:
	uv run --frozen --offline ruff check $(OWNED_PYTHON)
typecheck:
	uv run --frozen --offline mypy
format:
	uv run --frozen --offline ruff format $(OWNED_PYTHON)
format-check:
	uv run --frozen --offline ruff format --check $(OWNED_PYTHON)
test:
	uv run --frozen --offline pytest
test-docker:
	TRANSLATION_TEST_DOCKER=1 uv run --frozen --offline pytest
governance:
	$(PYTHON) -B rag/traducao/harness/harness.py selfcheck
score:
	$(PYTHON) -B scripts/harness_score.py --output docs/harness-score-current.json
score-check:
	$(PYTHON) -B scripts/harness_score.py --min-level 4
eval-a:
	$(PYTHON) -B scripts/harness_eval.py inventory --run-id $(RUN_ID) --docs full --tracks A
	$(PYTHON) -B scripts/harness_eval.py correctness --run-id $(RUN_ID)
feedback: lint governance
	git diff --check
check: governance lint typecheck format-check test-docker score-check
