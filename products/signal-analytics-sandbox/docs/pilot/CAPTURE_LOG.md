# Capture Log - First Telegram Source

Дата: 2026-05-07
Статус: captured public batch for `bablos79`
First source: `bablos79` (`https://t.me/bablos79`)

## Capture Method

Capture is public-only. For this run, the operator requested parsing the public
Telegram source, so the capture used unauthenticated `https://t.me/s/bablos79`
HTML pages and stored only public text into the local workspace.

Forbidden methods:

- private or authenticated scraping;
- joining private groups for capture;
- login-wall or paywall bypass;
- credential sharing or impersonation;
- screenshot/OCR capture for this pilot;
- bot ingestion or autonomous collection.

If a post cannot be captured through public text, record it as
`skipped` or `blocked` with a reason. Do not invent post text, timestamps, URLs,
or trading calls.

## Required Evidence Fields

Every captured row must have these fields before extraction begins:

| Field | Required | Notes |
|-------|----------|-------|
| `capture_id` | yes | Stable local ID, e.g. `bablos79-cap-001`. |
| `source_id` | yes | `bablos79` for the first source. |
| `public_url` | yes for captured rows | Public `https://t.me/...` post URL or public source reference. |
| `capture_timestamp_utc` | yes for captured rows | UTC timestamp when the operator captured the text. |
| `raw_text_sha256` | yes for captured rows | SHA-256 of the exact raw text bytes. |
| `raw_text_storage` | yes for captured rows | Local path or workspace reference where raw text is stored. |
| `status` | yes | One of the capture statuses below. |
| `skip_or_block_reason` | required unless `status=captured` | Explain why no usable capture exists yet. |
| `operator_notes` | yes | Short notes for source context and limitations. |

## Capture Status Definitions

| Status | Meaning | Next action |
|--------|---------|-------------|
| `captured` | Public post text is captured with URL, timestamp, raw text, and SHA-256. | Ready for manual extraction. |
| `skipped` | Public content exists but is intentionally not captured for methodology reasons. | Record reason; do not extract. |
| `blocked` | Capture is forbidden or impossible under pilot boundaries. | Record blocker; do not bypass controls. |
| `pending-operator-input` | No real public capture has been supplied yet. | Operator must provide public text/evidence. |

## Skip / Block Reasons

Use one of these reason codes when `status` is not `captured`:

| Reason code | Applies when |
|-------------|--------------|
| `non_public` | Post/source is not publicly reachable. |
| `private_group` | Content requires joining a private Telegram group or channel. |
| `paywalled` | Content is behind payment or subscription controls. |
| `login_walled` | Content requires login/authenticated access. |
| `screenshot_only` | Relevant content is only available as an image/screenshot; OCR is deferred. |
| `insufficient_text` | Public text exists but does not contain enough text for capture/extraction. |
| `deleted_or_unavailable` | Public post was deleted or cannot be verified at capture time. |
| `duplicate_public_post` | Same public post/content already captured. |
| `outside_audit_window` | Post is outside the bounded audit window/target count. |
| `pending_operator_input` | Operator has not supplied the public post text/evidence yet. |

## Current Capture Rows

Public unauthenticated Telegram HTML capture completed at `2026-05-07T18:51:32Z`. Fetched pages: `https://t.me/s/bablos79`, `https://t.me/s/bablos79?before=10504`, `https://t.me/s/bablos79?before=10483`, `https://t.me/s/bablos79?before=10462`.

Total captured text posts: 60. No private/authenticated source was used.

