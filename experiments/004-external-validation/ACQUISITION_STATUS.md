# Experiment 004 Acquisition Status

## Status

Official benchmark acquisition is currently blocked.

No benchmark substitution has been made.
No corpus has been extracted.
No C0 or C1 measurements have been computed.

## Date observed

```text
2026-10-01
```

## Frozen experiment protocol

```text
8227fa6a070c4822c682baf052cfb35c285c2d2e
```

Protocol SHA-256:

```text
99662720BC351B5E1C4C353E13660BD7338E5E06508B2C6C28FF0626DF4F7170
```

## Frozen BigCloneEval revision

```text
6d393ec8adb1d71493d09881ba520659b6c2c68e
```

## Intended official artifacts

BigCloneBench Version 2:

```text
BigCloneBench_BCEvalVersion.tar.gz
```

IJaDataset reduced distribution:

```text
IJaDataset_BCEvalVersion.tar.gz
```

The frozen BigCloneEval documentation identifies these artifacts and
provides OneDrive distribution links.

## Automated acquisition attempt

A direct PowerShell Invoke-WebRequest attempt against the official
BigCloneBench OneDrive link failed before any artifact was accepted.

Observed result:

```text
HTTP 403 Forbidden
```

The acquisition script rejected the failed response and did not extract
or measure any data.

## Browser acquisition attempt

Opening the official IJaDataset OneDrive distribution link in a normal
web browser did not produce the archive.

Observed browser result:

```text
ERR_FAILED
```

## Current upstream state

At the observation date, the public BigCloneBench documentation still
identifies BigCloneBench Version 2 as the preferred benchmark and points
to BigCloneEval for its optimized distribution.

The public BigCloneEval documentation still exposes the same OneDrive
artifact links recorded by the frozen local checkout.

The public BigCloneBench documentation notes that OneDrive limitations
may require login for large-file downloads.

## Reproducibility decision

Experiment 004 will not silently substitute an unofficial mirror,
repackaged benchmark, filtered derivative dataset, or older ERA release.

A replacement distribution may be used only if its provenance and
equivalence to the intended benchmark are established before measurement
and recorded transparently.

## Next acquisition route

The preferred next route is to obtain the intended artifacts from the
benchmark maintainer or another authoritative distribution source.

After acquisition, the exact filenames, byte sizes, SHA-256 hashes,
archive inventories, and extraction inventories must be recorded before
sampling or similarity measurement.

## Measurement prohibition

C0/C1 measurement remains prohibited until corpus acquisition, hashing,
inventory, schema inspection, and sampling freeze are complete.
