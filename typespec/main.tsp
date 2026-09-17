import "@typespec/json-schema";
import "@agent-ix/semantic-core";

using TypeSpec.JsonSchema;
using AgentIx.Semantic.Core;

/**
 * Tier-2 business object declaration schemas (agent-ix/spec-objects-business#4).
 *
 * One model per business object type this module contributes, each validating
 * that type's Quire declaration record (fields, relations, clauses,
 * operations; quire-rs FR-070..FR-072) with type-specific required keys,
 * forbidden keys, and item rules (FR-004). Every grammar item is a `$ref` to
 * `@agent-ix/semantic-core` 0.2.0 and is never redeclared here (FR-004-CON-1);
 * this namespace contributes archetype shapes only.
 *
 * The `$id` base embeds the manifest `version` by intent (FR-002-CON-5): one
 * schema URL names exactly one immutable byte sequence, so a downstream fixture
 * reader that pinned a version can never silently read later bytes. A bump edits
 * this base and `manifest.yaml`'s `version` in one commit and re-runs
 * `make schemas`.
 */
@jsonSchema("https://schemas.agent-ix.org/agent-ix/spec-objects-business/0.6.0/")
namespace AgentIx.SpecObjects.Business;

// ---------------------------------------------------------------------------
// Object artifact frontmatter (FR-009)
// ---------------------------------------------------------------------------

/**
 * The id of an artifact whose type is one of this module's object types: a
 * letter, then letters, digits and underscores. A hyphen is refused.
 * Artifact-type ids such as `FR-100` are not object ids and are not governed
 * by this pattern. The manifest's shared `id` locator carries the same
 * pattern, so Quire refuses a hyphenated object id at validation.
 */
@pattern("^[A-Za-z][A-Za-z0-9_]*$")
scalar ObjectId extends string;

/**
 * The frontmatter every object-type artifact carries, shared by all eleven
 * object types. Keys beyond these (`relationships`, `abstract`, ...) are
 * governed elsewhere and admitted here.
 */
model ObjectFrontmatter {
  id: ObjectId;
  @minLength(1) title: string;
  @minLength(1) type: string;
  object?: string;
  ...Record<unknown>;
}

// ---------------------------------------------------------------------------
// Support models
// ---------------------------------------------------------------------------

/**
 * Open marker: a `FieldDecl` flagged as identity. Used only as the `@contains`
 * predicate for the "≥ 1 identity field" and "0 identity fields" item rules;
 * it is deliberately open so it matches any identity-flagged field.
 */
model IdentityField {
  identity: true;
}

/** Open marker: a `TypeRef` whose target is the kernel `Timestamp` scalar. */
model OccurrenceTypeRef {
  target: KernelScalar.Timestamp;
}

/**
 * Open marker: a `FieldDecl` whose type targets `Timestamp` — the occurrence
 * time an event declaration must carry. Used as a `@contains` predicate.
 */
model OccurrenceField {
  type: OccurrenceTypeRef;
}

/** One entry of a domain's ubiquitous language. */
model Term {
  @minLength(1) term: string;
  doc: string;
}

/**
 * One state-machine transition.
 *
 * Reader rules JSON Schema cannot express (FR-004): `from` and `to` name a
 * `states[].value` of the same record, and `trigger` names an
 * `operations[].name` of the same record. Neither is claimed as a schema
 * refusal; both are stated for the extractor that first populates `states`
 * and `transitions`.
 */
model Transition {
  from: Identifier;
  to: Identifier;
  trigger: Identifier;
  guard?: ClauseRef;
  emits?: SemanticId;
  ...Record<never>;
}

/**
 * One member of a population: a declared type and the extent of its
 * instances (quire-rs FR-075 `Type | Extent` row).
 */
model PopulationMember {
  type: TypeRef;
  extent: Multiplicity;
  ...Record<never>;
}

/** Closed set of process step kinds. */
enum StepKind {
  command,
  event,
  decision,
  compensation,
  wait,
}

