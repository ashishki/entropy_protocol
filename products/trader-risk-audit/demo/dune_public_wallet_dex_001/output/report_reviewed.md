# Trader Risk Audit Report - Dune Public Wallet DEX Reviewed Copy

Reviewed status: Dune real-open-data development review complete.

This is real-open-data development rehearsal only. It is not a private trader
export, paid-pilot evidence, PMF evidence, customer validation, market-demand
evidence, proof that traders will pay, trading advice, or live trading control.

Material limitations preserved:

- source rows are public Dune `dex.trades` rows filtered by one public `tx_from`
  submitter address, not a verified private trader account ledger;
- the committed `account_id` is a safe public-scope label, not a wallet owner or
  customer id;
- `side=buy` means bought-token side of the public DEX swap, not verified trader
  intent;
- fees are set to `0` only as a canonical schema placeholder; gas, LP fees,
  MEV/slippage, and all-in user execution costs are unsupported;
- P&L attribution, if any, is an audit-engine rehearsal calculation on
  transformed rows, not verified trader-realized P&L;
- leverage, margin, account balances, deposits, withdrawals, and private rules
  are unsupported.

# Trader Risk Audit Report

This audit is not investment advice and does not control live trading.

## Executive Summary

- Rules reviewed: 2
- Violations recorded: 76
- Affected P&L: 0
- Selected policy profile: custom/unspecified

## Summary

- Trades reviewed: 80
- Accounts reviewed: 1
- Source files: trades.csv

### Repeated Patterns

- dune_public_wallet_max_position_size: 76

### Worst Violation Days

- 2026-05-05: 2
- 2026-05-06: 74

## Policy

- Schema version: 1
- Account scope: dune_public_wallet_scope_0xc468315a
- Rules reviewed: 2
- Rule IDs: dune_public_wallet_max_position_size, dune_public_wallet_max_leverage_unsupported

## Violations

