# Batch Analyst Contract

`SAS-MI-014` defines a bounded internal analyst contract only. It is not a
general agent runtime.

Allowed operations are fixed:

- retrieve cited context;
- read deterministic metrics;
- draft an internal memo.

Required controls:

- input channel and time window;
- max iterations;
- max retrieved documents;
- cost cap;
- explicit stop reason;
- audit log checksums for retrievals, metric reads, prompt input, and generated
  memo.

Forbidden operations:

- shell commands;
- network/source collection;
- broker APIs;
- approved ledger mutation;
- market-data mutation;
- report publication.
