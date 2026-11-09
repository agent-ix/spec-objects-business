---
id: positive_004
title: "DiagnosticCause"
type: variant_set
object: variant_set
---
# [positive_004] DiagnosticCause

A closed discriminated value: exactly one variant is selected and the payload
that variant requires travels with it.

## Variants

| Variant | Payload | Description |
|---|---|---|
| revision-mismatch | RevisionPair | The expected and actual revisions differ |
| digest-mismatch | DigestPair | The expected and actual digests differ |
| unavailable | none | The comparison could not be made |
