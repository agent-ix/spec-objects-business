# spec-objects-business

> Filament Module: tier-2 business ObjectTypes (DDD: domain, entity, value_object, aggregate_root, repository, event, state_machine, process, enumeration)

Agent-IX Filament module loaded by [`quire-cli`](https://github.com/agent-ix/quire-cli) and [`ix-spec`](https://github.com/agent-ix/ix-spec).

## Installing quire-cli

This module is consumed by the `quire` binary from [`quire-cli`](https://github.com/agent-ix/quire-cli), published on the public npm registry, so no auth or registry config is needed:

```bash
npm install -g @agent-ix/quire-cli
```

See [quire-cli install instructions](https://github.com/agent-ix/quire-cli#install) for details.

## Object types provided

| Object | `type:` | Description |
|--------|---------|-------------|
| Domain | `domain` | A bounded context defining what it owns vs. delegates to neighbouring contexts, with an optional entity summary, ERD, and ubiquitous language. |
| Entity | `entity` | An object with a stable identity field plus its typed attributes and their meaning. |
| Value object | `value_object` | An immutable value defined by its components, with equality and validity rules but no identity of its own. |
| Aggregate root | `aggregate_root` | The consistency boundary — root, nested entities, owned value objects, and the invariants the root enforces over them. |
| Nested entity | `nested_entity` | An entity owned by an aggregate root, with parent-local identity whose every mutation is mediated by the parent. |
| Repository | `repository` | The collection-like access point that loads and saves whole aggregates, with each operation's signature, behaviour, and failure semantics. |
| Event | `event` | A domain/integration event whose payload contract is given as a JSON Schema. |
| State machine | `state_machine` | An object lifecycle expressed as a mermaid `stateDiagram-v2` of states and transitions. |
| Process | `process` | A long-running workflow/saga diagrammed in mermaid (one or more flows), with optional state diagrams, specification, and algorithm. |
| Enumeration | `enumeration` | A controlled label vocabulary (state names, kinds, codes) as a `Value | Description` table referenced by exact string. |

## How this module is used

### With ix-spec (recommended)

```bash
# Install this module as a plugin (from a local checkout)
ix-spec plugin install path:../spec-objects-business

# List the kinds the installed modules expose
ix-spec catalog list

# Author new artifacts from these object types
ix-spec write . --types domain,aggregate_root

# Review/validate the authored artifacts
ix-spec review
```

See [ix-spec](https://github.com/agent-ix/ix-spec).

### With quire-cli directly

```bash
# Emit an authoring skeleton for a given kind
quire schema domain --module ./spec_objects_business

# Validate Markdown spec artifacts against the module
quire validate spec/**/*.md --module ./spec_objects_business

# Extract structured object bodies from a document
quire extract spec/order-management.md --module ./spec_objects_business
```

See [quire-cli usage instructions](https://github.com/agent-ix/quire-cli#usage-instructions).

## Development

Python 3.13+, [Poetry](https://python-poetry.org/) managed, flat layout (package `spec_objects_business` at root). Versioning is dynamic from the Git tag; CI (GitHub Actions on `push`/`pull_request`/`tag v*.*.*`) runs tests + lint and publishes the wheel/sdist to Google Artifact Registry (PyPI-compatible) via `twine`.

```bash
make install                  # install deps into the Poetry venv
make test                     # run pytest
make lint                     # ruff + black check
make format                   # ruff + black format
make build                    # build wheel + sdist under dist/
make update-lock              # update poetry.lock
make use-local p=<name>       # switch a dep to local pypi.ix
make use-upstream p=<name>    # switch a dep back to upstream
make local-publish            # build + publish to local pypi.ix
```

Required CI secrets/vars: `GCP_SERVICE_ACCOUNT_KEY`, `GCP_REGION`, `GCP_PROJECT_NAME`, `GCP_PYPI`.
