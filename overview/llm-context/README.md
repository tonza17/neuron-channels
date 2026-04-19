# LLM Context Archives

Generated XML archives for pasting into ChatGPT, Gemini, Claude, and similar tools.

## Preset Archives

Curated presets that mix content from multiple aggregator types for specific use cases.

| Preset | Tokens | Best For |
|---|---:|---|
| [`project-overview`](project-overview.xml) | 3K | General orientation, quick status questions, and lightweight strategy chats. |
| [`full`](full.xml) | 28K | Deep project review, comprehensive planning, and long-context synthesis. |
| [`research-history`](research-history.xml) | 25K | Literature review continuity, methodology discussion, and prior-investigation lookup. |
| [`results-deep-dive`](results-deep-dive.xml) | 14K | Performance analysis, experiment comparison, and result interpretation. |
| [`roadmap`](roadmap.xml) | 7K | Deciding what to do next, prioritizing experiments, and planning follow-up work. |
| [`literature-and-assets`](literature-and-assets.xml) | 8K | Method discussion, resource selection, and related-work chats. |
| [`qa`](qa.xml) | 11K | Answer review, follow-up questioning, and project knowledge-base chats. |
| [`project-memory`](project-memory.xml) | 12K | Keeping a durable project memory in medium-size chat sessions. |

## Per-Type Archives

One file per aggregator type with complete untruncated data.

| Type | Tokens | Description |
|---|---:|---|
| [`tasks`](type-tasks.xml) | 5K | Complete task data with full descriptions, results summaries, dependencies, and status. |
| [`papers`](type-papers.xml) | 73K | Complete paper corpus with full summaries, metadata, and abstracts. |
| [`datasets`](type-datasets.xml) | 2K | Complete dataset inventory with full descriptions, access info, and sizes. |
| [`answers`](type-answers.xml) | 9K | Complete question and answer corpus with full answer bodies. |
| [`suggestions`](type-suggestions.xml) | 4K | Complete suggestion list with full descriptions, priority, and status. |
| [`metrics`](type-metrics.xml) | 594 | Complete metric definitions with full descriptions, units, and associated datasets. |
| [`categories`](type-categories.xml) | 1K | Complete category definitions with full detailed descriptions. |
| [`task-types`](type-task-types.xml) | 22K | Complete task type definitions with descriptions and instructions. |
| [`costs`](type-costs.xml) | 286 | Complete cost breakdown with budget, per-service, and per-task details. |

## Context Windows

* `131k-class` — up to 131,072 estimated tokens
* `200k-class` — up to 200,000 estimated tokens
* `1M-class` — up to 1,000,000 estimated tokens

Token counts are approximate and use the shared rule `1 token ~= 4 chars`.

## Project Overview

Compact starter context for general project chats.

* Preset id: `project-overview`
* Short label: `overview` (3K)
* Best for: General orientation, quick status questions, and lightweight strategy chats.
* File: [`project-overview.xml`](project-overview.xml)
* Size: 13.0 KiB (13,312 bytes; 13,287 chars)
* Estimated tokens: 3,321
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
* Short label: `full` (28K)
* Best for: Deep project review, comprehensive planning, and long-context synthesis.
* File: [`full.xml`](full.xml)
* Size: 108.0 KiB (110,547 bytes; 110,240 chars)
* Estimated tokens: 27,560
* Fits: 131k-class, 200k-class, 1M-class

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
* Short label: `research` (25K)
* Best for: Literature review continuity, methodology discussion, and prior-investigation
  lookup.
* File: [`research-history.xml`](research-history.xml)
* Size: 95.9 KiB (98,214 bytes; 98,046 chars)
* Estimated tokens: 24,511
* Fits: 131k-class, 200k-class, 1M-class

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
* Short label: `results` (14K)
* Best for: Performance analysis, experiment comparison, and result interpretation.
* File: [`results-deep-dive.xml`](results-deep-dive.xml)
* Size: 54.8 KiB (56,098 bytes; 55,877 chars)
* Estimated tokens: 13,969
* Fits: 131k-class, 200k-class, 1M-class

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
* Short label: `roadmap` (7K)
* Best for: Deciding what to do next, prioritizing experiments, and planning follow-up work.
* File: [`roadmap.xml`](roadmap.xml)
* Size: 28.1 KiB (28,739 bytes; 28,706 chars)
* Estimated tokens: 7,176
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
* Short label: `assets` (8K)
* Best for: Method discussion, resource selection, and related-work chats.
* File: [`literature-and-assets.xml`](literature-and-assets.xml)
* Size: 33.1 KiB (33,937 bytes; 33,895 chars)
* Estimated tokens: 8,473
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
* Short label: `qa` (11K)
* Best for: Answer review, follow-up questioning, and project knowledge-base chats.
* File: [`qa.xml`](qa.xml)
* Size: 44.6 KiB (45,649 bytes; 45,557 chars)
* Estimated tokens: 11,389
* Fits: 131k-class, 200k-class, 1M-class

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
* Short label: `memory` (12K)
* Best for: Keeping a durable project memory in medium-size chat sessions.
* File: [`project-memory.xml`](project-memory.xml)
* Size: 46.7 KiB (47,838 bytes; 47,790 chars)
* Estimated tokens: 11,947
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
* Size: 21.0 KiB (21,482 bytes; 21,387 chars)
* Estimated tokens: 5,346
* Fits: 131k-class, 200k-class, 1M-class

### All Papers

Complete paper corpus with full summaries, metadata, and abstracts.

* Type id: `papers`
* File: [`type-papers.xml`](type-papers.xml)
* Size: 286.1 KiB (292,938 bytes; 292,339 chars)
* Estimated tokens: 73,084
* Fits: 131k-class, 200k-class, 1M-class

### All Datasets

Complete dataset inventory with full descriptions, access info, and sizes.

* Type id: `datasets`
* File: [`type-datasets.xml`](type-datasets.xml)
* Size: 7.8 KiB (7,941 bytes; 7,884 chars)
* Estimated tokens: 1,971
* Fits: 131k-class, 200k-class, 1M-class

### All Answers

Complete question and answer corpus with full answer bodies.

* Type id: `answers`
* File: [`type-answers.xml`](type-answers.xml)
* Size: 35.4 KiB (36,218 bytes; 36,151 chars)
* Estimated tokens: 9,037
* Fits: 131k-class, 200k-class, 1M-class

### All Suggestions

Complete suggestion list with full descriptions, priority, and status.

* Type id: `suggestions`
* File: [`type-suggestions.xml`](type-suggestions.xml)
* Size: 16.6 KiB (17,013 bytes; 17,007 chars)
* Estimated tokens: 4,251
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
* Size: 1.1 KiB (1,146 bytes; 1,146 chars)
* Estimated tokens: 286
* Fits: 131k-class, 200k-class, 1M-class
