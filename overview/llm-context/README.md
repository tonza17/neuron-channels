# LLM Context Archives

Generated XML archives for pasting into ChatGPT, Gemini, Claude, and similar tools.

## Preset Archives

Curated presets that mix content from multiple aggregator types for specific use cases.

| Preset | Tokens | Best For |
|---|---:|---|
| [`project-overview`](project-overview.xml) | 35K | General orientation, quick status questions, and lightweight strategy chats. |
| [`full`](full.xml) | 568K | Deep project review, comprehensive planning, and long-context synthesis. |
| [`research-history`](research-history.xml) | 764K | Literature review continuity, methodology discussion, and prior-investigation lookup. |
| [`results-deep-dive`](results-deep-dive.xml) | 440K | Performance analysis, experiment comparison, and result interpretation. |
| [`roadmap`](roadmap.xml) | 108K | Deciding what to do next, prioritizing experiments, and planning follow-up work. |
| [`literature-and-assets`](literature-and-assets.xml) | 61K | Method discussion, resource selection, and related-work chats. |
| [`qa`](qa.xml) | 133K | Answer review, follow-up questioning, and project knowledge-base chats. |
| [`project-memory`](project-memory.xml) | 50K | Keeping a durable project memory in medium-size chat sessions. |

## Per-Type Archives

One file per aggregator type with complete untruncated data.

| Type | Tokens | Description |
|---|---:|---|
| [`tasks`](type-tasks.xml) | 272K | Complete task data with full descriptions, results summaries, dependencies, and status. |
| [`papers`](type-papers.xml) | 297K | Complete paper corpus with full summaries, metadata, and abstracts. |
| [`datasets`](type-datasets.xml) | 7K | Complete dataset inventory with full descriptions, access info, and sizes. |
| [`libraries`](type-libraries.xml) | 65K | Complete library registry with full descriptions, module paths, and entry points. |
| [`answers`](type-answers.xml) | 108K | Complete question and answer corpus with full answer bodies. |
| [`suggestions`](type-suggestions.xml) | 101K | Complete suggestion list with full descriptions, priority, and status. |
| [`predictions`](type-predictions.xml) | 11K | Complete predictions inventory with full descriptions, metrics, and model references. |
| [`metrics`](type-metrics.xml) | 594 | Complete metric definitions with full descriptions, units, and associated datasets. |
| [`categories`](type-categories.xml) | 1K | Complete category definitions with full detailed descriptions. |
| [`task-types`](type-task-types.xml) | 22K | Complete task type definitions with descriptions and instructions. |
| [`costs`](type-costs.xml) | 1K | Complete cost breakdown with budget, per-service, and per-task details. |

## Context Windows

* `131k-class` — up to 131,072 estimated tokens
* `200k-class` — up to 200,000 estimated tokens
* `1M-class` — up to 1,000,000 estimated tokens

Token counts are approximate and use the shared rule `1 token ~= 4 chars`.

## Project Overview

Compact starter context for general project chats.

* Preset id: `project-overview`
* Short label: `overview` (35K)
* Best for: General orientation, quick status questions, and lightweight strategy chats.
* File: [`project-overview.xml`](project-overview.xml)
* Size: 137.3 KiB (140,635 bytes; 140,368 chars)
* Estimated tokens: 35,092
* Fits: 131k-class, 200k-class, 1M-class

### Included Types

| Included Type | Coverage |
|---|---|
| Project description | Full `project/description.md`. |
| Completed tasks | All completed tasks with `results_summary` excerpts and short descriptions. |
| Planned tasks | All planned or active tasks with status, date, dependencies, and short descriptions. |
| Questions and answers | All questions with short-answer coverage only. |

## Full Project Context

Largest preset with detailed completed-task reports and the full project knowledge base.

* Preset id: `full`
* Short label: `full` (568K)
* Best for: Deep project review, comprehensive planning, and long-context synthesis.
* File: [`full.xml`](full.xml)
* Size: 2225.1 KiB (2,278,465 bytes; 2,270,136 chars)
* Estimated tokens: 567,534
* Fits: 1M-class

### Included Types

| Included Type | Coverage |
|---|---|
| Project description | Full `project/description.md`. |
| Completed tasks | All completed tasks with `results_summary` excerpts and short descriptions. |
| Detailed results | Every available completed-task `results/results_detailed.md` file in full. |
| Planned tasks | All planned or active tasks with status, date, dependencies, short descriptions, and full long descriptions. |
| Questions and answers | All questions with full-answer bodies when available. |
| Papers | All papers with metadata and summary excerpts from paper summaries, full summaries, or abstracts. |
| Datasets | All datasets with access, size, source task, and description excerpts. |
| Libraries | All libraries with module paths, source task, and description excerpts. |
| Metrics | All registered metrics with units, value types, and description excerpts. |

