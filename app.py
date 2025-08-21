# app.py — Core Innovation Hub
# Run: streamlit run app.py

import io, base64, html, re
from pathlib import Path
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse, urlencode, urlunparse, parse_qsl

import yaml
import pandas as pd
import streamlit as st
import qrcode

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Core Innovation Hub", page_icon="✨", layout="wide")

# ---------- PATHS & BRAND ----------
BASE = Path(__file__).resolve().parent
YAML_PATH = BASE / "assets" / "data" / "projects.yaml"
LOGO_PATH = BASE / "assets" / "logos" / "hermosillo_logo.png"

# Images / Links
LOGO_SIDEBAR_URL     = "https://hermosillo.com/wp-content/uploads/2019/07/hermosillo-experience-matters-logo.svg"
LOGO_HEADER_LEFT_URL = "https://hermosillo.com/wp-content/uploads/2019/08/horizontal-hermosillo-experience-matters-registered-logo.png"
ROADMAP_IFRAME_URL   = "https://hmo-core-roadmap.streamlit.app/"  # optional embedded app

# ---------- CSS ----------
st.markdown("""
<style>
:root { --primary:#F97316; --bg:#F3F4F6; --card-bg:#FFFFFF; --card-bdr:#E5E7EB; --text:#0F172A; --muted:#6B7280; }
html, body, [class*="css"] { font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; background: var(--bg); }
h1,h2,h3,h4,h5,h6 { color: var(--text); font-weight: 700; }
.block-container { max-width: 1400px; padding-top: .75rem; padding-right: 2.25rem; }

.top-spacer{ height:48px; }

.ci-rail{ position: sticky; top: 0; background: #1F3B73; color: #E7ECF7; border-radius: 14px; padding: 16px 12px 18px;
  border: 1px solid rgba(255,255,255,0.12); box-shadow: 0 8px 28px rgba(0,0,0,.10); overflow: hidden;}
.ci-rail .brand{ font-weight:800; color:#fff; margin:8px 0 12px 0; }
.ci-rail a{ display:block; text-decoration:none; color:#E7ECF7; font-weight:600; background: rgba(255,255,255,.06);
  border:1px solid rgba(255,255,255,.12); padding:10px 12px; border-radius:12px; margin-bottom:8px; }
.ci-rail a:hover{ background: rgba(255,255,255,.12); }
.ci-rail hr{ border:none;height:1px;background:rgba(255,255,255,.15);margin:10px 0 }

.ci-title { font-weight: 900; font-size: 44px; line-height: 1.04; letter-spacing: .2px; color: var(--text); margin: 4px 0 8px 0; }
.ci-sub { color:#6B7280; margin-bottom: 8px; font-size:18px; }
.ci-title-accent { width: 64px; height: 6px; border-radius: 999px; background: var(--primary); }

.header-wrap{ display:flex; align-items:center; justify-content:center; gap:48px; margin-bottom: 12px; }
.title-group{ display:flex; align-items:center; gap:18px; }
.brand-inline-logo{ height:64px; width:auto; display:block; object-fit:contain; }

.kpi-stack{ display:flex; flex-direction:column; gap:12px; justify-content:center; height:100%; }
.kpi-box{ display:flex; flex-direction:column; align-items:flex-end; padding:12px 14px; border-radius:14px; background:#fff;
  border:1px solid var(--card-bdr); box-shadow: 0 6px 20px rgba(0,0,0,.06); min-width: 220px; max-width: 280px; width: 100%; }
.kpi-box .l{ font-size:11px; letter-spacing:.06em; color:#94A3B8; text-transform:uppercase; margin:0; }
.kpi-box .v{ font-size:26px; font-weight:800; color:#0F172A; margin:0; }

.chip{ background:#fff; border:1px solid var(--card-bdr); padding:10px 12px; border-radius:14px; box-shadow:0 2px 12px rgba(0,0,0,.04); }

.insight{ display:inline-flex; align-items:center; gap:.5rem; background:#fff; border:1px solid var(--card-bdr); color:#0F172A;
  padding:6px 10px; border-radius:999px; margin-right:8px; margin-bottom:6px; font-weight:700; }

.card{ background:#fff; border:1px solid var(--card-bdr); border-radius:16px; padding:16px; margin-bottom:16px; box-shadow:0 6px 20px rgba(16,24,40,.05); }
.card h3{ margin: 8px 0 4px 0; }
.card p{ margin: 0 0 12px 0; color: var(--muted); }
.badges{ margin-bottom:8px; }
.badge{ display:inline-block; padding:4px 10px; border-radius:999px; background:#F97316; color:#fff; font-weight:700; font-size:12px; margin:4px 6px 0 0; }

.kpis{ display:flex; gap:10px; flex-wrap:wrap; margin:8px 0 12px 0; }
.kpi-mini{ background:linear-gradient(180deg, rgba(0,0,0,.02), rgba(0,0,0,0)); border:1px solid var(--card-bdr); border-radius:12px; padding:8px 10px; min-width:150px; }
.kpi-mini .v{ font-weight:800; color:#0F172A; }
.kpi-mini .l{ font-size:11px; letter-spacing:.06em; color:#6B7280; text-transform:uppercase; }

.card .row{ display:grid; grid-template-columns: 3fr 1fr; gap: 18px; align-items:start; }
.card .row.onecol{ grid-template-columns: 1fr; } /* when right column is empty */
@media (max-width: 980px){ .card .row{ grid-template-columns: 1fr; } }
.rightcol h4{ margin: 0 0 8px 0; }
.qr{ border:1px solid #E5E7EB; border-radius:12px; padding:6px; display:inline-block; background:#fff; }

.sidebar-logo{display:block;margin:0 auto 16px auto;max-width:140px;border-radius:12px}
.tiny-logo{ position:fixed; top:18px; left:260px; width:38px; height:38px; border-radius:50%; border:1px solid #E5E7EB;
  box-shadow:0 2px 8px rgba(0,0,0,.15); background:#fff; z-index:9999; cursor:pointer; transition:transform .15s ease; }
.tiny-logo:hover{ transform:scale(1.05) }

.impact-grid{ display:grid; grid-template-columns: repeat(3, 1fr); gap:18px; margin: 8px 0 24px 0; }
.impact-card{ background: linear-gradient(180deg, rgba(255,255,255,1), rgba(255,255,255,.92)); border:1px solid var(--card-bdr); border-radius:16px; padding:16px; box-shadow: 0 8px 24px rgba(0,0,0,.06); }
.ic-top{ display:flex; align-items:center; gap:10px; color:#64748B; font-weight:700; letter-spacing:.04em; text-transform:uppercase; font-size:12px;}
.ic-val{ font-size:40px; font-weight:900; color:#0F172A; line-height:1; margin-top:4px; }
.ic-foot{ color:#6B7280; font-size:13px; margin-top:8px; }
.ic-icon{ font-size:20px; background:#FEE5D2; color:#F97316; border-radius:8px; padding:4px 8px; }

.roadmap-embed{ border: 1px solid var(--card-bdr); border-radius:16px; overflow:hidden; box-shadow: 0 8px 24px rgba(0,0,0,.06); background:#fff; }

/* Footer */
.ci-footer{
  text-align:center;
  color:#6B7280;
  font-size:13px;
  margin: 28px 0 24px 0;
}
.ci-footer .f-accent{
  width: 80px; height: 4px; border-radius:999px; background: var(--primary);
  margin: 0 auto 10px auto;
}
</style>
""", unsafe_allow_html=True)

