# ruff: noqa: E501
"""Static HTML review surface rendering."""

from __future__ import annotations

import json
from html import escape

from signal_sandbox.review.queue import ReviewQueueArtifact


def render_static_review_ui(queue: ReviewQueueArtifact) -> str:
    rows = [
        row.model_dump(mode="json")
        | {
            "asset_text": ", ".join(row.assets) if row.assets else "",
            "provider_status": "mapped" if row.provider else "missing",
        }
        for row in queue.rows
    ]
    payload = json.dumps(rows, ensure_ascii=False, sort_keys=True)
    channels = sorted({row.channel for row in queue.rows})
    decisions = sorted({row.current_decision for row in queue.rows})
    claim_types = sorted({row.suggested_claim_type for row in queue.rows})
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Three-Channel Review Queue</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #1f2933;
      --muted: #5b6776;
      --line: #c9d2dc;
      --fill: #f5f7fa;
      --accent: #0f766e;
      --warn: #9a3412;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font: 14px/1.45 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: white;
    }}
    header {{
      position: sticky;
      top: 0;
      z-index: 3;
      display: grid;
      gap: 10px;
      padding: 12px 16px;
      border-bottom: 1px solid var(--line);
      background: rgba(255,255,255,.96);
    }}
    h1 {{ margin: 0; font-size: 18px; letter-spacing: 0; }}
    .status {{ display: flex; flex-wrap: wrap; gap: 8px 16px; color: var(--muted); }}
    .filters {{
      display: grid;
      grid-template-columns: repeat(6, minmax(120px, 1fr));
      gap: 8px;
      align-items: end;
    }}
    label {{ display: grid; gap: 4px; color: var(--muted); font-size: 12px; }}
    select, input, textarea {{
      width: 100%;
      min-height: 34px;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 6px 8px;
      font: inherit;
      background: white;
      color: var(--ink);
    }}
    button {{
      min-height: 34px;
      border: 1px solid var(--accent);
      border-radius: 6px;
      padding: 6px 10px;
      font: inherit;
      background: var(--accent);
      color: white;
      cursor: pointer;
    }}
    main {{ display: grid; grid-template-columns: minmax(0, 1fr) 380px; min-height: calc(100vh - 126px); }}
    table {{ width: 100%; border-collapse: collapse; table-layout: fixed; }}
    th, td {{ border-bottom: 1px solid var(--line); padding: 8px; vertical-align: top; }}
    th {{ position: sticky; top: 126px; z-index: 2; background: var(--fill); text-align: left; }}
    td:nth-child(1) {{ width: 130px; }}
    td:nth-child(2) {{ width: 110px; }}
    td:nth-child(3) {{ width: 130px; }}
    .snippet {{ max-height: 86px; overflow: auto; }}
    .tag {{ display: inline-block; margin: 0 4px 4px 0; padding: 1px 5px; border-radius: 5px; background: var(--fill); color: var(--muted); }}
    aside {{ border-left: 1px solid var(--line); padding: 12px; background: #fbfcfd; }}
    .decision-form {{ display: grid; gap: 8px; position: sticky; top: 138px; }}
    textarea {{ min-height: 160px; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    a {{ color: var(--accent); overflow-wrap: anywhere; }}
    .warn {{ color: var(--warn); }}
    @media (max-width: 980px) {{
      .filters {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      main {{ grid-template-columns: 1fr; }}
      aside {{ border-left: 0; border-top: 1px solid var(--line); }}
      th {{ top: 212px; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Three-Channel Review Queue</h1>
    <div class="status">
      <span>{queue.summary["queue_rows_total"]} rows</span>
      <span>{queue.summary["pending_false_negative_rows"]} false negatives</span>
      <span>{queue.summary["provider_gap_rows"]} provider gaps</span>
      <span class="warn">external delivery blocked</span>
    </div>
    <div class="filters">
      <label>Channel <select id="channel">{_options(channels)}</select></label>
      <label>Claim type <select id="claimType">{_options(claim_types)}</select></label>
      <label>Asset <input id="asset" placeholder="BTC, SBER"></label>
      <label>Provider <select id="providerStatus"><option value="">All</option><option value="mapped">Mapped</option><option value="missing">Missing</option></select></label>
      <label>Review status <select id="reviewStatus">{_options(decisions)}</select></label>
      <button id="reset" type="button">Reset</button>
    </div>
  </header>
  <main>
    <section>
      <table>
        <thead>
          <tr><th>ID</th><th>Channel</th><th>Status</th><th>Normalized fields</th><th>Source text</th></tr>
        </thead>
        <tbody id="rows"></tbody>
      </table>
    </section>
    <aside>
      <form class="decision-form" id="decisionForm">
        <label>Queue row <input id="decisionQueueId" readonly></label>
        <label>Status <select id="decisionStatus"><option>accepted</option><option>false_positive</option><option>false_negative</option><option>needs_context</option><option>unsupported_provider</option><option>media_blocked</option></select></label>
        <label>Reviewer <input id="reviewer" value="operator"></label>
        <label>Reason <textarea id="reason" placeholder="Required reason"></textarea></label>
        <button type="submit">Add Decision</button>
        <label>Deterministic JSON artifact <textarea id="artifact" readonly></textarea></label>
        <label>Markdown export <textarea id="markdown" readonly></textarea></label>
      </form>
    </aside>
  </main>
  <script id="queue-data" type="application/json">{escape(payload)}</script>
  <script>
    const rows = JSON.parse(document.getElementById('queue-data').textContent);
    const decisions = [];
    const tbody = document.getElementById('rows');
    const fields = ['channel', 'claimType', 'asset', 'providerStatus', 'reviewStatus'];

    function currentFilters() {{
      return {{
        channel: document.getElementById('channel').value,
        claimType: document.getElementById('claimType').value,
        asset: document.getElementById('asset').value.trim().toUpperCase(),
        providerStatus: document.getElementById('providerStatus').value,
        reviewStatus: document.getElementById('reviewStatus').value
      }};
    }}
    function matches(row, filters) {{
      if (filters.channel && row.channel !== filters.channel) return false;
      if (filters.claimType && row.suggested_claim_type !== filters.claimType) return false;
      if (filters.providerStatus && row.provider_status !== filters.providerStatus) return false;
      if (filters.reviewStatus && row.current_decision !== filters.reviewStatus) return false;
      if (filters.asset && !row.assets.map(a => a.toUpperCase()).includes(filters.asset)) return false;
      return true;
    }}
    function render() {{
      const filters = currentFilters();
      const visible = rows.filter(row => matches(row, filters)).slice(0, 300);
      tbody.innerHTML = visible.map(row => `
        <tr data-id="${{row.queue_id}}">
          <td><button type="button" class="select-row">${{row.queue_id}}</button></td>
          <td>${{row.channel}}</td>
          <td><span class="tag">${{row.current_decision}}</span><span class="tag">${{row.provider_status}}</span></td>
          <td>${{row.suggested_claim_type}}<br>${{row.asset_text || 'no asset'}}<br>${{row.provider_symbol || 'no provider symbol'}}</td>
          <td><a href="${{row.source_url}}" target="_blank" rel="noreferrer">${{row.source_url}}</a><div class="snippet">${{escapeHtml(row.evidence_snippet)}}</div></td>
        </tr>`).join('');
    }}
    function selectRow(queueId) {{
      document.getElementById('decisionQueueId').value = queueId;
      const row = rows.find(item => item.queue_id === queueId);
      document.getElementById('reason').value = row ? row.blocker_reason : '';
    }}
    function buildDecisionArtifact() {{
      const ordered = [...decisions].sort((a, b) => a.decision_id.localeCompare(b.decision_id));
      return JSON.stringify({{ artifact_id: 'review_ui_decisions', decision_count: ordered.length, decisions: ordered }}, null, 2);
    }}
    function buildMarkdown() {{
      const ordered = [...decisions].sort((a, b) => a.decision_id.localeCompare(b.decision_id));
      const lines = ['# Review UI Decisions', '', '| decision_id | status | queue_id | source_url | reason |', '|---|---|---|---|---|'];
      ordered.forEach(row => lines.push('| `' + row.decision_id + '` | `' + row.status + '` | `' + row.queue_id + '` | ' + row.source_url + ' | ' + row.reason.replaceAll('|','/') + ' |'));
      return lines.join('\\n');
    }}
    function stableId(parts) {{
      let hash = 0;
      const text = parts.join('|');
      for (let i = 0; i < text.length; i++) hash = ((hash << 5) - hash + text.charCodeAt(i)) | 0;
      return 'review-ui-' + Math.abs(hash).toString(16).padStart(8, '0');
    }}
    function escapeHtml(value) {{
      return String(value).replace(/[&<>"']/g, char => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[char]));
    }}
    fields.forEach(id => document.getElementById(id).addEventListener('input', render));
    document.getElementById('reset').addEventListener('click', () => {{ fields.forEach(id => document.getElementById(id).value = ''); render(); }});
    tbody.addEventListener('click', event => {{ if (event.target.classList.contains('select-row')) selectRow(event.target.textContent); }});
    document.getElementById('decisionForm').addEventListener('submit', event => {{
      event.preventDefault();
      const queueId = document.getElementById('decisionQueueId').value;
      const row = rows.find(item => item.queue_id === queueId);
      if (!row) return;
      const status = document.getElementById('decisionStatus').value;
      const reviewer = document.getElementById('reviewer').value.trim();
      const reason = document.getElementById('reason').value.trim();
      if (!reviewer || !reason) return;
      decisions.push({{
        decision_id: stableId([queueId, status, reviewer, reason]),
        queue_id: queueId,
        claim_id: row.claim_id || queueId,
        status,
        reviewer,
        reviewed_at_utc: new Date().toISOString(),
        source_url: row.source_url,
        evidence_span: {{ source_document_id: String(row.source_post_id), start_char: 0, end_char: row.evidence_snippet.length, excerpt: row.evidence_snippet }},
        reason
      }});
      document.getElementById('artifact').value = buildDecisionArtifact();
      document.getElementById('markdown').value = buildMarkdown();
    }});
    render();
  </script>
</body>
</html>
"""


def _options(values: list[str]) -> str:
    return '<option value="">All</option>' + "".join(
        f'<option value="{escape(value)}">{escape(value)}</option>' for value in values
    )