## Research History

Research-stage documents across completed tasks, plus core project context.

* Preset id: `research-history`
* Short label: `research` (764K)
* Best for: Literature review continuity, methodology discussion, and prior-investigation
  lookup.
* File: [`research-history.xml`](research-history.xml)
* Size: 2992.7 KiB (3,064,536 bytes; 3,057,233 chars)
* Estimated tokens: 764,308
* Fits: 1M-class

### Included Types

| Included Type | Coverage |
|---|---|
| Project description | Full `project/description.md`. |
| Completed tasks | All completed tasks with `results_summary` excerpts and short descriptions. |
| Planned tasks | All planned or active tasks with status, date, dependencies, and short descriptions. |
| Questions and answers | All questions with short-answer coverage only. |
| Research documents | All available completed-task `research_papers.md`, `research_internet.md`, and `research_code.md` files in full. |

## Results Deep Dive

Completed-task result summaries plus all detailed results reports.

* Preset id: `results-deep-dive`
* Short label: `results` (440K)
* Best for: Performance analysis, experiment comparison, and result interpretation.
* File: [`results-deep-dive.xml`](results-deep-dive.xml)
* Size: 1725.1 KiB (1,766,490 bytes; 1,758,769 chars)
* Estimated tokens: 439,692
* Fits: 1M-class

### Included Types

| Included Type | Coverage |
|---|---|
| Project description | Full `project/description.md`. |
| Completed tasks | All completed tasks with `results_summary` excerpts and short descriptions. |
| Detailed results | Every available completed-task `results/results_detailed.md` file in full. |
| Planned tasks | All planned or active tasks with status, date, dependencies, and short descriptions. |
| Questions and answers | All questions with short-answer coverage only. |

## Roadmap

Project planning preset centered on upcoming tasks and open suggestions.

* Preset id: `roadmap`
* Short label: `roadmap` (108K)
* Best for: Deciding what to do next, prioritizing experiments, and planning follow-up work.
* File: [`roadmap.xml`](roadmap.xml)
* Size: 420.7 KiB (430,829 bytes; 430,394 chars)
* Estimated tokens: 107,598
* Fits: 131k-class, 200k-class, 1M-class

### Included Types

| Included Type | Coverage |
|---|---|
| Project description | Full `project/description.md`. |
| Completed tasks | All completed tasks with `results_summary` excerpts and short descriptions. |
| Planned tasks | All planned or active tasks with status, date, dependencies, short descriptions, and full long descriptions. |
| Questions and answers | All questions with short-answer coverage only. |
| Suggestions | All open suggestions with priority, kind, source task, and description excerpts. |

## Literature and Assets

Paper summaries and reusable project assets without the heaviest task reports.

* Preset id: `literature-and-assets`
* Short label: `assets` (61K)
* Best for: Method discussion, resource selection, and related-work chats.
* File: [`literature-and-assets.xml`](literature-and-assets.xml)
* Size: 238.1 KiB (243,822 bytes; 243,477 chars)
* Estimated tokens: 60,869
* Fits: 131k-class, 200k-class, 1M-class

### Included Types

| Included Type | Coverage |
|---|---|
| Project description | Full `project/description.md`. |
| Completed tasks | All completed tasks with `results_summary` excerpts and short descriptions. |
| Planned tasks | All planned or active tasks with status, date, dependencies, and short descriptions. |
| Questions and answers | All questions with short-answer coverage only. |
| Papers | All papers with metadata and summary excerpts from paper summaries, full summaries, or abstracts. |
| Datasets | All datasets with access, size, source task, and description excerpts. |
| Libraries | All libraries with module paths, source task, and description excerpts. |
| Metrics | All registered metrics with units, value types, and description excerpts. |

## Questions and Answers

Question-centric preset with the full answer corpus and compact project state.

* Preset id: `qa`
* Short label: `qa` (133K)
* Best for: Answer review, follow-up questioning, and project knowledge-base chats.
* File: [`qa.xml`](qa.xml)
* Size: 519.9 KiB (532,348 bytes; 531,612 chars)
* Estimated tokens: 132,903
* Fits: 200k-class, 1M-class

### Included Types

| Included Type | Coverage |
|---|---|
| Project description | Full `project/description.md`. |
| Completed tasks | All completed tasks with `results_summary` excerpts and short descriptions. |
| Planned tasks | All planned or active tasks with status, date, dependencies, and short descriptions. |
| Questions and answers | All questions with full-answer bodies when available. |

## Project Memory

Mid-size preset intended as a reusable working memory for ongoing chats.

