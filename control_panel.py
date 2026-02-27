from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import requests
import streamlit as st

ROOT = Path(__file__).parent
SITE_URL = "https://atlan-c.github.io/turvablogi/"
ACTIONS_URL = "https://github.com/atlan-c/turvablogi/actions"

st.set_page_config(page_title="Turvablogi-ohjauspaneeli", layout="centered")
st.title("Turvablogi – selkokielinen ohjauspaneeli")


def run_cmd(cmd: list[str]):
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, shell=False)
    return p.returncode, (p.stdout or "") + ("\n" + p.stderr if p.stderr else "")


def find_hugo() -> str:
    h = shutil.which("hugo")
    if h:
        return h
    winget_hugo = Path.home() / "AppData/Local/Microsoft/WinGet/Links/hugo.exe"
    if winget_hugo.exists():
        return str(winget_hugo)
    return "hugo"


st.subheader("1) Luo uusi postaus")
post_title = st.text_input("Postauksen otsikko", placeholder="Esim. Viikkokatsaus")
if st.button("Luo postaus"):
    if not post_title.strip():
        st.error("Kirjoita otsikko ensin.")
    else:
        code, out = run_cmd([
            "powershell", "-ExecutionPolicy", "Bypass", "-File",
            str(ROOT / "scripts" / "new-post.ps1"), "-Title", post_title.strip(),
        ])
        (st.success if code == 0 else st.error)("Postauspohja luotu." if code == 0 else "Postauksen luonti epäonnistui.")
        st.code(out)

st.subheader("2) Testaa paikallinen build")
if st.button("Aja build (hugo --minify)"):
    code, out = run_cmd([find_hugo(), "--minify"])
    (st.success if code == 0 else st.error)("Build onnistui." if code == 0 else "Build epäonnistui.")
    st.code(out)

st.subheader("3) Julkaise tuotantoon")
publish_msg = st.text_input("Commit-viesti", value="Uusi postaus")
mode = st.radio("Julkaisutapa", ["Suora push mainiin", "Suojattu tapa: branch + PR-linkki"], index=1)
if st.button("Julkaise nyt"):
    if mode == "Suora push mainiin":
        code, out = run_cmd([
            "powershell", "-ExecutionPolicy", "Bypass", "-File",
            str(ROOT / "scripts" / "publish.ps1"), "-Message", publish_msg,
        ])
        if code == 0:
            st.success("Julkaisu onnistui. GitHub Actions hoitaa deployn.")
        elif code == 2:
            st.error("Push estettiin (branch protection). Käytä branch + PR -tapaa.")
        else:
            st.error("Julkaisu epäonnistui.")
        st.code(out)
    else:
        code, out = run_cmd([
            "powershell", "-ExecutionPolicy", "Bypass", "-File",
            str(ROOT / "scripts" / "publish-pr.ps1"), "-Message", publish_msg,
        ])
        if code == 0:
            st.success("Branch push onnistui. Avaa PR-linkki lokista.")
            lines = [ln for ln in out.splitlines() if "Open PR URL:" in ln]
            if lines:
                st.link_button("Avaa PR", lines[-1].replace("Open PR URL:", "").strip())
        else:
            st.error("Branch/PR-julkaisu epäonnistui.")
        st.code(out)

st.subheader("4) Tarkista että sivu on live")
col1, col2 = st.columns(2)
with col1:
    st.link_button("Avaa live-sivu", SITE_URL)
with col2:
    st.link_button("Avaa Actions", ACTIONS_URL)

if st.button("Tarkista live-sivu"):
    try:
        r = requests.get(SITE_URL, timeout=20)
        if r.status_code == 200 and "Turvablogi" in r.text:
            st.success(f"Sivu vastaa oikein ({r.status_code}).")
        else:
            st.warning(f"Sivu vastasi statuksella {r.status_code}.")
    except Exception as e:
        st.error(f"Tarkistus epäonnistui: {e}")

st.subheader("5) Tilannekuva")
if st.button("Näytä git status"):
    _, out = run_cmd(["git", "status", "-sb"])
    st.code(out)
if st.button("Näytä 5 viimeisintä committia"):
    _, out = run_cmd(["git", "log", "--oneline", "-n", "5"])
    st.code(out)
