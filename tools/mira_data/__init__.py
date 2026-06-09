"""Mira portable data-acquisition substrate (stdlib-only core).

This package fills the execution-layer slots that ``data/ingestion-layer.md`` and
the source registry already specify but never implemented: fetch adapters
(provider adapter -> canonical contract), an evidence-tier tagger, and an
emitter for the ingestion / evidence / calculation-ledger artifacts.

Design contract (see ``architecture/data-acquisition-upgrade.md``):

- stdlib only in the core; ``yfinance`` is an optional escalation, never a core
  dependency (honours the justfile "zero third-party deps" contract).
- every fetched field is born tagged with its registry evidence posture, so an
  aggregator value can never masquerade as an official fact.
- a calculation-ledger row is emitted only for numbers Mira itself derives and
  that affect a judgment; issuer-disclosed values are reported, not ledgered.
"""

__all__ = ["canonical", "net", "emit"]
