import io, base64, qrcode
import streamlit as st

def inject_css():
    st.markdown("""
    <style>
      /* Base page width & spacing */
      .block-container { padding-top: 0.75rem; max-width: 1400px; }
      header[data-testid="stHeader"] { background: transparent; }

      :root{
        --h-orange:#F25C05;
        --rail:#1F3B73;        /* Hermosillo deep blue */
        --rail-ink:#E7ECF7;
        --chip-bg:#FFFFFF;
        --chip-bdr:rgba(0,0,0,0.10);
        --card-bdr:rgba(0,0,0,0.08);
      }

      /* Left rail */
      .ci-rail{
        position: sticky; top: 0;
        background: var(--rail);
        color: var(--rail-ink);
        border-radius: 14px;
        padding: 16px 12px;
        border: 1px solid rgba(255,255,255,0.10);
        min-height: 92vh;
        box-shadow: 0 8px 28px rgba(0,0,0,0.10);
      }
      .ci-rail .brand{
        display:flex; align-items:center; gap:10px; font-weight:800;
        color:#fff; letter-spacing:.02em; margin-bottom:10px;
      }
      .ci-rail a{
        display:flex; align-items:center; gap:10px;
        text-decoration:none; color:#E7ECF7; font-weight:600;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        padding:10px 12px; border-radius: 12px; margin-bottom:8px;
      }
      .ci-rail a:hover{ background: rgba(255,255,255,0.12); }

      /* Page header */
      .ci-title { font-weight:800; font-size:28px; margin:6px 0 4px 0; }
      .ci-sub { color:#6B7280; }

      /* KPI chips (right of title) */
      .kpi-box{
        display:flex; flex-direction:column; align-items:flex-end;
        padding:10px 12px; border-radius:12px; background:#fff;
        border:1px solid var(--card-bdr); box-shadow: 0 4px 16px rgba(0,0,0,0.04);
      }
      .kpi-box .l{ font-size:11px; letter-spacing:.06em; color:#94A3B8; text-transform:uppercase;}
      .kpi-box .v{ font-size:24px; font-weight:800; color:#0F172A;}

      /* Filter chips row */
      .chips{ display:flex; flex-wrap:wrap; gap:10px; }
      .chip{
        background: var(--chip-bg);
        border:1px solid var(--chip-bdr);
        padding: 10px 12px; border-radius:14px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
      }

      /* Cards */
      .card{
        background:#fff; border:1px solid var(--card-bdr);
        border-radius:16px; padding:12px 14px;
        box-shadow: 0 6px 20px rgba(16,24,40,0.04);
      }
      .card:hover{ box-shadow: 0 10px 28px rgba(16,24,40,0.08); }

      /* Project grid */
      .ci-grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
      @media (max-width:1200px){ .ci-grid{ grid-template-columns:repeat(2,1fr);} }
      @media (max-width:760px){ .ci-grid{ grid-template-columns:1fr;} }

      /* Badges */
      .badges{ margin-bottom:8px; }
      .badge{
        display:inline-block; padding:4px 10px; border-radius:999px;
        background: rgba(242,92,5,0.10); color:#7A2E00;
        border:1px solid rgba(242,92,5,0.25);
        font-size:12px; font-weight:700; margin-right:6px; margin-bottom:6px;
      }

      /* KPI mini chips inside project card */
      .kpis{ display:flex; gap:10px; flex-wrap:wrap; margin:8px 0 10px 0; }
      .kpi{
        background:linear-gradient(180deg, rgba(0,0,0,0.02), rgba(0,0,0,0.00));
        border:1px solid var(--card-bdr); border-radius:12px; padding:10px 12px; min-width:160px;
      }
      .kpi .v{ font-weight:800; font-size:18px; color:#0F172A;}
      .kpi .l{ font-size:11px; letter-spacing:.06em; color:#6B7280; text-transform:uppercase; }

      /* Insight badges */
      .insight{ display:inline-flex; align-items:center; gap:.5rem; background:#fff;
        border:1px solid var(--card-bdr); color:#0F172A; padding:6px 10px; border-radius:999px; margin-right:8px; margin-bottom:6px; font-weight:700;}
    </style>
    """, unsafe_allow_html=True)

def qr_img_b64(url: str, size: int = 106) -> str:
    import qrcode
    buf = io.BytesIO()
    q = qrcode.QRCode(border=1, box_size=6); q.add_data(url); q.make(fit=True)
    q.make_image(fill_color="black", back_color="white").save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"<img alt='qr' src='data:image/png;base64,{b64}' width='{size}' height='{size}' style='border-radius:12px;border:1px solid rgba(0,0,0,.1);padding:6px;background:#fff'/>"

def badges_html(badges):
    return "".join([f"<span class='badge'>{b}</span>" for b in badges or []])

def kpis_html(kpis):
    if not kpis: return ""
    chips = "".join([f\"\"\"\n      <div class='kpi'><div class='v'>{k['value']}</div><div class='l'>{k['label']}</div></div>\n    \"\"\" for k in kpis[:3]])
    return f"<div class='kpis'>{chips}</div>"
