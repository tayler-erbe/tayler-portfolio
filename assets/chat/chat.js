/*! Ask about Tayler: a static search over pre-written answer cards.
 * No AI runs here. No server, no API key, no cookies, no storage, no tracking, no external requests.
 * The only network request is kb.json, fetched from the same folder as this script, the first time the panel opens.
 * Retrieval: text normalisation, an alias table, fuzzy correction of typos, BM25 over each card's question variants,
 * title, tags and answer, plus a best-matching-variant coverage score, with a confidence threshold.
 */
(function () {
  "use strict";

  // ------------------------------------------------------------------ engine (pure; also used by the tests)
  var W_Q = 3, W_TITLE = 2, W_TAGS = 2, W_ANS = 1, K1 = 1.2, B = 0.75;
  // words that say how she feels about a thing, not what the thing is: a match on these alone is never an answer
  // ("favorite burrito" must not answer with the favorite-bands card when no card mentions burritos)
  var GENERIC = { favorite: 1, favourite: 1, fav: 1, like: 1, love: 1, best: 1, type: 1, kind: 1, prefer: 1, enjoy: 1, thing: 1, most: 1 };
  var MIN_COVER = 0.4, MIN_SCORE = 2.5, RELATED_RATIO = 0.45, UNKNOWN_W = 0.6, ARTICLE_PRIOR = 0.7, ANSWER_CREDIT = 0.6;
  var PARENT_SLACK = 0.02, PARENT_RATIO = 0.3;   // see the parent rule in search()
  // meaning-based search (optional, loaded lazily): BM25 answers alone when it is sure (exact phrasing, or a confident match with
  // cover >= GATE_COVER and score >= GATE_SCORE); otherwise BM25 and embedding scores are fused. Tuned on the blind dev half only.
  var HYBRID_W = 0.5, GATE_COVER = 0.7, GATE_SCORE = 25, EMB_TAU = 0.75, EMB_FLOOR = 0.3, H_PARENT_RATIO = 0.9, AGREE_K = 3;

  function fold(s) {
    s = String(s || "").toLowerCase();
    if (s.normalize) s = s.normalize("NFKD").replace(/[̀-ͯ]/g, "");
    return s.replace(/[‘’ʼ`']/g, "").replace(/[“”"]/g, " ");
  }
  function rawTokens(s) {
    return fold(s).replace(/[^a-z0-9.+#]+/g, " ").split(" ")
      .map(function (t) { return t.replace(/^\.+|\.+$/g, ""); })
      .filter(function (t) { return t.length > 0; });
  }
  function stem(t) {
    if (/^\d/.test(t) || t.length <= 3) return t;
    if (/ies$/.test(t) && t.length > 4) return t.slice(0, -3) + "y";
    if (/sses$/.test(t)) return t.slice(0, -2);
    if (/ss$/.test(t) || /us$/.test(t) || /is$/.test(t)) return t;
    if (/ing$/.test(t) && t.length > 5) return t.slice(0, -3);
    if (/ed$/.test(t) && t.length > 4) return t.slice(0, -2);
    if (/s$/.test(t)) return t.slice(0, -1);
    return t;
  }
  function editDistance(a, b, max) {            // Damerau (optimal string alignment), early exit above max
    if (Math.abs(a.length - b.length) > max) return max + 1;
    var d = [], i, j;
    for (i = 0; i <= a.length; i++) { d[i] = [i]; }
    for (j = 0; j <= b.length; j++) { d[0][j] = j; }
    for (i = 1; i <= a.length; i++) {
      var rowMin = max + 1;
      for (j = 1; j <= b.length; j++) {
        var c = a[i - 1] === b[j - 1] ? 0 : 1;
        d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + c);
        if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) d[i][j] = Math.min(d[i][j], d[i - 2][j - 2] + 1);
        if (d[i][j] < rowMin) rowMin = d[i][j];
      }
      if (rowMin > max) return max + 1;
    }
    return d[a.length][b.length];
  }

  function Engine(kb, opts) {
    var self = this;
    this.kb = kb;
    this.opt = { minCover: MIN_COVER, minScore: MIN_SCORE, unknownW: UNKNOWN_W, articlePrior: ARTICLE_PRIOR,
                 parentSlack: PARENT_SLACK, parentRatio: PARENT_RATIO,
                 hybridW: HYBRID_W, gateCover: GATE_COVER, gateScore: GATE_SCORE, embTau: EMB_TAU, embFloor: EMB_FLOOR,
                 hParentRatio: H_PARENT_RATIO, agreeK: AGREE_K };
    if (opts) for (var o in opts) this.opt[o] = opts[o];
    this.stop = {};
    (kb.stopwords || []).forEach(function (w) { self.stop[w] = 1; });
    // alias table: phrase (as stemmed tokens joined by space) -> list of canonical tokens
    this.alias = {}; this.maxPhrase = 1;
    (kb.synonyms || []).forEach(function (group) {
      var canon = "#" + rawTokens(group[0]).map(stem).join("_");
      group.forEach(function (term) {
        var key = rawTokens(term).map(stem).join(" ");
        if (!key) return;
        (self.alias[key] = self.alias[key] || []).indexOf(canon) < 0 && self.alias[key].push(canon);
        self.maxPhrase = Math.max(self.maxPhrase, key.split(" ").length);
      });
    });
    this.vocab = {};
    this.docs = kb.cards.map(function (card) {
      var f = {
        q: [].concat.apply([], (card.questions || []).map(function (q) { return self.analyze(q, false); })),
        title: self.analyze(card.title, false),
        tags: [].concat.apply([], (card.tags || []).map(function (t) { return self.analyze(t, false); })),
        ans: self.analyze(card.answer || "", false)
      };
      // nocanon: alias groups this card must not join ("email" in an email-archiving card is not a way to contact her)
      var drop = {};
      if (card.nocanon && card.nocanon.length) {
        card.nocanon.forEach(function (g) { drop["#" + rawTokens(g).map(stem).join("_")] = 1; });
        Object.keys(f).forEach(function (k) { f[k] = f[k].filter(function (t) { return !drop[t]; }); });
      }
      var tf = {}, len = 0;
      function add(list, w) { list.forEach(function (t) { tf[t] = (tf[t] || 0) + w; len += w; }); }
      add(f.q, W_Q); add(f.title, W_TITLE); add(f.tags, W_TAGS); add(f.ans, W_ANS);
      var keys = {};                               // terms in the questions, title and tags count fully; answer-only terms count 0.6
      f.ans.forEach(function (t) { keys[t] = ANSWER_CREDIT; });
      f.q.concat(f.title, f.tags).forEach(function (t) { keys[t] = 1; });
      return { card: card, tf: tf, len: len, keys: keys, drop: drop,
               exact: (card.questions || []).map(function (q) { return rawTokens(q).join(" "); }) };
    });
    this.N = this.docs.length;
    this.avgLen = this.docs.reduce(function (s, d) { return s + d.len; }, 0) / Math.max(1, this.N);
    this.df = {};
    this.docs.forEach(function (d) { Object.keys(d.tf).forEach(function (t) { self.df[t] = (self.df[t] || 0) + 1; }); });
    Object.keys(this.df).forEach(function (t) { if (t.charAt(0) !== "#") self.vocab[t] = self.df[t]; });
  }
  function isTransposition(a, b) {
    var diff = [];
    for (var i = 0; i < a.length; i++) if (a[i] !== b[i]) diff.push(i);
    return diff.length === 2 && diff[1] === diff[0] + 1 && a[diff[0]] === b[diff[1]] && a[diff[1]] === b[diff[0]];
  }
  function dropsDouble(t, w) {                    // w is t with one copy of a doubled letter removed
    for (var i = 0; i + 1 < t.length; i++) if (t[i] === t[i + 1] && t.slice(0, i) + t.slice(i + 1) === w) return true;
    return false;
  }
  function uniq(a) { var s = {}, o = []; a.forEach(function (x) { if (!s[x]) { s[x] = 1; o.push(x); } }); return o; }

  // text -> units. A unit is one word or alias phrase: {raw: stemmed word or null, canons: ["#group", ...]}.
  // Stopwords keep a unit only when they belong to an alias phrase.
  Engine.prototype.units = function (text, isQuery) {
    var self = this, raw = rawTokens(text), out = [], i = 0;
    var toks = raw.map(function (r) {               // stopwords are checked on the raw word and on its stem
      var st = stem(r);
      if (self.stop[r]) return r;
      if (self.stop[st]) return st;
      return isQuery ? self.correct(st) : st;
    });
    while (i < toks.length) {
      var used = 0;
      for (var n = Math.min(this.maxPhrase, toks.length - i); n >= 2; n--) {
        var key = toks.slice(i, i + n).join(" ");
        if (this.alias[key]) {
          var raws = toks.slice(i, i + n).filter(function (t) { return !self.stop[t]; });
          out.push({ raw: raws.length ? raws.join(" ") : null, words: raws, canons: this.alias[key].slice() });
          used = n; break;
        }
      }
      if (used) { i += used; continue; }
      var t = toks[i];
      if (!this.stop[t] || this.alias[t]) out.push({ raw: this.stop[t] ? null : t, words: this.stop[t] ? [] : [t], canons: (this.alias[t] || []).slice() });
      i++;
    }
    return out;
  };
  // flattened terms for BM25: every word plus every canonical alias token
  Engine.prototype.analyze = function (text, isQuery) {
    var out = [];
    this.units(text, isQuery).forEach(function (u) { out.push.apply(out, u.words); out.push.apply(out, u.canons); });
    return out;
  };

  // fix a likely typo by the nearest known word: same first letter, 5+ letters, 1 edit (2 edits from 10 letters)
  Engine.prototype.correct = function (t) {
    if (!this.vocab || this.vocab[t] || this.alias[t] || this.stop[t] || t.length < 5 || /\d/.test(t)) return t;
    var max = t.length >= 10 ? 2 : 1, best = t, bestD = max + 1, bestDf = 0, cands = [];
    for (var v in this.vocab) cands.push([v, this.vocab[v]]);
    for (var k in this.alias) if (k.indexOf(" ") < 0) cands.push([k, 0.5]);
    for (var i = 0; i < cands.length; i++) {
      var w = cands[i][0];
      if (w.charAt(0) !== t.charAt(0) || Math.abs(w.length - t.length) > max) continue;
      if (t.length < 6 && w.length === t.length && !isTransposition(t, w)) continue;   // short words: no substitutions (stock is not stack)
      if (t.length < 6 && w.length < t.length && !dropsDouble(t, w)) continue;           // short words: drop only a doubled letter (chatt is chat, stock is not sock)
      var d = editDistance(t, w, max);
      if (d < bestD || (d === bestD && cands[i][1] > bestDf)) { best = w; bestD = d; bestDf = cands[i][1]; }
    }
    return bestD <= max ? best : t;
  };

  Engine.prototype.idf = function (t) {
    var df = this.df[t] || 0;
    return Math.log(1 + (this.N - df + 0.5) / (df + 0.5));
  };

  // kb_emb.bin (build_emb.py): uint32 header length, JSON header, uint16 owner[n], (pad), float32 scale[n], int8 vec[n*dim]
  Engine.prototype.setEmbeddings = function (buf) {
    var dv = new DataView(buf), hl = dv.getUint32(0, true);
    var head = JSON.parse(new TextDecoder().decode(new Uint8Array(buf, 4, hl)));
    var off = 4 + hl, n = head.n, dim = head.dim;
    var owners = new Uint16Array(buf.slice(off, off + 2 * n)); off += 2 * n; if (off % 4) off += 2;
    var scale = new Float32Array(buf.slice(off, off + 4 * n)); off += 4 * n;
    var vec = new Int8Array(buf, off, n * dim);
    var pos = {}, self = this;
    this.docs.forEach(function (d, i) { pos[d.card.id] = i; });
    var map = head.cards.map(function (id) { return pos[id] === undefined ? -1 : pos[id]; });   // header order -> doc index
    this.emb = { n: n, dim: dim, owner: owners, scale: scale, vec: vec, map: map, head: head };
    return head;
  };
  Engine.prototype.embScores = function (q) {      // max cosine over each card's vectors; q is a normalised Float32Array
    var e = this.emb, out = new Float32Array(this.docs.length).fill(-1);
    for (var i = 0; i < e.n; i++) {
      var d = e.map[e.owner[i]];
      if (d < 0) continue;
      var s = 0, base = i * e.dim;
      for (var k = 0; k < e.dim; k++) s += e.vec[base + k] * q[k];
      s *= e.scale[i] / 127;
      if (s > out[d]) out[d] = s;
    }
    return out;
  };
  Engine.prototype.agrees = function (id, qvec, k) {   // is BM25's card among the embedding's top k?
    if (!k) return false;
    var es = this._es || this.embScores(qvec), pos = -1, better = 0, i;
    this._es = es;
    for (i = 0; i < this.docs.length; i++) if (this.docs[i].card.id === id) { pos = i; break; }
    if (pos < 0) return false;
    for (i = 0; i < es.length; i++) if (es[i] > es[pos]) better++;
    return better < k;
  };
  Engine.prototype.hybrid = function (res, qvec) {
    this._es = null;
    var o = this.opt, top = res.top;
    if ((res.best && res.best.exact) || (top && (top.exact || (res.confident && top.cover >= o.gateCover && top.score >= o.gateScore)))) return res;   // BM25 is sure
    if (res.confident && top && this.agrees(top.card.id, qvec, o.agreeK)) return res;   // both searches agree on BM25's card
    if (!res.best && /\b(old|age|tall|height|weight|birthday)\b/.test(rawTokens(res.query).join(" "))) return res; // never guess personal details
    var es = this._es || this.embScores(qvec), order = [], i;
    for (i = 0; i < es.length; i++) order.push(i);
    order.sort(function (a, b) { return es[b] - es[a]; });
    order = order.slice(0, 30);
    var smax = es[order[0]], f = {}, byId = {}, maxBm = 0;
    (res.all || []).forEach(function (r) { if (r.score > maxBm) maxBm = r.score; });
    (res.all || []).forEach(function (r) { f[r.card.id] = o.hybridW * r.score / (maxBm || 1); byId[r.card.id] = r; });
    var self = this;
    order.forEach(function (j) {
      var c = self.docs[j].card;
      f[c.id] = (f[c.id] || 0) + (1 - o.hybridW) * Math.max(0, (es[j] - o.embFloor) / Math.max(1e-6, smax - o.embFloor));
      if (!byId[c.id]) byId[c.id] = { card: c, score: 0, cover: 0, exact: false, content: true };
    });
    var ids = Object.keys(f).sort(function (a, b) { return f[b] - f[a]; });
    var best = ids[0], par = best && byId[best].card.parent;
    if (par && f[par] !== undefined && f[par] >= o.hParentRatio * f[best]) best = par;   // a general question goes to the summary card
    var confident = res.confident || smax >= o.embTau;
    var related = ids.filter(function (id) { return id !== best && f[id] >= RELATED_RATIO * f[best]; }).slice(0, 2)
                     .map(function (id) { return byId[id]; });
    return { query: res.query, terms: res.terms, best: confident ? byId[best] : null, top: byId[best], related: related,
             confident: confident, mode: "hybrid", embTop: smax, ranked: ids.slice(0, 30).map(function (id) { return byId[id]; }) };
  };

  Engine.prototype.search = function (query, qvec) {
    var res = this.searchBm25(query);
    return qvec && this.emb ? this.hybrid(res, qvec) : res;
  };
  Engine.prototype.searchBm25 = function (query) {
    var self = this, qnorm = rawTokens(query).join(" ");
    var units = this.units(query, true);
    if (!units.length && /\b(who|you|your|yourself|she|her|tayler|erbe|taylor|tay|u|ur)\b/.test(qnorm) &&
        !/\b(old|age|tall|height|weight|birthday)\b/.test(qnorm)) {   // never guess personal details
      var about = this.docs.filter(function (d) { return d.card.id === "about"; })[0];
      if (about) return { query: query, terms: [], best: { card: about.card, score: 1, cover: 1, exact: true },
                          top: { card: about.card, score: 1, cover: 1 }, related: [], confident: true };
    }
    var terms = uniq(this.analyze(query, true));
    var known = terms.filter(function (t) { return self.df[t]; });
    // each unit's weight in the coverage score: its rarest known member, or the unknown-word weight (no card has it)
    var unknownIdf = this.idf("\u0000none"), qw = 0;
    units.forEach(function (u) {
      var members = u.words.concat(u.canons).filter(function (m) { return self.df[m]; });
      u.members = members;
      u.w = members.length ? Math.max.apply(null, members.map(function (m) { return self.idf(m); })) : self.opt.unknownW * unknownIdf;
      qw += u.w;
    });
    var wantsWriting = terms.indexOf("#medium") >= 0;
    var results = this.docs.map(function (d) {
      if (qnorm && d.exact.indexOf(qnorm) >= 0) return { card: d.card, score: 100, cover: 1, exact: true };
      // a query word that carries an alias group this card opted out of says nothing about this card
      // ("send her an email": "email" means contact, so an email-archiving card cannot claim it)
      var blocked = {};
      units.forEach(function (u) {
        if (u.canons.some(function (c) { return d.drop[c]; })) u.words.concat(u.canons).forEach(function (m) { blocked[m] = 1; });
      });
      var bm = 0;
      known.forEach(function (t) {
        if (blocked[t]) return;
        var f = d.tf[t] || 0;
        if (!f) return;
        bm += self.idf(t) * (f * (K1 + 1)) / (f + K1 * (1 - B + B * d.len / self.avgLen));
      });
      var cover = 0, content = false;
      if (qw > 0 && bm > 0) {
        var hit = 0;
        units.forEach(function (u) {
          // a unit counts when the card has one of its alias groups, or all of its words
          var best = 0;
          if (u.canons.some(function (c) { return d.drop[c]; })) { return; }
          u.canons.forEach(function (c) { if ((d.keys[c] || 0) > best) best = d.keys[c]; });
          if (u.words.length) {
            var all = Math.min.apply(null, u.words.map(function (w) { return d.keys[w] || 0; }));
            if (all > best) best = all;
          }
          hit += u.w * best;
          if (best > 0 && !u.words.concat(u.canons).every(function (m) { return GENERIC[m] || GENERIC[m.replace(/^#/, "")]; })) content = true;
        });
        cover = hit / qw;
      }
      var score = bm * (0.5 + cover);
      if (d.card.kind === "article" && !wantsWriting) score *= self.opt.articlePrior;   // a project card beats its article unless writing is asked for
      if (typeof d.card.prior === "number") score *= d.card.prior;   // e.g. her long own-words cards, so their answer text does not outrank a focused card
      return { card: d.card, score: score, cover: cover, exact: false, content: content };
    }).filter(function (r) { return r.score > 0; });
    results.sort(function (a, b) { return b.score - a.score; });
    // a focused card (e.g. "Book OCR: results") names its summary card as parent. When the parent covers the question as
    // well as the focused card does, the question was general: answer with the summary and offer the focused card as related.
    for (var hop = 0; hop < 2 && results.length && results[0].card.parent && !results[0].exact; hop++) {
      var kid = results[0], pid = kid.card.parent, pi = -1;
      for (var j = 1; j < results.length; j++) if (results[j].card.id === pid) { pi = j; break; }
      if (pi < 0 || results[pi].cover < kid.cover - this.opt.parentSlack || results[pi].score < this.opt.parentRatio * kid.score) break;
      var par = results.splice(pi, 1)[0];
      results.unshift(par);
    }
    var top = results[0];
    var confident = !!top && (top.exact || (top.content && top.cover >= this.opt.minCover && top.score >= this.opt.minScore));
    var related = [];
    if (top) {
      for (var i = 1; i < results.length && related.length < 2; i++) {
        if (results[i].score >= RELATED_RATIO * top.score && results[i].cover >= 0.3) related.push(results[i]);
      }
    }
    return { query: query, terms: terms, best: confident ? top : null, top: top || null,
             related: confident ? related : results.filter(function (r) { return r.content; }).slice(0, 2), confident: confident,
             ranked: results.slice(0, 30), all: results, mode: "bm25" };
  };

  // ------------------------------------------------------------------ UI
  var SCRIPT = document.currentScript;
  var SRC = SCRIPT && SCRIPT.src ? SCRIPT.src : "assets/chat/chat.js";
  var DATA_VERSION = "2026101903";                 // bump with every new kb.json, so a cached copy is never reused (no page edit needed)
  var VERSION = (SRC.split("?")[1] ? SRC.split("?")[1] + "&" : "") + "d=" + DATA_VERSION;   // chat.js?v=... passes v= on too
  var BASE = SRC.split("?")[0].replace(/[^\/]*$/, "");
  var KB_URL = BASE + "kb.json" + (VERSION ? "?" + VERSION : "");
  var EMB_URL = BASE + "kb_emb.bin" + (VERSION ? "?" + VERSION : "");
  // the in-browser sentence model: library from jsDelivr and model files from the Hugging Face hub, both pinned to exact
  // versions. The question is embedded on the visitor's device and never sent anywhere. If any of this fails (old phone,
  // offline, blocked CDN), the panel keeps using BM25 alone.
  var EMB_LIB = "https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.0.2/dist/transformers.min.js";
  var EMB_ON = true;
  var TEXT = {                                   // UI labels (functional, not prose); Tayler may change any of these
    bubble: "Ask about Tayler",
    title: "Ask about Tayler",
    sub: "(search over my work, not a live AI)",
    placeholder: "Type a question",
    send: "Ask",
    close: "Close",
    starters: "Try asking",
    related: "Related",
    loading: "Loading answers",
    failed: "The answers could not load.",
    you: "You asked"
  };
  var engine = null, loading = null, els = {}, embedder = null, embLoading = null, embState = "off";

  function h(tag, attrs, kids) {
    var e = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === "text") e.textContent = attrs[k];
      else if (k === "class") e.className = attrs[k];
      else if (k.slice(0, 2) === "on") e.addEventListener(k.slice(2), attrs[k]);
      else e.setAttribute(k, attrs[k]);
    });
    (kids || []).forEach(function (c) { if (c) e.appendChild(typeof c === "string" ? document.createTextNode(c) : c); });
    return e;
  }
  function icon(path) {
    var ns = "http://www.w3.org/2000/svg", s = document.createElementNS(ns, "svg");
    s.setAttribute("viewBox", "0 0 24 24"); s.setAttribute("aria-hidden", "true"); s.setAttribute("focusable", "false");
    var p = document.createElementNS(ns, "path"); p.setAttribute("d", path);
    p.setAttribute("fill", "none"); p.setAttribute("stroke", "currentColor"); p.setAttribute("stroke-width", "1.8");
    p.setAttribute("stroke-linecap", "square");
    s.appendChild(p); return s;
  }
  function safeUrl(u) {
    u = String(u || "");
    return /^(https:\/\/|mailto:|[a-z0-9_\-]+\.(html|pdf)(#[\w\-]*)?$|#)/i.test(u) ? u : "#";
  }
  function fmtDate(iso) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || "");
    if (!m) return "";
    var names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    return names[+m[2] - 1] + " " + (+m[3]) + ", " + m[1];
  }

  function loadEmbedder() {                       // lazy, non-blocking; resolves to the embed function or null
    if (embLoading) return embLoading;
    if (!EMB_ON || typeof WebAssembly !== "object" || typeof TextDecoder !== "function") { embState = "unsupported"; return (embLoading = Promise.resolve(null)); }
    embState = "loading";
    var dynImport = new Function("u", "return import(u)");   // keeps older parsers from failing on import()
    embLoading = load().then(function () {
      return Promise.all([dynImport(EMB_LIB), fetch(EMB_URL, { credentials: "omit", cache: "force-cache" })
        .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.arrayBuffer(); })]);
    }).then(function (x) {
      var lib = x[0], head = engine.setEmbeddings(x[1]);
      lib.env.allowLocalModels = false;
      lib.env.useBrowserCache = false;             // no Cache Storage: nothing is stored on the visitor's device
      return lib.pipeline("feature-extraction", head.model, { revision: head.revision, dtype: head.dtype || "q8" });
    }).then(function (fe) {
      embedder = function (q) {
        return fe(q, { pooling: "mean", normalize: true }).then(function (t) { return new Float32Array(t.data); });
      };
      embState = "ready";
      return embedder;
    }).catch(function () { embState = "failed"; embedder = null; return null; });
    return embLoading;
  }
  function searchBest(q) {                         // hybrid when the model is ready, BM25 at once otherwise
    if (!embedder) return Promise.resolve(engine.search(q));
    return embedder(q).then(function (v) { return engine.search(q, v); }, function () { return engine.search(q); });
  }

  function load() {
    if (loading) return loading;
    loading = fetch(KB_URL, { credentials: "omit", cache: "force-cache" })
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(function (kb) { engine = new Engine(kb); return engine; });
    return loading;
  }

  function build() {
    var bubble = h("button", { type: "button", class: "ask-bubble", "aria-expanded": "false", "aria-controls": "ask-panel",
                               "aria-haspopup": "dialog" },
      [icon("M4 5h16v11H9l-5 4z"), h("span", { class: "ask-bubble-label", text: TEXT.bubble })]);
    var log = h("div", { class: "ask-log", role: "log", "aria-live": "polite", "aria-relevant": "additions", "aria-label": "Answers" });
    var input = h("input", { type: "text", id: "ask-input", class: "ask-input", autocomplete: "off", spellcheck: "true",
                             maxlength: "200", placeholder: TEXT.placeholder });
    var form = h("form", { class: "ask-form", role: "search" }, [
      h("label", { for: "ask-input", class: "ask-sr", text: "Question about Tayler" }), input,
      h("button", { type: "submit", class: "ask-send", text: TEXT.send })]);
    var closeBtn = h("button", { type: "button", class: "ask-close", "aria-label": TEXT.close }, [icon("M6 6l12 12M18 6L6 18")]);
    var panel = h("div", { id: "ask-panel", class: "ask-panel", role: "dialog", "aria-modal": "false",
                           "aria-labelledby": "ask-title", hidden: "" }, [
      h("div", { class: "ask-head" }, [
        h("div", { class: "ask-head-text" }, [
          h("h2", { id: "ask-title", class: "ask-title" }, [TEXT.title, " ", h("span", { class: "ask-sub", text: TEXT.sub })])]),
        closeBtn]),
      log, form]);
    var root = h("div", { class: "ask-root" }, [panel, bubble]);
    document.body.appendChild(root);
    els = { root: root, bubble: bubble, panel: panel, log: log, input: input, form: form };

    bubble.addEventListener("click", function () { panel.hidden ? open() : close(); });
    closeBtn.addEventListener("click", close);
    panel.addEventListener("keydown", function (e) { if (e.key === "Escape") { e.preventDefault(); close(); } });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var q = input.value.trim();
      if (!q) return;
      input.value = "";
      ask(q);
    });
  }

  function open() {
    els.panel.hidden = false;
    els.bubble.setAttribute("aria-expanded", "true");
    els.root.classList.add("is-open");
    els.input.focus();
    loadEmbedder();
    if (!els.log.childNodes.length) {
      var status = h("p", { class: "ask-status", text: TEXT.loading });
      els.log.appendChild(status);
      load().then(function () {
        status.remove();
        els.log.appendChild(starters());
      }, function () {
        status.textContent = TEXT.failed + " ";
        status.appendChild(h("a", { href: "mailto:hello@taylererbe.com", text: "hello@taylererbe.com" }));
      });
    }
  }
  function close() {
    els.panel.hidden = true;
    els.bubble.setAttribute("aria-expanded", "false");
    els.root.classList.remove("is-open");
    els.bubble.focus();
  }

  function chip(label, onClick) {
    return h("button", { type: "button", class: "ask-chip", text: label, onclick: onClick });
  }
  function starters() {
    var list = (engine.kb.starters || []).map(function (s) { return h("li", null, [chip(s.label, function () { ask(s.q, s.label); })]); });
    return h("div", { class: "ask-block ask-starters" }, [h("p", { class: "ask-label", text: TEXT.starters }), h("ul", { class: "ask-chips" }, list)]);
  }
  function links(list) {
    if (!list || !list.length) return null;
    return h("ul", { class: "ask-links" }, list.map(function (l) {
      var url = safeUrl(l.url), ext = /^https:/.test(url);
      var a = h("a", { href: url, text: l.label });
      if (ext) { a.setAttribute("target", "_blank"); a.setAttribute("rel", "noopener noreferrer");
                 a.appendChild(h("span", { class: "ask-sr", text: " (opens in a new tab)" })); }
      return h("li", null, [a]);
    }));
  }
  function cardView(card) {
    var kids = [];
    kids.push(h("p", { class: "ask-label", text: card.kind === "article" ? "Medium" + (card.date ? " · " + fmtDate(card.date) : "") : card.section_label }));
    kids.push(h("h3", { class: "ask-card-title", text: card.title }));
    if (card.state === "PENDING") {
      kids.push(h("p", { class: "ask-answer", text: engine.kb.pending.answer }));
      kids.push(links(engine.kb.pending.links));
    } else {
      kids.push(h("p", { class: "ask-answer", text: card.answer }));
      kids.push(links(card.links));
    }
    return h("article", { class: "ask-card", "data-card": card.id }, kids);
  }
  function relatedView(items) {
    if (!items.length) return null;
    return h("div", { class: "ask-related" }, [h("p", { class: "ask-label", text: TEXT.related }),
      h("ul", { class: "ask-chips" }, items.map(function (r) {
        return h("li", null, [chip(r.card.title, function () { show(r.card); })]);
      }))]);
  }
  function fallbackView(res) {
    var fb = engine.kb.fallback;
    var wrap = h("article", { class: "ask-card ask-card-fallback", "data-card": "fallback" }, [
      fb.title ? h("h3", { class: "ask-card-title", text: fb.title }) : null,
      fb.answer ? h("p", { class: "ask-answer", text: fb.answer }) : null,
      links(fb.links)]);
    var block = h("div", { class: "ask-block" }, [wrap]);
    if (res.related && res.related.length) block.appendChild(relatedView(res.related.filter(function (r) { return r.cover > 0.2; })) || h("span"));
    block.appendChild(starters());
    return block;
  }
  function userLine(q) {
    return h("p", { class: "ask-q" }, [h("span", { class: "ask-sr", text: TEXT.you + ": " }), q]);
  }
  function append(node) {
    els.log.appendChild(node);
    node.scrollIntoView && node.scrollIntoView({ block: "start", behavior: "smooth" });
  }
  function show(card) {
    append(h("div", { class: "ask-block" }, [userLine(card.title), cardView(card)]));
    els.input.focus();
  }
  function ask(q, label) {
    load().then(function () { return searchBest(q); }).then(function (res) {
      var block = h("div", { class: "ask-block" }, [userLine(label || q)]);
      if (res.best) {
        block.appendChild(cardView(res.best.card));
        var rel = relatedView(res.related);
        if (rel) block.appendChild(rel);
        append(block);
      } else {
        append(block);
        append(fallbackView(res));
      }
      els.input.focus();
    });
  }

  function injectCss() {
    if (document.querySelector('link[data-ask-css]')) return;
    var l = document.createElement("link");
    l.rel = "stylesheet"; l.href = BASE + "chat.css" + (VERSION ? "?" + VERSION : ""); l.setAttribute("data-ask-css", "");
    document.head.appendChild(l);
  }

  window.AskTayler = { Engine: Engine, load: load, search: function (q, v) { return engine ? engine.search(q, v) : null; },
                       loadEmbedder: loadEmbedder, embed: function (q) { return embedder ? embedder(q) : Promise.resolve(null); },
                       embState: function () { return embState; }, _engine: function () { return engine; }, ask: function (q) { return load().then(function () { return searchBest(q); }); },
                       _norm: rawTokens, _stem: stem };
  function start() { injectCss(); build(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