* Preset id: `project-memory`
* Short label: `memory` (50K)
* Best for: Keeping a durable project memory in medium-size chat sessions.
* File: [`project-memory.xml`](project-memory.xml)
* Size: 197.4 KiB (202,105 bytes; 201,811 chars)
* Estimated tokens: 50,452
* Fits: 131k-class, 200k-class, 1M-class

### Included Types

| Included Type | Coverage |
|---|---|
| Project description | Full `project/description.md`. |
| Completed tasks | All completed tasks with `results_summary` excerpts and short descriptions. |
| Planned tasks | All planned or active tasks with status, date, dependencies, and short descriptions. |
| Questions and answers | All questions with short-answer coverage only. |
| Papers | The 20 most recent papers with metadata and summary excerpts. |
| Datasets | All datasets with access, size, source task, and description excerpts. |
| Libraries | All libraries with module paths, source task, and description excerpts. |
| Metrics | All registered metrics with units, value types, and description excerpts. |
| Suggestions | The top 20 open suggestions ordered by priority and date. |

## Per-Type Archive Details

### All Tasks

Complete task data with full descriptions, results summaries, dependencies, and status.

* Type id: `tasks`
* File: [`type-tasks.xml`](type-tasks.xml)
* Size: 1067.4 KiB (1,093,010 bytes; 1,088,562 chars)
* Estimated tokens: 272,140
* Fits: 1M-class

### All Papers

Complete paper corpus with full summaries, metadata, and abstracts.

* Type id: `papers`
* File: [`type-papers.xml`](type-papers.xml)
* Size: 1162.7 KiB (1,190,588 bytes; 1,188,108 chars)
* Estimated tokens: 297,027
* Fits: 1M-class

### All Datasets

Complete dataset inventory with full descriptions, access info, and sizes.

* Type id: `datasets`
* File: [`type-datasets.xml`](type-datasets.xml)
* Size: 29.3 KiB (30,034 bytes; 29,894 chars)
* Estimated tokens: 7,473
* Fits: 131k-class, 200k-class, 1M-class

### All Libraries

Complete library registry with full descriptions, module paths, and entry points.

* Type id: `libraries`
* File: [`type-libraries.xml`](type-libraries.xml)
* Size: 255.7 KiB (261,805 bytes; 261,153 chars)
* Estimated tokens: 65,288
* Fits: 131k-class, 200k-class, 1M-class

### All Answers

Complete question and answer corpus with full answer bodies.

* Type id: `answers`
* File: [`type-answers.xml`](type-answers.xml)
* Size: 423.0 KiB (433,129 bytes; 432,636 chars)
* Estimated tokens: 108,159
* Fits: 131k-class, 200k-class, 1M-class

### All Suggestions

Complete suggestion list with full descriptions, priority, and status.

* Type id: `suggestions`
* File: [`type-suggestions.xml`](type-suggestions.xml)
* Size: 395.7 KiB (405,156 bytes; 404,994 chars)
* Estimated tokens: 101,248
* Fits: 131k-class, 200k-class, 1M-class

### All Predictions

Complete predictions inventory with full descriptions, metrics, and model references.

* Type id: `predictions`
* File: [`type-predictions.xml`](type-predictions.xml)
* Size: 41.3 KiB (42,320 bytes; 42,284 chars)
* Estimated tokens: 10,571
* Fits: 131k-class, 200k-class, 1M-class

### All Metrics

Complete metric definitions with full descriptions, units, and associated datasets.

* Type id: `metrics`
* File: [`type-metrics.xml`](type-metrics.xml)
* Size: 2.3 KiB (2,379 bytes; 2,379 chars)
* Estimated tokens: 594
* Fits: 131k-class, 200k-class, 1M-class

### All Categories

Complete category definitions with full detailed descriptions.

* Type id: `categories`
* File: [`type-categories.xml`](type-categories.xml)
* Size: 4.3 KiB (4,429 bytes; 4,425 chars)
* Estimated tokens: 1,106
* Fits: 131k-class, 200k-class, 1M-class

### All Task Types

Complete task type definitions with descriptions and instructions.

* Type id: `task-types`
* File: [`type-task-types.xml`](type-task-types.xml)
* Size: 84.2 KiB (86,222 bytes; 86,156 chars)
* Estimated tokens: 21,539
* Fits: 131k-class, 200k-class, 1M-class

### Project Costs

Complete cost breakdown with budget, per-service, and per-task details.

* Type id: `costs`
* File: [`type-costs.xml`](type-costs.xml)
* Size: 5.3 KiB (5,446 bytes; 5,446 chars)
* Estimated tokens: 1,361
* Fits: 131k-class, 200k-class, 1M-class
