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
 * `@agent-ix/semantic-core` and is never redeclared here (FR-004-CON-1);
 * this namespace contributes archetype shapes only.
 */
@jsonSchema("https://schemas.agent-ix.org/agent-ix/spec-objects-business/")
namespace AgentIx.SpecObjects.Business;

// ---------------------------------------------------------------------------
// Object artifact frontmatter (FR-009)
// ---------------------------------------------------------------------------

model ObjectFrontmatter {
  @pattern("^[A-Za-z][A-Za-z0-9_]*(?:-[A-Za-z0-9_]+)*$")
  id: string;
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
@extension("not", #{ required: #["guard", "guardExpression"] })
model Transition {
  from: Identifier;
  to: Identifier;
  trigger: Identifier;
  guard?: ClauseRef;
  guardExpression?: Expression;
  emits?: SemanticId;
  ...Record<never>;
}

/**
 * An inline Quire expression carried opaquely: the authored text and the span
 * of that text. A `Guard` cell or a `Pre:`/`Post:` line holding an expression
 * rather than a clause id is carried this way (quire-rs FR-071, FR-075).
 */
model Expression {
  kind: "expression";
  @minLength(1) text: string;
  sourceSpan: SourceLocus;
  ...Record<never>;
}

/** Which contract line of an operation an expression was authored on. */
enum ExpressionSlot {
  pre,
  post,
}

/**
 * The inline expression of one operation `Pre:` or `Post:` line. It sits
 * beside `operations` because `OperationDecl.pre` and `post` carry clause
 * references only. `operation` names an `operations[].name` of the same
 * record, a reader rule JSON Schema does not express.
 */
model OperationExpression {
  operation: Identifier;
  slot: ExpressionSlot;
  expression: Expression;
  ...Record<never>;
}

/** One member of a population: a declared type. */
model PopulationMember {
  type: TypeRef;
  ...Record<never>;
}

/** Whether a population's membership is fixed (`closed`) or may grow (`open`). */
enum PopulationExtent {
  closed,
  open,
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
 * A bounded context. A domain declares a boundary, not data: `fields`,
 * `operations` and `clauses` are forbidden by the seal (QSpec FR-208: a
 * namespace declares no fields and no operations, and a `quire` clause on it
 * is `unsupported_construct`/`declaration-form`).
 */
model Domain {
  relations?: RelationDecl[];
  vocabulary?: Term[];
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
  operationExpressions?: OperationExpression[];
  ...Record<never>;
}

/**
 * An entity whose identity is local to its owner. `relations` is forbidden by
 * the seal: a nested entity is reached through its owner. It carries no
 * `owner` key: the owner is the single inbound composite edge a bundle
 * declares for the artifact (a bundle rule, quoin FR-123), so no per-artifact
 * extraction can fill it. Identity locality is prose the schema does not
 * express.
 */
model NestedEntity {
  @minItems(1)
  @contains(IdentityField)
  fields?: FieldDecl[];

  clauses?: ClauseRef[];
  operations?: OperationDecl[];
  operationExpressions?: OperationExpression[];
  ...Record<never>;
}

/**
 * A value object: equality by value, so it carries no identity field of its
 * own. `relations` and `operations` are forbidden by the seal (QSpec FR-208:
 * an operation of a record value type is `unsupported_construct`/
 * `declaration-form`).
 */
model ValueObject {
  @minItems(1)
  @contains(IdentityField)
  @minContains(0)
  @maxContains(0)
  fields: FieldDecl[];

  clauses?: ClauseRef[];
  ...Record<never>;
}

/** An aggregate root: the consistency boundary that exists to enforce invariants. */
model AggregateRoot {
  @contains(IdentityField)
  fields?: FieldDecl[];

  @minItems(1)
  clauses?: ClauseRef[];

  relations?: RelationDecl[];
  operations?: OperationDecl[];
  operationExpressions?: OperationExpression[];
  members?: RelationDecl[];
  emits?: SemanticId[];
  ...Record<never>;
}

/**
 * A repository: persistence operations over an aggregate. `fields` and
 * `clauses` are forbidden by the seal, and each operation's `pre`/`post` (a
 * `Pre:`/`Post:` contract) must be empty or absent (QSpec FR-208: an
 * operation contract or a `quire` clause on a persistence interface is
 * `unsupported_construct`/`declaration-form`).
 */
@extension(
  "allOf",
  #[
    #{
      properties: #{
        operations: #{
          not: #{
            contains: #{
              anyOf: #[
                #{ required: #["pre"], properties: #{ pre: #{ minItems: 1 } } },
                #{ required: #["post"], properties: #{ post: #{ minItems: 1 } } }
              ]
            }
          }
        }
      }
    }
  ]
)
model Repository {
  @minItems(1)
  operations: OperationDecl[];

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
  fields?: FieldDecl[];

  clauses?: ClauseRef[];
  source?: SemanticId;
  ...Record<never>;
}

/** A state machine: one operation per transition command. */
model StateMachine {
  @minItems(1)
  operations?: OperationDecl[];

  operationExpressions?: OperationExpression[];
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
  fields?: FieldDecl[];

  steps?: ProcessStep[];
  states?: EnumValue[];
  clauses?: ClauseRef[];
  operations?: OperationDecl[];
  operationExpressions?: OperationExpression[];
  emits?: SemanticId[];
  ...Record<never>;
}

/**
 * A population: the declared types whose instances a model ranges over, with
 * one `extent` for the whole population. A population declares membership,
 * not data: `fields` and `operations` are forbidden by the seal.
 */
model Population {
  extent?: PopulationExtent;
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

/**
 * One variant of a closed union, one row of the `## Variants` table. `payload`
 * is the artifact id of the type the selected variant carries (a table cell
 * reads a `SemanticId`, not a `TypeRef` object); a variant with no payload
 * leaves the cell empty and omits the key.
 */
model VariantDecl {
  name: Identifier;
  payload?: SemanticId;
  description?: string;
  ...Record<never>;
}

/**
 * A closed discriminated union: a closed set of variants, each carrying the
 * payload its selection requires. The `## Variants` table is read by the
 * module's body extraction; the declaration record carries no fields or
 * operations, which the seal forbids.
 */
model VariantSet {
  variants?: VariantDecl[];
  clauses?: ClauseRef[];
  ...Record<never>;
}

/**
 * An acyclic partial order: nodes, edges, and the concurrent branches the
 * edges leave unordered. It has no current state, so it declares no `states`,
 * `transitions`, `fields` or `operations`; the seal forbids them. The
 * graph itself is the required `## Graph` mermaid block, which the module's
 * body extraction reads.
 */
model Graph {
  clauses?: ClauseRef[];
  ...Record<never>;
}
