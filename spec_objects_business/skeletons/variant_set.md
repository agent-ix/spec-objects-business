---
id: variant_set_001
title: "DiagnosticCause"
type: variant_set
object: variant_set
---
<!-- variant_set authoring skeleton (spec-objects-business). Contract:
     - Frontmatter MUST carry id, title, type: variant_set, object: variant_set.
     - "## Variants" (H2, required): a `| Variant | Payload | Description |`
       table with at least one row. The set is closed: the rows are every
       variant there is. Payload names the type the selected variant carries
       (an enumeration, a value object, another variant set), or `none` for a
       variant with no payload. Each Variant appears once.
     - "## Invariants" (H2, optional): prose rules over the whole set.
     Use an enumeration when the variants are bare labels; use a variant_set
     when each variant requires its own payload. A variant_set declares no
     fields or operations. -->
# [variant_set_001] DiagnosticCause

A diagnostic cause is a closed discriminated value: exactly one variant is
selected, and the payload that variant requires travels with it. It is not a
free-form string map.

## Variants

| Variant | Payload | Description |
|---|---|---|
| revision-mismatch | RevisionPair | The expected and actual source revisions differ |
| byte-digest-mismatch | DigestPair | The expected and actual byte digests differ |
| digest-domain-mismatch | DigestDomainPair | The expected and actual digest domains differ |
| unavailable | none | The comparison could not be made |