| capture_id | source_id | public_url | capture_timestamp_utc | source_timestamp_utc | raw_text_sha256 | raw_text_storage | status | skip_or_block_reason | operator_notes |
|------------|-----------|------------|-----------------------|----------------------|-----------------|------------------|--------|----------------------|----------------|
| `bablos79-10442` | `bablos79` | `https://t.me/bablos79/10442` | `2026-05-07T18:51:32Z` | `2026-04-27T07:12:22+00:00` | `b3efd9207df62a8bc98381986770a9856d6a895fd6eba5d1d845a235ec50bb39` | `workspace/captures/bablos79/bablos79-10442.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10443` | `bablos79` | `https://t.me/bablos79/10443` | `2026-05-07T18:51:32Z` | `2026-04-27T07:37:49+00:00` | `e8cc076d6964b735e01793ea6306204aa895ffa5817f3656d8547d9ec7bc54c0` | `workspace/captures/bablos79/bablos79-10443.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10444` | `bablos79` | `https://t.me/bablos79/10444` | `2026-05-07T18:51:32Z` | `2026-04-27T08:12:53+00:00` | `c785dddfdda0d6930af3bbfadddf809c8be0d5b408571a850bb086b8ca94e420` | `workspace/captures/bablos79/bablos79-10444.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10445` | `bablos79` | `https://t.me/bablos79/10445` | `2026-05-07T18:51:32Z` | `2026-04-27T08:22:42+00:00` | `7240bc06c96033184438ba48ba40c034c36d48d1a7b58b48350014b510b52e24` | `workspace/captures/bablos79/bablos79-10445.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10446` | `bablos79` | `https://t.me/bablos79/10446` | `2026-05-07T18:51:32Z` | `2026-04-27T09:35:58+00:00` | `cf0691306ee1a12f6c7afb6bf6fbefd21b9fe4375c707d4b8a73d9d8bb7981a6` | `workspace/captures/bablos79/bablos79-10446.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10447` | `bablos79` | `https://t.me/bablos79/10447` | `2026-05-07T18:51:32Z` | `2026-04-27T10:03:37+00:00` | `4c1b16c3073103c7fa2112eb38cfdfc2fac847bb74223db72855b12f6c0a07a1` | `workspace/captures/bablos79/bablos79-10447.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10448` | `bablos79` | `https://t.me/bablos79/10448` | `2026-05-07T18:51:32Z` | `2026-04-27T11:06:10+00:00` | `0149b7b2ee6d9efb9ca18961423c3f2dd0cd4370b1c695734d0863417d93575b` | `workspace/captures/bablos79/bablos79-10448.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10449` | `bablos79` | `https://t.me/bablos79/10449` | `2026-05-07T18:51:32Z` | `2026-04-27T11:09:24+00:00` | `72e56d34e32a4e31b0b02ea09c6457df57d825190b53483ecbe10f0557ac91a8` | `workspace/captures/bablos79/bablos79-10449.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10450` | `bablos79` | `https://t.me/bablos79/10450` | `2026-05-07T18:51:32Z` | `2026-04-27T11:16:37+00:00` | `f0de04a2127086f91c07862f86b26fe3568a1410c5ede6c824992f27d7f447d4` | `workspace/captures/bablos79/bablos79-10450.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10451` | `bablos79` | `https://t.me/bablos79/10451` | `2026-05-07T18:51:32Z` | `2026-04-27T11:23:25+00:00` | `6cae57c6496b8c2551106790e961ebc8854ee996b6683a048420dabd191b7f3d` | `workspace/captures/bablos79/bablos79-10451.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10452` | `bablos79` | `https://t.me/bablos79/10452` | `2026-05-07T18:51:32Z` | `2026-04-27T12:58:04+00:00` | `3a843c2ba81a9d72443a6c792b6b04741b02857052952b259a009c51d19e8754` | `workspace/captures/bablos79/bablos79-10452.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10453` | `bablos79` | `https://t.me/bablos79/10453` | `2026-05-07T18:51:32Z` | `2026-04-27T15:08:57+00:00` | `be89906be98d4bc265d665e31dfc6523a957f2d417925c14d195b5128831feae` | `workspace/captures/bablos79/bablos79-10453.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10454` | `bablos79` | `https://t.me/bablos79/10454` | `2026-05-07T18:51:32Z` | `2026-04-27T15:26:58+00:00` | `6a62902462312b50342e131ddfce6a815df27f781ca51b6e97e32aaf54239cbd` | `workspace/captures/bablos79/bablos79-10454.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10455` | `bablos79` | `https://t.me/bablos79/10455` | `2026-05-07T18:51:32Z` | `2026-04-27T15:40:05+00:00` | `29a9f48d84913fa017f621e4e00216d3629426f24ac10388387ede56f2d75291` | `workspace/captures/bablos79/bablos79-10455.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10456` | `bablos79` | `https://t.me/bablos79/10456` | `2026-05-07T18:51:32Z` | `2026-04-27T16:15:32+00:00` | `4f57ce3fde201a68de82ce2b258f8a963b988f08b4bdeec0169de3b3a32aaae7` | `workspace/captures/bablos79/bablos79-10456.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10457` | `bablos79` | `https://t.me/bablos79/10457` | `2026-05-07T18:51:32Z` | `2026-04-28T06:05:11+00:00` | `981135b1151f5e7ade7a45b77974d91953e6df0a743783f576d0d66bdec68650` | `workspace/captures/bablos79/bablos79-10457.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10458` | `bablos79` | `https://t.me/bablos79/10458` | `2026-05-07T18:51:32Z` | `2026-04-28T06:35:35+00:00` | `314619c54cb8df0aad973401084b0a32c0ba2b8282c2be4c5f9f04a2e3014330` | `workspace/captures/bablos79/bablos79-10458.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10459` | `bablos79` | `https://t.me/bablos79/10459` | `2026-05-07T18:51:32Z` | `2026-04-28T06:44:46+00:00` | `5e4d38246fc612f4537539c758291acbd91d2c0763e6d0c9b9ca8414be95b471` | `workspace/captures/bablos79/bablos79-10459.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10460` | `bablos79` | `https://t.me/bablos79/10460` | `2026-05-07T18:51:32Z` | `2026-04-28T06:54:17+00:00` | `2994d72d218ae1ae294241527ae0c863c958b4e292dd68dfbd86ad9cd0d5c360` | `workspace/captures/bablos79/bablos79-10460.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10461` | `bablos79` | `https://t.me/bablos79/10461` | `2026-05-07T18:51:32Z` | `2026-04-28T07:18:30+00:00` | `bcd28f0ae86c9e4e82c2c26e1886c87ae367f0c0862f4126fe4d36cb98d6eb16` | `workspace/captures/bablos79/bablos79-10461.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10463` | `bablos79` | `https://t.me/bablos79/10463` | `2026-05-07T18:51:32Z` | `2026-04-28T14:16:30+00:00` | `587105d1433275166f7d649a4d16bbbaaa90c2639760f42c012d6ff19348a8e6` | `workspace/captures/bablos79/bablos79-10463.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10464` | `bablos79` | `https://t.me/bablos79/10464` | `2026-05-07T18:51:32Z` | `2026-04-28T16:04:15+00:00` | `375b7806d8438cd0f640e31038bb0a6e8366ace2d11d51d60f9b9c527201ff4e` | `workspace/captures/bablos79/bablos79-10464.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10465` | `bablos79` | `https://t.me/bablos79/10465` | `2026-05-07T18:51:32Z` | `2026-04-29T07:30:41+00:00` | `b26087182a1d71069e57e2dd5e739c9427414e5f96934fd3a037b07e1dc966c2` | `workspace/captures/bablos79/bablos79-10465.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10466` | `bablos79` | `https://t.me/bablos79/10466` | `2026-05-07T18:51:32Z` | `2026-04-29T09:31:05+00:00` | `22a52915b201add32224fe70b2d4bd20f51b5b25d0a1443d0d17e3066e5bda0b` | `workspace/captures/bablos79/bablos79-10466.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10467` | `bablos79` | `https://t.me/bablos79/10467` | `2026-05-07T18:51:32Z` | `2026-04-29T09:44:27+00:00` | `81cc2fcf0ddacc3511b991e6e3953235fbc452dc4001a893a94fd91c73e25410` | `workspace/captures/bablos79/bablos79-10467.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10468` | `bablos79` | `https://t.me/bablos79/10468` | `2026-05-07T18:51:32Z` | `2026-04-29T10:10:07+00:00` | `c89e9cd6a04c988cdd6ed2efb30505cb64536a894fbc4c559932431cec027298` | `workspace/captures/bablos79/bablos79-10468.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10469` | `bablos79` | `https://t.me/bablos79/10469` | `2026-05-07T18:51:32Z` | `2026-04-29T10:34:29+00:00` | `0b5aa688f63697610fe62dc5c368856762d9541ed17e475691785255add216ee` | `workspace/captures/bablos79/bablos79-10469.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10470` | `bablos79` | `https://t.me/bablos79/10470` | `2026-05-07T18:51:32Z` | `2026-04-29T10:49:41+00:00` | `54790a51f20dc62a35d9c1c5d267ac627302015633850a412b362e860a12960d` | `workspace/captures/bablos79/bablos79-10470.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10471` | `bablos79` | `https://t.me/bablos79/10471` | `2026-05-07T18:51:32Z` | `2026-04-29T12:13:40+00:00` | `e5d93244a7998d1c34889d863e3c164f95c22e29b828021962cfd1a1f6030c84` | `workspace/captures/bablos79/bablos79-10471.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10472` | `bablos79` | `https://t.me/bablos79/10472` | `2026-05-07T18:51:32Z` | `2026-04-29T13:40:03+00:00` | `1ee4fcb3aa2f8026adb30e4fc0f9b7af506f1dc17e63e267be4bba931be17ea0` | `workspace/captures/bablos79/bablos79-10472.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10475` | `bablos79` | `https://t.me/bablos79/10475` | `2026-05-07T18:51:32Z` | `2026-04-29T18:36:49+00:00` | `dce8cdd67a81f02d5173f19b90cb8f9298afc16180edd64be985a10629fb27ae` | `workspace/captures/bablos79/bablos79-10475.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10476` | `bablos79` | `https://t.me/bablos79/10476` | `2026-05-07T18:51:32Z` | `2026-04-30T07:34:30+00:00` | `fced0cd89e597531ae3082941397f7c9f0804a1b41779edfea295cb55c95b4fe` | `workspace/captures/bablos79/bablos79-10476.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10477` | `bablos79` | `https://t.me/bablos79/10477` | `2026-05-07T18:51:32Z` | `2026-04-30T07:57:35+00:00` | `4029171bf7202547ef279d8a62e02cd80abc139fd2c93a6dac24b7770315b563` | `workspace/captures/bablos79/bablos79-10477.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10478` | `bablos79` | `https://t.me/bablos79/10478` | `2026-05-07T18:51:32Z` | `2026-04-30T09:46:50+00:00` | `bcccb754e9c8fec7d32e8c2ea9852c2b24667fd490edd8863c232ee302c96718` | `workspace/captures/bablos79/bablos79-10478.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10479` | `bablos79` | `https://t.me/bablos79/10479` | `2026-05-07T18:51:32Z` | `2026-04-30T10:42:21+00:00` | `da772f0d9e752d072dddf0f41915513405e67cc67202c3ec35019d381e655b8c` | `workspace/captures/bablos79/bablos79-10479.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10482` | `bablos79` | `https://t.me/bablos79/10482` | `2026-05-07T18:51:32Z` | `2026-05-02T06:42:00+00:00` | `a4b8fd5c114751814fcfe35e3a5fc6e15b9e9d92996a7216a10887d3a669c24f` | `workspace/captures/bablos79/bablos79-10482.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10483` | `bablos79` | `https://t.me/bablos79/10483` | `2026-05-07T18:51:32Z` | `2026-05-02T13:00:12+00:00` | `5667c87486143ec8e10631c52de30e2ba5219d6f6550de9829e60bb917287a32` | `workspace/captures/bablos79/bablos79-10483.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10485` | `bablos79` | `https://t.me/bablos79/10485` | `2026-05-07T18:51:32Z` | `2026-05-04T08:13:14+00:00` | `30cd37eac992847668be9edd79d432a78aad9e7e7819312a3d1cd1a168629645` | `workspace/captures/bablos79/bablos79-10485.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10486` | `bablos79` | `https://t.me/bablos79/10486` | `2026-05-07T18:51:32Z` | `2026-05-04T09:20:20+00:00` | `664beec95f743f383930f568f677d93b233b54d06ef24d16d2b19547df789fd0` | `workspace/captures/bablos79/bablos79-10486.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10487` | `bablos79` | `https://t.me/bablos79/10487` | `2026-05-07T18:51:32Z` | `2026-05-04T11:05:13+00:00` | `cfaad0156d0f44ee79710ad5d08ca07546672797fbe59fe8032998cb94ffe9a0` | `workspace/captures/bablos79/bablos79-10487.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10488` | `bablos79` | `https://t.me/bablos79/10488` | `2026-05-07T18:51:32Z` | `2026-05-04T11:13:39+00:00` | `23ca9bd011c477dd2be12f72f5402757e81bb2c7bda84cfade4c305e5736362d` | `workspace/captures/bablos79/bablos79-10488.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10489` | `bablos79` | `https://t.me/bablos79/10489` | `2026-05-07T18:51:32Z` | `2026-05-04T12:45:53+00:00` | `d49d71e85992e6da607784cc21fd15c1fa999d194e26fa2ac187bd3aaf066fbf` | `workspace/captures/bablos79/bablos79-10489.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10490` | `bablos79` | `https://t.me/bablos79/10490` | `2026-05-07T18:51:32Z` | `2026-05-04T13:56:36+00:00` | `683f1e126ea775817f58016fe45d22ef07d1cce3ee2a4b9bec64bbea2e17b008` | `workspace/captures/bablos79/bablos79-10490.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10491` | `bablos79` | `https://t.me/bablos79/10491` | `2026-05-07T18:51:32Z` | `2026-05-04T14:33:46+00:00` | `24f1b54621d697fb0de9461c36f599d1604645fe7610caa79989da3c237b066e` | `workspace/captures/bablos79/bablos79-10491.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10492` | `bablos79` | `https://t.me/bablos79/10492` | `2026-05-07T18:51:32Z` | `2026-05-04T15:20:20+00:00` | `83b4068532e725a76133aa315f663dcfdb82effc7d62725a52215e550c15ec46` | `workspace/captures/bablos79/bablos79-10492.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10493` | `bablos79` | `https://t.me/bablos79/10493` | `2026-05-07T18:51:32Z` | `2026-05-04T16:11:44+00:00` | `34e43305e8f08d4a1e3551e4855ca41ca86d39dbecd1f88f773648862b16bca6` | `workspace/captures/bablos79/bablos79-10493.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10495` | `bablos79` | `https://t.me/bablos79/10495` | `2026-05-07T18:51:32Z` | `2026-05-05T05:06:35+00:00` | `7544545bea2fccbf781da94d9c908d757013464cd17bf9c2c68f8d287fea82ba` | `workspace/captures/bablos79/bablos79-10495.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10496` | `bablos79` | `https://t.me/bablos79/10496` | `2026-05-07T18:51:32Z` | `2026-05-05T07:11:04+00:00` | `8a182b4496f304dc9675a3181be7052000305da5419ec11e53ac3c70cf91f31d` | `workspace/captures/bablos79/bablos79-10496.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10497` | `bablos79` | `https://t.me/bablos79/10497` | `2026-05-07T18:51:32Z` | `2026-05-05T08:06:18+00:00` | `0167db24e8bf4e9e016c5cbf4da9f00342263525bda1fa8980f1ef216eaa8ed5` | `workspace/captures/bablos79/bablos79-10497.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10498` | `bablos79` | `https://t.me/bablos79/10498` | `2026-05-07T18:51:32Z` | `2026-05-05T08:25:36+00:00` | `627ad313c6a7a1a67498b5f096741bc767c3c6023e21a07627531a4bf9ee9415` | `workspace/captures/bablos79/bablos79-10498.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10499` | `bablos79` | `https://t.me/bablos79/10499` | `2026-05-07T18:51:32Z` | `2026-05-05T08:31:27+00:00` | `884b974dda969c24208324a6ca27a3e6274e44485a389ab5dd107816c6f0cb51` | `workspace/captures/bablos79/bablos79-10499.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10500` | `bablos79` | `https://t.me/bablos79/10500` | `2026-05-07T18:51:32Z` | `2026-05-05T12:43:44+00:00` | `d83aa742b3b62cc11c256c20b1e48388d4a3f2cddfcef217d0339fce9d339dbb` | `workspace/captures/bablos79/bablos79-10500.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10501` | `bablos79` | `https://t.me/bablos79/10501` | `2026-05-07T18:51:32Z` | `2026-05-05T12:55:18+00:00` | `ab0d4d95c21c133f8fa8faa77e3be944d0dc1bd153bed5c069182d645dd341fd` | `workspace/captures/bablos79/bablos79-10501.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10502` | `bablos79` | `https://t.me/bablos79/10502` | `2026-05-07T18:51:32Z` | `2026-05-05T13:15:14+00:00` | `53150f5b948c504706a6341bf2bc83c4f5fb05ae3b79f362d65909f187dbd1fa` | `workspace/captures/bablos79/bablos79-10502.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10503` | `bablos79` | `https://t.me/bablos79/10503` | `2026-05-07T18:51:32Z` | `2026-05-05T13:16:37+00:00` | `19b3a107864a752f4f13395a96ae49e47a32d9c7a71a54f78fa25649dac453e7` | `workspace/captures/bablos79/bablos79-10503.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10504` | `bablos79` | `https://t.me/bablos79/10504` | `2026-05-07T18:51:32Z` | `2026-05-05T15:29:49+00:00` | `fb3f5b4c48c0909d6d869a5349ec07e1733d07a94f35e9722e036438c406c299` | `workspace/captures/bablos79/bablos79-10504.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10505` | `bablos79` | `https://t.me/bablos79/10505` | `2026-05-07T18:51:32Z` | `2026-05-05T18:21:20+00:00` | `072ba1c45b4f5a50ee655c6e3d86484ca1238e3237105bbf17259568463ae545` | `workspace/captures/bablos79/bablos79-10505.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10506` | `bablos79` | `https://t.me/bablos79/10506` | `2026-05-07T18:51:32Z` | `2026-05-06T06:15:03+00:00` | `d6878e9eb042da2aa11fe3e13d5827482da014176a6e8d6a27820a5cff3d5d2e` | `workspace/captures/bablos79/bablos79-10506.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10507` | `bablos79` | `https://t.me/bablos79/10507` | `2026-05-07T18:51:32Z` | `2026-05-06T06:27:27+00:00` | `6e8bdea5257f67dfdc94a2fd5210b75bcc929eb45197513c5ef5f71c6b746617` | `workspace/captures/bablos79/bablos79-10507.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
| `bablos79-10508` | `bablos79` | `https://t.me/bablos79/10508` | `2026-05-07T18:51:32Z` | `2026-05-06T06:57:32+00:00` | `64110f41bea0d2341261991d60d733023f5f67a415f68fe33bc11de8076f7ede` | `workspace/captures/bablos79/bablos79-10508.json` | `captured` | - | Public unauthenticated Telegram `/s/` HTML capture. |
## Target For First Batch

Target from `docs/pilot/PILOT_SCOPE.md`: collect enough public text to support
30-50 defensible signal records where available, with 40 as the working target.

This capture pass collected 60 public text posts. Manual extraction must now
determine how many are defensible signal candidates. For later batches, prefer
the most recent public posts and move backward until one of these is true:

- 30-50 defensible signal candidates are available;
- the bounded window is exhausted;
- the source proves mostly ambiguous, screenshot-only, deleted, or
  insufficient-text;
- a legal/public-source boundary blocks further capture.

## Handoff To Extraction

`SAS-PILOT-004` may continue manual extraction now. There are 60 `captured`
rows under `workspace/captures/bablos79/`; extraction must not approve records
without human review and complete signal fields.
