---
id: variant_set_001
title: "DiagnosticCause"
type: variant_set
object: variant_set
---
<!-- variant_set authoring skeleton (spec-objects-business). Contract:
     - Frontmatter MUST carry id, title, type: variant_set, object: variant_set.
     - "## Variants" (H2, required): a `| Name | Payload | Description |`
       table with at least one row, read into the record's `variants`. The
       set is closed: the rows are every variant there is. Name is an
       identifier (letters, digits, underscore). Payload is the artifact id
       of the type the selected variant carries (an enumeration, a value
       object, another variant set); leave it empty for a variant with no
       payload. Each Name appears once.
     Use an enumeration when the variants are bare labels; use a variant_set
     when each variant requires its own payload. A variant_set declares no
     fields, operations or invariants section. -->
# [variant_set_001] DiagnosticCause

A diagnostic cause is a closed discriminated value: exactly one variant is
selected, and the payload that variant requires travels with it. It is not a
free-form string map.

## Variants

| Name | Payload | Description |
|---|---|---|
| revision_mismatch | value_object_001 | The expected and actual source revisions differ |
| byte_digest_mismatch | value_object_001 | The expected and actual byte digests differ |
| digest_domain_mismatch | enumeration_001 | The expected and actual digest domains differ |
| unavailable | | The comparison could not be made |
