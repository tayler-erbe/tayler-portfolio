/* Results explorer for document-intelligence-evaluation.html.
   Reads aggregate rows only (assets/document-intelligence/benchmark.json): no inference, no uploads, no per-case output.
   Colours and fonts come from the classes in the page's stylesheet, never from this script. */
'use strict';
(function () {
  const $ = id => document.getElementById(id);
  const tasks = {
    ocr_crop: { name: 'Prose crop OCR', metric: 'Character error', lower: true, note: '50 prose crops per configuration. Character error is pooled over cases; numeric recall and failure counts are reported separately.' },
    table: { name: 'Table transcription', metric: 'TEDS', lower: false, note: 'Table structure similarity, not proof of correct amounts. Development uses 60 tables; confirmation v1 uses 159. Variants without a significant paired difference are candidates, not winners.' },
    chart_qa: { name: 'Chart questions', metric: 'Relaxed accuracy', lower: false, note: 'ChartQA reference matching with a 5% numeric tolerance. Development uses 200 questions; several questions can share one chart, so rows are not independent documents.' },
    chart_table: { name: 'Chart to table', metric: 'Value recall', lower: false, note: '60 chart-to-table cases. Gold values are matched within 5%; value recall is not question answering accuracy.' },
    page_text: { name: 'Whole-page text', metric: 'Word F1', lower: false, note: 'Word overlap is not semantic accuracy or reading order. Layout masking is experimental: on the desktop confirmation pages it raised word F1 and lowered numeric recall.' }
  };
  let data = null, current = [];
  const percent = n => Number.isFinite(n) ? (100 * n).toFixed(1) + '%' : '—';
  const scoreText = r => (r.task === 'ocr_crop' || r.task === 'chart_qa') ? percent(r.score) : r.score.toFixed(3);
  const node = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; };
  const cell = (tr, content, cls) => { const td = node('td', cls); if (content instanceof Node) td.append(content); else td.textContent = content; tr.append(td); return td; };
  const state = () => ({ task: $('di-task').value, side: $('di-side').value, split: $('di-split').value, variant: $('di-variant').value });
  const num = v => (v === '' || v === null || v === undefined) ? NaN : Number(v);

  function render() {
    if (!data) return;
    const s = state(), t = tasks[s.task];
    current = data.rows
      .filter(r => r.task === s.task && (s.side === 'all' || r.side === s.side) && r.split === s.split && (s.variant === 'all' || r.variant === s.variant))
      .sort((a, b) => t.lower ? a.score - b.score : b.score - a.score);
    $('di-metric').textContent = t.metric.toUpperCase() + ' / ' + (t.lower ? 'LOWER' : 'HIGHER') + ' IS BETTER';
    $('di-score-col').textContent = t.metric;
    $('di-title').textContent = t.name;
    $('di-notice').textContent = t.note
      + (s.side === 'all' ? ' Both-machine views mix hardware and runtime; the 8B weights differ between machines.' : '')
      + (s.split === 'confirmation v2' ? ' Round-2 page scores come from the routing report; latencies and failure counts it does not report are left blank.' : '');
    const chart = $('di-bars'), body = $('di-rows');
    chart.replaceChildren(); body.replaceChildren();
    if (!current.length) chart.append(node('p', 'di-empty', 'No recorded configuration matches these filters. An absent result is a run that was not made, not a failure.'));
    const max = t.lower ? Math.max(...current.map(r => r.score), 0.001) : 1;
    for (const r of current) {
      const row = node('div', 'di-bar-row');
      const label = node('div', 'di-bar-label', r.model);
      label.append(node('small', '', r.side + ' / ' + r.variant));
      const track = node('div', 'di-bar-track');
      const fill = node('div', 'di-bar-fill');
      fill.style.width = Math.max(0.5, r.score / max * 100) + '%';
      track.append(fill);
      row.append(label, track, node('div', 'di-bar-value', scoreText(r)));
      chart.append(row);
      const tr = node('tr');
      const name = node('span', '', r.model);
      name.append(node('small', 'di-sub', r.side + ' / ' + r.variant));
      cell(tr, name);
      cell(tr, scoreText(r), 'num');
      cell(tr, r.cases + ' / ' + (r.failed === null || r.failed === undefined ? '—' : r.failed), 'num');
      cell(tr, percent(num(r.numeric_recall)), 'num');
      cell(tr, Number.isFinite(num(r.median_seconds)) ? num(r.median_seconds).toFixed(2) + ' s' : '—', 'num');
      body.append(tr);
    }
    $('di-count').textContent = current.length + ' configuration' + (current.length === 1 ? '' : 's') + ' / ' + s.split + ' / bar length is the metric, not a normalised quality score';
  }

  function csv() {
    if (!current.length) { $('di-notice').textContent = 'Nothing in this view to export. Change the filters first.'; return; }
    const cols = ['model', 'model_id', 'side', 'variant', 'task', 'split', 'metric', 'score', 'cases', 'failed', 'numeric_recall', 'numeric_precision', 'median_seconds', 'source'];
    const q = v => '"' + String(v ?? '').replaceAll('"', '""') + '"';
    const text = [cols.map(q).join(','), ...current.map(r => cols.map(c => q(r[c])).join(','))].join('\r\n');
    const url = URL.createObjectURL(new Blob([text], { type: 'text/csv;charset=utf-8;' }));
    const a = node('a'); a.href = url; a.download = 'document-intelligence-' + $('di-task').value + '-' + $('di-side').value + '.csv'; a.click();
    setTimeout(() => URL.revokeObjectURL(url), 5000);
  }

  document.querySelectorAll('#di-filters select').forEach(e => e.addEventListener('change', render));
  $('di-reset').addEventListener('click', () => { $('di-filters').reset(); render(); });
  $('di-csv').addEventListener('click', csv);
  document.querySelectorAll('[data-di-preset]').forEach(a => a.addEventListener('click', e => {
    e.preventDefault();
    const p = a.dataset.diPreset;
    $('di-task').value = p;
    $('di-side').value = p === 'page_text' ? 'all' : 'laptop';
    $('di-split').value = p === 'page_text' ? 'confirmation v2' : 'development';
    $('di-variant').value = p === 'ocr_crop' ? 'baseline' : 'all';
    render();
    $('explorer').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
  }));

  fetch('assets/document-intelligence/benchmark.json')
    .then(r => { if (!r.ok) throw new Error('load'); return r.json(); })
    .then(d => { data = d; render(); })
    .catch(() => {
      $('di-notice').textContent = 'The aggregate data did not load. Serve the site over HTTP or use the downloads below.';
      $('di-bars').append(node('p', 'di-empty', 'Results are unavailable in this view.'));
    });
})();