# ---------- HELPERS ----------
def ensure_list(x):
    return x if isinstance(x, list) else ([] if x in (None, "", {}) else [x])

def slugify(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "project"

def render_kpi(label: str, value: str):
    st.markdown(f"""
    <div class="kpi-box">
      <div class="l">{label}</div>
      <div class="v">{value}</div>
    </div>
    """, unsafe_allow_html=True)

def ensure_streamlit_embed(url: str) -> str:
    if not url: return ""
    try:
        u = urlparse(url); host = (u.netloc or "").lower()
        if host.endswith("streamlit.app") or "share.streamlit.io" in host:
            q = dict(parse_qsl(u.query)); q["embed"] = "true"
            u = u._replace(query=urlencode(q)); return urlunparse(u)
    except Exception:
        pass
    return url

def load_projects_yaml(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        st.error(f"Missing YAML file: {path.as_posix()}"); return []
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if isinstance(data, list): return data
    if isinstance(data, dict):
        if "projects" in data and isinstance(data["projects"], list): return data["projects"]
        out = []
        for name, details in data.items():
            d = details or {}; 
            if not isinstance(d, dict): d = {"value": d}
            d.setdefault("title", d.get("name") or name); out.append(d)
        return out
    return []

def normalize_table(items: List[Dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for p in items:
        demo = p.get("demo") or {}
        rows.append({
            "title": p.get("title") or p.get("name") or "",
            "impact": p.get("impact") or p.get("description") or "",
            "category": p.get("category") or "",
            "status": p.get("status") or "",
            "badges": ensure_list(p.get("badges")),
            "links": ensure_list(p.get("links")),
            "kpis": ensure_list(p.get("kpis")),
            "demo_type": demo.get("type", ""),
            "demo_src": demo.get("src") or demo.get("url") or demo.get("file") or "",
            "raw": p
        })
    if not rows:
        rows.append({"title":"", "impact":"", "category":"", "status":"", "badges":[], "links":[], "kpis":[], "demo_type":"", "demo_src":"", "raw":{}})
    return pd.DataFrame(rows, dtype=object)

def resolve_media_src(src: str) -> str:
    if not src or src.startswith(("http://", "https://")): return src or ""
    p = BASE / src
    if not p.exists():
        for folder in ["assets/videos", "assets/gallery", "assets"]:
            test = BASE / folder / src
            if test.exists(): p = test; break
        else: return ""
    return p.as_posix()

def qr_to_b64(url: str, size: int = 110) -> str:
    try:
        buf = io.BytesIO()
        q = qrcode.QRCode(border=1, box_size=6); q.add_data(url); q.make(fit=True)
        q.make_image(fill_color="black", back_color="white").save(buf, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"
    except Exception:
        return ""

# ---------- MEDIA CLASSIFIER (for gallery tiles) ----------
IMG_EXT = (".png",".jpg",".jpeg",".gif",".webp",".svg")
VID_EXT = (".mp4",".webm",".ogg")

def _youtube_embed(url: str) -> str:
    try:
        u = urlparse(url)
        if "youtu.be" in u.netloc:
            vid = u.path.strip("/"); 
        else:
            qs = dict(parse_qsl(u.query)); vid = qs.get("v","")
        return f"https://www.youtube.com/embed/{vid}?rel=0"
    except Exception:
        return url

def _gdrive_preview(url: str) -> str:
    # Ensure /preview form for drive files
    try:
        u = urlparse(url)
        if "drive.google.com" not in u.netloc.lower(): return url
        if "/preview" in u.path: return url
        # /file/d/<id>/view -> /file/d/<id>/preview
        path = u.path.replace("/view", "/preview")
        return urlunparse(u._replace(path=path))
    except Exception:
        return url

def classify_media(url: str) -> Tuple[str, str]:
    """
    Returns (kind, normalized_url)
      kind in {"image","video","iframe"}
    """
    if not isinstance(url, str) or not url.strip(): return ("image","")
    u = url.strip()
    low = u.lower()
    # Google Drive -> iframe preview
    if "drive.google.com" in low:
        return ("iframe", _gdrive_preview(u))
    # YouTube
    if "youtube.com" in low or "youtu.be" in low:
        return ("iframe", _youtube_embed(u))
    # File extensions
    if any(low.endswith(ext) for ext in VID_EXT): return ("video", u)
    if any(low.endswith(ext) for ext in IMG_EXT): return ("image", u)
    # Unknown -> image by default
    return ("image", u)

# --- BULLETS + GALLERY RENDERER ---------------------------------------------
def render_bullets_and_gallery(demo: Dict[str, Any]) -> str:
    if not isinstance(demo, dict):
        return "<div style='padding:10px;border:1px dashed #E5E7EB;border-radius:12px;color:#64748B'>Demo not configured</div>"

    items  = demo.get("items") or []
    layout = str(demo.get("layout") or "3-columns").lower().strip()
    media  = demo.get("media") or []

    cols = 2 if "2" in layout else 3
    grid_css = f"repeat({cols}, 1fr)"

    # bullets
    bullets_html = ""
    if items:
        per_col = max(1, (len(items) + cols - 1) // cols)
        col_html = []
        for i in range(cols):
            chunk = items[i*per_col:(i+1)*per_col]
            if not chunk: continue
            lis = "".join([f"<li>{html.escape(str(x))}</li>" for x in chunk])
            col_html.append(f"<ul style='margin:0;padding-left:20px'>{lis}</ul>")
        bullets_html = (
            "<div class='ci-bullets' style="
            "'background:#fff;border:1px solid var(--card-bdr);border-radius:12px;"
            "padding:12px;box-shadow:0 2px 12px rgba(0,0,0,.04);margin-bottom:12px;'>"
            f"<div style='display:grid;grid-template-columns:{grid_css};gap:12px;'>"
            f"{''.join(col_html)}"
            "</div></div>"
        )

    # gallery
    gallery_html = ""
    if media:
        tiles = []
        for m in media:
            if isinstance(m, dict):
                url = str(m.get("url","")).strip(); cap = str(m.get("caption","")).strip()
                kind, norm = classify_media(url)
            else:
                url = str(m or "").strip(); cap = ""; kind, norm = classify_media(url)
            if not norm: continue
            esc = html.escape(norm)
            cap_html = f"<div style='margin-top:6px;color:#6B7280;font-size:12px;'>{html.escape(cap)}</div>" if cap else ""
            if kind == "video":
                tiles.append(
                    "<div>"
                    f"<video controls playsinline style='width:100%;border-radius:10px;outline:none;'>"
                    f"<source src='{esc}'></video>{cap_html}</div>"
                )
            elif kind == "iframe":
                tiles.append(
                    "<div>"
                    f"<div style='position:relative;width:100%;padding-top:56.25%;border-radius:10px;overflow:hidden;'>"
                    f"<iframe src='{esc}' loading='lazy' allow='autoplay; encrypted-media' "
                    "style='position:absolute;inset:0;width:100%;height:100%;border:0;border-radius:10px;'></iframe>"
                    f"</div>{cap_html}</div>"
                )
            else:  # image
                tiles.append(
                    "<div>"
                    f"<img src='{esc}' style='width:100%;border-radius:10px;display:block;'/>"
                    f"{cap_html}</div>"
                )
        if tiles:
            gallery_html = (
                "<div class='ci-gallery' style="
                "'background:#fff;border:1px solid var(--card-bdr);border-radius:12px;"
                "padding:12px;box-shadow:0 2px 12px rgba(0,0,0,.04);'>"
                "<div style='font-weight:700;color:#0F172A;margin-bottom:8px;'>Media</div>"
                "<div style='display:grid;grid-template-columns:repeat(3,1fr);gap:12px;'>"
                f"{''.join(tiles)}"
                "</div></div>"
            )

    if not (items or media):
        return "<div style='padding:10px;border:1px dashed #E5E7EB;border-radius:12px;color:#64748B'>Demo not configured</div>"

    out = (bullets_html + gallery_html).replace("\n","").replace("\r","")
    return out

def media_tag(demo_type: str, demo_src: str, demo_dict: Dict[str, Any] = None) -> str:
    # bullets support
    if (demo_type or "").lower() == "bullets":
        return render_bullets_and_gallery(demo_dict or {})

    if not demo_type or not demo_src:
        return "<div style='padding:10px;border:1px dashed #E5E7EB;border-radius:12px;color:#64748B'>Demo not configured</div>"

    if demo_src.startswith(("http://", "https://")):
        url = demo_src
        if demo_type == "iframe": url = ensure_streamlit_embed(url)
        esc = html.escape(url)
        if demo_type == "iframe":
            return f"<iframe src='{esc}' width='100%' height='420' style='border:0;border-radius:12px;'></iframe>"
        if demo_type == "video":
            return f"<video controls playsinline style='width:100%;border-radius:12px;outline:none;'><source src='{esc}' type='video/mp4'></video>"
        if demo_type == "image":
            return f"<img src='{esc}' style='width:100%;border-radius:12px;'/>"
        return "<div>Unsupported media</div>"

    src_path = resolve_media_src(demo_src)
    if not src_path: return "<div>Media not found</div>"

    if demo_type == "image":
        try:
            with open(src_path, "rb") as f: b64 = base64.b64encode(f.read()).decode()
            return f"<img src='data:image/png;base64,{b64}' style='width:100%;border-radius:12px;'/>"
        except Exception:
            return "<div>Image not available</div>"

    if demo_type == "video":
        try:
            with open(src_path, "rb") as f: b64 = base64.b64encode(f.read()).decode()
            return ("<video controls playsinline style='width:100%;border-radius:12px;outline:none;'>"
                    f"<source src='data:video/mp4;base64,{b64}' type='video/mp4'></video>")
        except Exception:
            return "<div>Video not available</div>"

    if demo_type == "iframe":
        return "<div style='padding:10px;border:1px dashed #E5E7EB;border-radius:12px;color:#64748B'>Local iframes not supported. Provide an https URL.</div>"

    return "<div>Unsupported media</div>"

def project_card_html(row) -> str:
    title   = html.escape(row.get("title") or "Untitled")
    slug    = slugify(row.get("title") or "")
    impact  = html.escape(row.get("impact") or "")
    badges  = row.get("badges") or []
    kpis    = row.get("kpis") or []
    links   = row.get("links") or []
    demo_t  = row.get("demo_type") or ""
    demo_s  = row.get("demo_src") or ""

    badges_html = "".join([f"<span class='badge'>{html.escape(str(b))}</span>" for b in badges])
    kpis_html   = "".join([f"<div class='kpi-mini'><div class='v'>{html.escape(str(k.get('value','')))}</div><div class='l'>{html.escape(str(k.get('label','')))}</div></div>" for k in (kpis or [])[:3]])

    # Links & QR
    links_html = ""
    first_url = ""
    if links:
        items = []
        for l in links:
            label = html.escape(str(l.get("label","Open"))); url = html.escape(str(l.get("url","")))
            if url:
                items.append(f"<li><a href='{url}' target='_blank'>{label}</a></li>")
                if not first_url: first_url = url
        if items: links_html = "<h4>Open Links</h4><ul>" + "".join(items) + "</ul>"

    qr_html = ""
    if first_url:
        b64 = qr_to_b64(first_url)
        if b64: qr_html = f"<div class='qr'><img src='{b64}' width='110' height='110' /></div>"

    # Conditionally render right column; adjust grid class
    rightbits = "".join([links_html, ('<h4>Scan to open</h4>' if qr_html else ''), qr_html])
    row_class = "row" if rightbits else "row onecol"
    rightcol  = f"<div class='rightcol'>{rightbits}</div>" if rightbits else ""

    return (
    f"<div class='card' id='{slug}'>"
      f"<div class='badges'>{badges_html}</div>"
      f"<h3>{title}</h3>"
      f"<p>{impact}</p>"
      f"<div class='kpis'>{kpis_html}</div>"
      f"<div class='{row_class}'>"
        f"<div class='leftcol'>{media_tag(demo_t, demo_s, row.get('raw', {}).get('demo', {}))}</div>"
        f"{rightcol}"
      f"</div>"
    f"</div>"
    )

# ---------- LOAD DATA ----------
projects_raw = load_projects_yaml(YAML_PATH)
df = normalize_table(projects_raw)

project_menu = [{"title": r.get("title") or "Untitled", "slug": slugify(r.get("title") or "")}
                for _, r in df.iterrows()]

# ---------- SIDEBAR ----------
with st.sidebar:
    proj_links = "".join([f"<a href='#{itm['slug']}'>• {html.escape(itm['title'])}</a>" for itm in project_menu]) or ""
    logo_html = f"<img src='{LOGO_SIDEBAR_URL}' class='sidebar-logo'/>" if LOGO_SIDEBAR_URL \
                else (f"<img src='file://{LOGO_PATH.as_posix()}' class='sidebar-logo'/>" if LOGO_PATH.exists() else "")
    sidebar_html = f"""
    <div class="ci-rail">
      {logo_html}
      <div class='brand'>Hermosillo · Core Innovation</div>
      <a href='#overview'>📊 Overview</a>
      <a href='#projects'>🧩 Projects</a>
      <a href='#impact'>📈 Transformation</a>
      <a href='#roadmap'>🧭 Roadmap</a>
      {'<hr/><strong>Projects</strong>' if proj_links else ''}
      {proj_links}
    </div>
    """
    st.markdown(sidebar_html, unsafe_allow_html=True)

tiny_src = LOGO_SIDEBAR_URL if LOGO_SIDEBAR_URL else (f"file://{LOGO_PATH.as_posix()}" if LOGO_PATH.exists() else "")
if tiny_src:
    st.markdown(
        f"<a href='#' onclick='window.location.reload();' title='Refresh'><img src='{tiny_src}' class='tiny-logo'/></a>",
        unsafe_allow_html=True
    )

# ---------- HEADER ----------
st.markdown("<div class='top-spacer'></div>", unsafe_allow_html=True)
live_count = int(df["badges"].apply(lambda b: any((str(x or "")).lower()=="live" for x in (b or []))).sum()) if not df.empty else 0

header_html = f"""
<div class="header-wrap">
  <div class="title-group">
    <div>
      <div class='ci-title'>Core Innovation — Project Showcase</div>
      <div class='ci-sub'>Experience Matters • Hermosillo</div>
      <div class='ci-title-accent'></div>
    </div>
    {'<img src="'+LOGO_HEADER_LEFT_URL+'" class="brand-inline-logo"/>' if LOGO_HEADER_LEFT_URL else ''}
  </div>
  <div class="kpi-stack">
    <div class="kpi-box"><div class="l">Projects</div><div class="v">+{len(df)}</div></div>
    <div class="kpi-box"><div class="l">Live Demos</div><div class="v">{live_count}</div></div>
  </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ---------- OVERVIEW ----------
st.markdown("<div id='overview'></div>", unsafe_allow_html=True)
c1,c2,c3,c4 = st.columns([1.2,1.2,1.2,1.2])
with c1:
    st.markdown("<div class='chip'>Category</div>", unsafe_allow_html=True)
    cats = ["All"] + sorted([x for x in df["category"].dropna().unique().tolist() if x])
    sel_cat = st.selectbox("", cats, label_visibility="collapsed")
with c2:
    st.markdown("<div class='chip'>Status</div>", unsafe_allow_html=True)
    stats = ["All"] + sorted([x for x in df["status"].dropna().unique().tolist() if x])
    sel_stat = st.selectbox("", stats, label_visibility="collapsed")
with c3:
    st.markdown("<div class='chip'>Demo Type</div>", unsafe_allow_html=True)
    demos = ["All"] + sorted([x for x in df["demo_type"].dropna().unique().tolist() if x])
    sel_demo = st.selectbox("", demos, label_visibility="collapsed")
with c4:
    st.markdown("<div class='chip'>Search</div>", unsafe_allow_html=True)
    q = st.text_input("", "", label_visibility="collapsed").strip().lower()

fdf = df.copy()
if sel_cat  != "All": fdf = fdf[fdf["category"] == sel_cat]
if sel_stat != "All": fdf = fdf[fdf["status"] == sel_stat]
if sel_demo != "All": fdf = fdf[fdf["demo_type"] == sel_demo]
if q:
    fdf = fdf[
        fdf["title"].str.lower().str.contains(q, na=False) |
        fdf["impact"].str.lower().str.contains(q, na=False)
    ]

# ---------- INSIGHTS ----------
ins = [("✅", f"{len(fdf)} projects match filters"),
       ("🎥", f"{int((fdf['demo_type']=='video').sum())} video demos"),
       ("🖥️", f"{int((fdf['demo_type']=='iframe').sum())} live iframes")]
st.markdown("".join([f"<span class='insight'>{i} {t}</span>" for i, t in ins]), unsafe_allow_html=True)
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ---------- PROJECTS ----------
st.markdown("<div id='projects'></div>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-bottom:6px'>Projects</h3>", unsafe_allow_html=True)
st.markdown("<div class='ci-title-accent' style='width:42px;height:5px;margin-bottom:12px'></div>", unsafe_allow_html=True)
for _, row in fdf.iterrows():
    st.markdown(project_card_html(row), unsafe_allow_html=True)

# ---------- IMPACT ----------
st.markdown("<div id='impact'></div>", unsafe_allow_html=True)
st.markdown("<h3>Transformation & Impact</h3>", unsafe_allow_html=True)
st.markdown("""
<div class="impact-grid">
  <div class="impact-card">
    <div class="ic-top"><span class="ic-icon">↘</span> Decision lead time</div>
    <div class="ic-val">60–70%</div>
    <div class="ic-foot">Faster decisions from standards + dashboards</div>
  </div>
  <div class="impact-card">
    <div class="ic-top"><span class="ic-icon">✓</span> Rework / errors</div>
    <div class="ic-val">25–40%</div>
    <div class="ic-foot">Template quality + QA checklists reduce errors</div>
  </div>
  <div class="impact-card">
    <div class="ic-top"><span class="ic-icon">⚙</span> Automation hours / mo</div>
    <div class="ic-val">120+</div>
    <div class="ic-foot">Saved via scripts, batch jobs, and integrations</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------- ROADMAP ----------
st.markdown("<div id='roadmap'></div>", unsafe_allow_html=True)
st.markdown("### Roadmap — Scale the DNA")
r1,r2,r3 = st.columns(3)
with r1: st.markdown("- Standardize templates\n- Expand dashboards\n- Certify cohort")
with r2: st.markdown("- Parametric budgeting pilots\n- ACC QA rollout company-wide\n- Automation catalog")
with r3: st.markdown("- AI-assisted reviews\n- AR/VR site overlays\n- Predictive risk scoring")

embed_url = ensure_streamlit_embed(ROADMAP_IFRAME_URL)
if embed_url:
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="roadmap-embed">
      <iframe src="{html.escape(embed_url)}" width="100%" height="680" style="border:0;"></iframe>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("Set `ROADMAP_IFRAME_URL` to embed a live app in the Roadmap section.")

# ---------- FOOTER ----------
st.markdown("""
<div class="ci-footer">
  <div class="f-accent"></div>
  <div>Developed by <strong>Core Innovation</strong> — Grupo Hermosillo · 2025</div>
</div>
""", unsafe_allow_html=True)
