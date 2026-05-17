# Tagging Strategy

## Required Operational Tags

Use these tags consistently in documentation, logs, audits, issues, commits, future cloud resources, and metrics:

```text
project=ai-logix
phase=000-foundation-metrics
environment=local|dev|staging|prod
owner=axon-ai
module=backend|frontend|db|ocr|review|auth|evidence
risk_level=low|medium|high|critical
data_classification=public|internal|sensitive
```

## Usage

### Documentation

Use tags in sprint docs and audit docs to make scope searchable.

Example:

```text
project=ai-logix phase=000-foundation-metrics module=auth risk_level=high
```

### Future Logs

When structured logging is added, include module, environment, and data classification.

### Audits

Audit entries and audit reports should classify risk and data sensitivity.

### Issues

GitHub issues should use tags or labels matching module and risk level.

### Commits

Commit messages should remain human-readable. Include module in body when useful, for example `module=docs`.

### Future Cloud Resources

No cloud resources are created in Phase 0. Future cloud resources must include:

- `project=ai-logix`
- `environment`
- `owner`
- `module`
- `data_classification`

### Metrics

Metric reports should identify project, environment, and module so local/dev/staging/prod signals do not mix.

## Current Sprint Tag

```text
project=ai-logix phase=000-foundation-metrics owner=axon-ai data_classification=internal
```
