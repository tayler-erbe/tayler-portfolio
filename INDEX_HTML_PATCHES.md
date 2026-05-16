# `index.html` Patches

Two small edits to make to `index.html`. Both are paste-ins — no full-file rewrite needed.

---

## Patch 1 — Add new project card #09

Add this as a new project card in your projects grid. Place it **after** your current last project (whatever has the highest number — looks like #08 in our notes). Match the surrounding card's exact opening/closing structure; this snippet uses the same component classes and inline-style patterns visible in your existing case-study pages.

```html
<!-- PROJECT 09 — Performance Engineering / vLLM Throughput -->
<a href="vllm-inference-throughput-evaluation.html" class="project-card">
  <div class="project-num">09</div>
  <div class="project-title">vLLM vs Ollama <span>Throughput Evaluation</span></div>
  <div class="project-subtitle">Performance Engineering · LLaVA Inference · NVIDIA L4</div>
  <p class="project-desc">
    A controlled performance characterization of a production image-classification pipeline on a single NVIDIA L4 GPU.
    Diagnosed request serialization in Ollama and recovered <strong>6.22× throughput</strong> by migrating to vLLM
    continuous batching — taking a 12,125-image corpus from 22 hours to 3.7 hours on the same hardware and same model.
  </p>
  <div class="project-meta">
    <span>2026</span>
    <span>Performance Engineering</span>
    <span>GPU Inference</span>
  </div>
  <div class="project-tags">
    <span class="chip chip-accent">vLLM</span>
    <span class="chip chip-accent">LLaVA</span>
    <span class="chip">NVIDIA L4</span>
    <span class="chip">Continuous Batching</span>
    <span class="chip">Throughput Characterization</span>
  </div>
</a>
```

> **Note:** I do not know the exact class names you use on the projects grid. Open `index.html`, find the markup for one of your existing project cards (e.g. project #04 archival image), and **copy its outer wrapper structure** — then drop the *content* from this snippet inside that structure. The text strings and link target (`vllm-inference-throughput-evaluation.html`) are what matter; the class names should match whatever pattern you already have.

---

## Patch 2 — Light update to project #04 card (Archival Image Intelligence)

Two micro-edits to the existing project #04 card:

### 2a. Stat update inside the card

If the card currently shows `10,000+ images` (or similar), change it to:

```
12,125 archival images
```

### 2b. Add a one-line "See also" link

Inside the #04 card's body (just before the closing tag of the card wrapper, or wherever feels natural alongside its existing tags/meta), add:

```html
<div class="project-see-also" style="margin-top:0.75rem; font-family:'DM Mono',monospace; font-size:0.7rem; letter-spacing:0.08em; text-transform:uppercase; color:var(--accent2);">
  See also: Performance Engineering Deep-Dive →
</div>
```

This is intentionally **not a separate `<a>` tag** because the entire project card is presumably already a link to `archival-image-intelligence.html`. The archival case study page itself contains the link to the new throughput case study (added in the hero and in a dedicated new section toward the end), so users following the trail naturally land there.

---

## Patch 3 — (Optional) Update card tags on #04

If project #04's card has a tag/chip row, you can add one of these to advertise the new capability:

```html
<span class="chip chip-accent">vLLM</span>
```

or simply

```html
<span class="chip">Throughput-Optimized</span>
```

---

## Files to commit

Once patched, the deliverables to commit to `tayler-portfolio` are:

1. `archival-image-intelligence.html` — updated (replace existing)
2. `vllm-inference-throughput-evaluation.html` — new
3. `docs/charts/01_throughput_scaling.png` — new (referenced by case study)
4. `docs/charts/02_gpu_utilization.png` — new
5. `docs/charts/03_latency_inflation.png` — new
6. `docs/charts/04_corpus_time.png` — new
7. `index.html` — patched per above

The new case study references the charts at relative path `docs/charts/0X_<name>.png`, so they need to be in a `docs/charts/` subfolder alongside the HTML files. (Same chart files that are already in the `llava-vision-inference-backend-throughput-evaluation` repo at `docs/charts/`.)