| Rule ID | Timestamp | Source Row IDs | Evaluated Value | Threshold | Severity | P&L Impact |
| --- | --- | --- | --- | --- | --- | --- |
| dune_public_wallet_max_position_size | 2026-05-05T20:43:47+00:00 | trade_88bb2a0ed12f4079 | 280023.0335674039439448 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-05T20:43:47+00:00 | trade_d1ebc6768d2ccc7a | 720057.4470756934843072 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T00:54:35+00:00 | trade_24526f08dde3810a | 319930.99503244086737616 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T00:54:35+00:00 | trade_482ed273ba1a09ff | 679855.8257265163432302 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T17:51:23+00:00 | trade_3182902c6d06383f | 60000.12760887311 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T17:51:23+00:00 | trade_32f20e1711b58928 | 319999.784101407081 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T17:51:23+00:00 | trade_5567bcb23a5f4620 | 280000.686378739813 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T17:51:23+00:00 | trade_8e720f65e3e8ffed | 99999.977572363506 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T17:51:23+00:00 | trade_925ae70584856561 | 116344.93991472986149102 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T17:51:23+00:00 | trade_9eaaa5c2941f1577 | 139999.713232082002 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T17:51:23+00:00 | trade_cc62d03a287f5fbf | 419962.1436681413760172 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T17:51:23+00:00 | trade_d97c08f72c9ec68c | 579951.8238464920820254 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T17:53:59+00:00 | trade_0903b60206b2f499 | 39999.919992801287 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T17:53:59+00:00 | trade_25972f05a7575320 | 99999.00914840657 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T17:53:59+00:00 | trade_5a2c8b045ccf3a90 | 239974.2641542890675024 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T17:53:59+00:00 | trade_672a0c8e1fb1c6d4 | 359996.693364857578 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T17:53:59+00:00 | trade_6d98dd887745bab8 | 159998.300371679866 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T17:53:59+00:00 | trade_79fc00904bc44762 | 139998.442204139464 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T17:53:59+00:00 | trade_89fd6b0442ff4f6d | 159968.53541044733849136 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T17:53:59+00:00 | trade_8c2fc816aefa80a2 | 559920.5047003638194194 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:37:47+00:00 | trade_17ffc6374d7fe009 | 220025.084547831917 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:37:47+00:00 | trade_2348c0488dba144e | 139953.218196008692 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:37:47+00:00 | trade_45281b68cf078ae4 | 539991.6776892316898955 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:37:47+00:00 | trade_99ff406790233bd6 | 59980.096427124885 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:37:47+00:00 | trade_b5d237fb2d3c77a1 | 400064.410221698243 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:37:47+00:00 | trade_e01322636a943775 | 440026.59148681000928955 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:37:47+00:00 | trade_ed81a476ae9a9f24 | 160045.101621034622 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:40:23+00:00 | trade_439420643d104a3e | 159862.63688844611572854 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:40:23+00:00 | trade_6a11087c2b7c97f4 | 259764.0003293380049015 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:40:23+00:00 | trade_7cb1d95906a5543c | 579537.6758274154921345 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:40:23+00:00 | trade_af740c354ad7fc5f | 299741.043971898476 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:40:23+00:00 | trade_cae000b9a7ecdcff | 39954.028292484624 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:40:23+00:00 | trade_d1999cc5841d5f4b | 239808.946843585056 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:40:23+00:00 | trade_e06ee0a0094f2b31 | 99969.01371182968 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:40:23+00:00 | trade_f3d1bf3b0af02754 | 46484.67423693399570262 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:40:23+00:00 | trade_fb84d9f74ed0f3d5 | 119946.008010404928 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:53:59+00:00 | trade_75977c140c862469 | 99586.625422317 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:53:59+00:00 | trade_9b800debf25d8da2 | 99586.63991404155 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:53:59+00:00 | trade_9b813842cdeff35c | 526386.61200969975 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:53:59+00:00 | trade_a58f9c4c02352d81 | 256081.31854475595 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:53:59+00:00 | trade_eb5be464a36cd799 | 341440.0634256138 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:58:11+00:00 | trade_2bfe5b0b15c06ec1 | 2339184.11189837112 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:58:11+00:00 | trade_9d0ba7005a2ee251 | 149947.3150906212 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:58:11+00:00 | trade_a617cb086076574c | 209926.83281220072 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T18:58:11+00:00 | trade_e50b46536600dd0f | 269905.0754137788 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T19:06:35+00:00 | trade_073287f61708d604 | 149955.213859314855 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T19:06:35+00:00 | trade_1178417e34f365fd | 479845.2298260701355834 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T19:06:35+00:00 | trade_127f612f3de91ecf | 399862.14651943741831333 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T19:06:35+00:00 | trade_3a08c635c1ae5f52 | 169949.313127865073 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T19:06:35+00:00 | trade_9bf0c0a51b975bcd | 49980.26516571698819486 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T19:06:35+00:00 | trade_b1f8a5aaafdbf0ef | 229931.691941936304 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T19:06:35+00:00 | trade_de3ed21f5cb1e23a | 69979.618189096014 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T19:06:35+00:00 | trade_efb11f60bca2557d | 179946.436385519615 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:05:59+00:00 | trade_0598ca6a235d3899 | 709722.2799314313154806 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:05:59+00:00 | trade_469e744c6b55946d | 49976.49109774880366568 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:05:59+00:00 | trade_47f9bac76bf74202 | 259916.58064168793 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:05:59+00:00 | trade_491a43acfd8f18e3 | 29989.437454453877672106 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:05:59+00:00 | trade_4e60b524ae259c0f | 49983.91536611495286702032619 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:05:59+00:00 | trade_599aa2bbfa0d30ac | 49983.97234208048 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:05:59+00:00 | trade_ca0a03a847a2ddc7 | 149938.65140653679899026 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:05:59+00:00 | trade_de64cf16cb53a533 | 189939.704042059035 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:05:59+00:00 | trade_e0ba6c7f0e8adab6 | 89971.032137547955 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:05:59+00:00 | trade_ee1b066f9d8609c4 | 319898.15075332227 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:10:35+00:00 | trade_1346fb44008038d3 | 69976.265235715725 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:10:35+00:00 | trade_1e5d9ae75ef9a573 | 129955.563762238262 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:10:35+00:00 | trade_4f63921ee4fd975e | 49977.31609618479833388 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:10:35+00:00 | trade_534c43a4acd6bec3 | 119945.05801594408885116 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:10:35+00:00 | trade_5705640a9e37a6af | 69976.176934681062 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:10:35+00:00 | trade_74a20517e88aaf63 | 59969.393466016107153912 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:10:35+00:00 | trade_88fb235e5ab2e377 | 49974.18844440154192806 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:10:35+00:00 | trade_ba2833b69fea9327 | 569744.1572979800380932 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:10:35+00:00 | trade_c2b3799eed268cbf | 339884.371121445678 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:10:35+00:00 | trade_ddcf3cc5fea82025 | 69968.1632907203602896 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:10:35+00:00 | trade_e3be9d4f7a3bdb3c | 79972.87002498917559289066426 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:10:35+00:00 | trade_eef15a36e3cff4cf | 169942.094885472142 | 25000 | breach | 0 |
| dune_public_wallet_max_position_size | 2026-05-06T21:20:59+00:00 | trade_0014d4768bf63d9e | 209940.316652407248 | 25000 | breach | 0 |

## P&L Attribution

- Total P&L: 0
- Compliant P&L: 0
- Violating P&L: 0
- Unclassified P&L: 0
- Reconciliation delta: 0

## Limitations

- dune_public_wallet_max_leverage_unsupported: unsupported_leverage_data (leverage)

## Next Review

- Review any unresolved unsupported-data limitations.
- Confirm policy thresholds before report delivery.
- Re-run the audit after rule or export changes.