/** One step of a business process. */
model ProcessStep {
  name: Identifier;
  kind: StepKind;
  consumes?: SemanticId[];
  emits?: SemanticId[];
  doc?: string;
  ...Record<never>;
}

// ---------------------------------------------------------------------------
// Object-type declaration records
// ---------------------------------------------------------------------------

/**
 * A bounded context. A domain declares a boundary, not data: `fields` and
 * `operations` are forbidden by the seal.
 */
model Domain {
  members?: RelationDecl[];
  vocabulary?: Term[];
  clauses?: ClauseRef[];
  ...Record<never>;
}

/** An entity: identified data with its own lifecycle. */
model Entity {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  relations?: RelationDecl[];
  clauses?: ClauseRef[];
  operations?: OperationDecl[];
  ...Record<never>;
}

/**
 * An entity whose identity is local to its owner. `relations` is forbidden by
 * the seal: a nested entity is reached through its owner. Identity locality is
 * prose the schema does not express.
 */
model NestedEntity {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  owner?: RelationDecl;
  clauses?: ClauseRef[];
  operations?: OperationDecl[];
  ...Record<never>;
}

/**
 * A value object: equality by value, so it carries no identity field of its
 * own. `relations` is forbidden by the seal.
 */
model ValueObject {
  @minItems(1)
  @contains(IdentityField)
  @minContains(0)
  @maxContains(0)
  fields: FieldDecl[];

  clauses?: ClauseRef[];
  operations?: OperationDecl[];
  ...Record<never>;
}

/** An aggregate root: the consistency boundary that exists to enforce invariants. */
model AggregateRoot {
  @contains(IdentityField)
  fields: FieldDecl[];

  @minItems(1)
  clauses: ClauseRef[];

  relations?: RelationDecl[];
  operations?: OperationDecl[];
  members?: RelationDecl[];
  emits?: SemanticId[];
  ...Record<never>;
}

/** A repository: persistence operations over an aggregate. `fields` is forbidden by the seal. */
model Repository {
  @minItems(1)
  operations: OperationDecl[];

  clauses?: ClauseRef[];
  persists?: SemanticId[];
  ...Record<never>;
}

/**
 * A domain event declaration.
 *
 * The declared shape carries no identity field and no `eventId`: occurrence
 * identity belongs to the runtime record, not the declaration. It must carry at
 * least one occurrence field (a `Timestamp`), expressed as a second `contains`
 * predicate through `allOf`, because JSON Schema admits one `contains` per
 * array. `operations` is forbidden by the seal.
 */
@extension(
  "allOf",
  #[#{ properties: #{ fields: #{ contains: #{ `$ref`: "OccurrenceField.json" } } } }]
)
model Event {
  @minItems(1)
  @contains(IdentityField)
  @minContains(0)
  @maxContains(0)
  fields: FieldDecl[];

  clauses?: ClauseRef[];
  source?: SemanticId;
  ...Record<never>;
}

/** A state machine: one operation per transition command. */
model StateMachine {
  @minItems(1)
  operations: OperationDecl[];

  fields?: FieldDecl[];
  states?: EnumValue[];
  transitions?: Transition[];
  clauses?: ClauseRef[];
  ...Record<never>;
}

/**
 * A business process. Its `fields` carry the correlation key, so at least one
 * is an identity field. `relations` is forbidden by the seal.
 */
model Process {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  steps?: ProcessStep[];
  clauses?: ClauseRef[];
  operations?: OperationDecl[];
  emits?: SemanticId[];
  ...Record<never>;
}

/**
 * A population: the closed set of declared types whose instances a model
 * ranges over, each with its extent. A population declares membership, not
 * data: `fields` and `operations` are forbidden by the seal.
 */
model Population {
  members?: PopulationMember[];
  clauses?: ClauseRef[];
  ...Record<never>;
}

/** A controlled label vocabulary. `fields` and `operations` are forbidden by the seal. */
model Enumeration {
  values?: EnumValue[];
  clauses?: ClauseRef[];
  ...Record<never>;
}
