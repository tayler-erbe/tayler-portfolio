#!/usr/bin/env python3
"""Mechanical style check for taylererbe.com. Exit 0 only if every page passes.

    python tools/check_style.py            # check every *.html page at the site root
    python tools/check_style.py page.html  # check some pages

Fails a page when it
  1. defines its own colour hex values (in <style>, style="", SVG colour attributes or script-built styles)
     instead of using the tokens in assets/site.css;
  2. names a font family (font-family: 'DM Sans' ..., an SVG font-family attribute, or a Google Fonts <link>)
     instead of var(--font-display | --font-body | --font-mono | --font-heading);
  3. defines CSS custom properties of its own (:root tokens belong in site.css);
  4. does not load assets/site.css;
  5. lacks the shared nav (nav.site-nav with links to the portfolio, skyrule.html and resume.pdf)
     or the shared footer (footer.site-footer with the same links);
  6. has a broken local link: a local href/src that does not exist, or a #fragment with no matching id.
Also checks that assets/site.css itself parses (balanced braces) and that every var(--x) a page uses is defined there.
Standard library only.
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
SITE_CSS = ROOT / "assets" / "site.css"
HEX = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b(?![-\w])")
FONT_DECL = re.compile(r"font-family\s*:\s*([^;}\"]+)", re.I)
ALLOWED_FONT = re.compile(r"^\s*(var\(--font-(display|body|mono|heading)\)|inherit)\s*!?\w*\s*$")
SVG_COLOUR_ATTRS = {"fill", "stroke", "stop-color", "flood-color", "lighting-color", "color"}
REQUIRED_LINKS = ("index.html", "skyrule.html", "resume.pdf")


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.styles, self.attr_styles, self.svg_attrs, self.scripts = set(), [], [], [], [], []
        self.stylesheets, self.font_links = [], []
        self._in = None
        self._nav_depth = self._footer_depth = 0
        self.nav_links, self.footer_links = set(), set()
        self.has_site_nav = self.has_site_footer = False
        self._stack = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "name" in a:
            self.ids.add(a["name"])
        for k in ("href", "src"):
            if a.get(k):
                self.links.append((tag, k, a[k], self.getpos()[0]))
        if a.get("style"):
            self.attr_styles.append((a["style"], self.getpos()[0]))
        for k, v in attrs:
            if v and (k in SVG_COLOUR_ATTRS or k == "font-family"):
                self.svg_attrs.append((k, v, self.getpos()[0]))
        if tag == "link":
            rel = (a.get("rel") or "").lower()
            href = a.get("href") or ""
            if "stylesheet" in rel:
                self.stylesheets.append(href)
            if "fonts.googleapis.com/css" in href:
                self.font_links.append(self.getpos()[0])
        if tag in ("style", "script"):
            self._in = tag
        if tag == "nav" and "site-nav" in cls:
            self.has_site_nav = True
            self._nav_depth = 1
        elif tag == "nav" and self._nav_depth:
            self._nav_depth += 1
        if tag == "footer" and "site-footer" in cls:
            self.has_site_footer = True
            self._footer_depth = 1
        if tag == "a":
            href = a.get("href", "")
            if self._nav_depth:
                self.nav_links.add(href.split("#")[0] or "index.html")
            if self._footer_depth:
                self.footer_links.add(href.split("#")[0] or "index.html")

    def handle_endtag(self, tag):
        if tag in ("style", "script"):
            self._in = None
        if tag == "nav" and self._nav_depth:
            self._nav_depth -= 1
        if tag == "footer" and self._footer_depth:
            self._footer_depth = 0

    def handle_data(self, data):
        if self._in == "style":
            self.styles.append((data, self.getpos()[0]))
        elif self._in == "script":
            self.scripts.append((data, self.getpos()[0]))


def defined_tokens() -> set[str]:
    css = SITE_CSS.read_text(encoding="utf-8")
    return set(re.findall(r"(--[\w-]+)\s*:", css))


def check_site_css() -> list[str]:
    errs = []
    if not SITE_CSS.exists():
        return ["assets/site.css is missing"]
    css = re.sub(r"/\*.*?\*/", "", SITE_CSS.read_text(encoding="utf-8"), flags=re.S)
    if css.count("{") != css.count("}"):
        errs.append("assets/site.css: unbalanced braces")
    used = set(re.findall(r"var\((--[\w-]+)", css))
    missing = used - defined_tokens()
    if missing:
        errs.append(f"assets/site.css uses undefined tokens: {sorted(missing)}")
    return errs


def check_page(path: Path, tokens: set[str], id_cache: dict) -> list[str]:
    text = path.read_text(encoding="utf-8")
    p = Page()
    p.feed(text)
    errs = []
    name = path.name

    def hexes(s):
        return [h for h in HEX.findall(s)]

    for css, line in p.styles:
        # blank out comments but keep their line breaks, so reported line numbers stay right
        body = re.sub(r"/\*.*?\*/", lambda c: "\n" * c.group(0).count("\n"), css, flags=re.S)

        def at(i, body=body, line=line):
            return line + body[:i].count("\n")
        for m in HEX.finditer(body):
            errs.append(f"{name}:{at(m.start())}: colour {m.group(0)} in <style>; use a token from assets/site.css")
        for m in FONT_DECL.finditer(body):
            if not ALLOWED_FONT.match(m.group(1)):
                errs.append(f"{name}:{at(m.start())}: font-family '{m.group(1).strip()}' in <style>; use var(--font-*)")
        for m in re.finditer(r"(?<![\w(])(--[\w-]+)\s*:", body):
            errs.append(f"{name}:{at(m.start())}: page defines its own token {m.group(1)}; tokens belong in assets/site.css")
    for st, line in p.attr_styles:
        for h in hexes(st):
            errs.append(f"{name}:{line}: colour {h} in style=\"\"; use a token")
        for m in FONT_DECL.finditer(st):
            if not ALLOWED_FONT.match(m.group(1)):
                errs.append(f"{name}:{line}: font-family '{m.group(1).strip()}' in style=\"\"; use var(--font-*)")
    for k, v, line in p.svg_attrs:
        if k == "font-family":
            if not ALLOWED_FONT.match(v):
                errs.append(f"{name}:{line}: font-family=\"{v}\" attribute; use var(--font-*)")
        elif "url(" not in v:
            for h in hexes(v):
                errs.append(f"{name}:{line}: {k}=\"{h}\"; use var(--token)")
    for js, line in p.scripts:
        for m in re.finditer(r"font-family\s*:\s*([^;`\"]+)", js):
            if not ALLOWED_FONT.match(m.group(1)):
                errs.append(f"{name}:{line}: script builds font-family '{m.group(1).strip()[:40]}'; use var(--font-*)")
        for m in re.finditer(r"(?:color|background|fill|stroke)\s*:\s*(#[0-9a-fA-F]{3,8})\b", js):
            errs.append(f"{name}:{line}: script builds colour {m.group(1)}; use a token")
    for line in p.font_links:
        errs.append(f"{name}:{line}: page loads Google Fonts itself; fonts are loaded by assets/site.css")

    # every var(--x) used must exist in site.css
    used = set(re.findall(r"var\((--[\w-]+)", text))
    for t in sorted(used - tokens):
        errs.append(f"{name}: uses undefined token {t}")

    # shared stylesheet, nav and footer
    if "assets/site.css" not in p.stylesheets:
        errs.append(f"{name}: does not load assets/site.css")
    if not p.has_site_nav:
        errs.append(f"{name}: missing the shared nav (nav.site-nav)")
    else:
        for req in REQUIRED_LINKS:
            if req not in p.nav_links:
                errs.append(f"{name}: shared nav lacks a link to {req}")
    if not p.has_site_footer:
        errs.append(f"{name}: missing the shared footer (footer.site-footer)")
    else:
        for req in REQUIRED_LINKS:
            if req not in p.footer_links:
                errs.append(f"{name}: shared footer lacks a link to {req}")

    # local links
    for tag, attr, url, line in p.links:
        u = urlparse(url)
        if u.scheme in ("http", "https", "mailto", "tel", "data", "javascript") or url.startswith("//"):
            continue
        target = unquote(u.path)
        frag = u.fragment
        if target:
            f = (path.parent / target).resolve()
            if not f.exists():
                errs.append(f"{name}:{line}: broken local {attr} '{url}' (no file {target})")
                continue
        else:
            f = path
        if frag and f.suffix == ".html":
            if f not in id_cache:
                q = Page()
                q.feed(f.read_text(encoding="utf-8"))
                id_cache[f] = q.ids
            # "#top" scrolls to the top of a page by browser default, so it needs no id
            if frag not in id_cache[f] and frag != "top":
                errs.append(f"{name}:{line}: broken anchor '{url}' (no id '{frag}' in {f.name})")
    return errs


def main(argv: list[str]) -> int:
    pages = [ROOT / a for a in argv] if argv else sorted(ROOT.glob("*.html"))
    tokens = defined_tokens() if SITE_CSS.exists() else set()
    errs = check_site_css()
    cache: dict = {}
    for pg in pages:
        e = check_page(pg, tokens, cache)
        status = "ok  " if not e else "FAIL"
        print(f"{status} {pg.name}" + (f"  ({len(e)} problems)" if e else ""))
        errs += e
    if errs:
        print("\n".join(["", f"{len(errs)} problem(s):"] + ["  " + x for x in errs]))
        return 1
    print(f"\nAll {len(pages)} pages pass: tokens only, shared nav and footer, local links resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
