#!/usr/bin/env python3
"""Seed difficulty.toml: easy | regular | complex.
Heuristics: description keywords, upstream primary languages (langs.txt), hand overrides.
difficulty.toml is user-editable afterwards; re-runs never overwrite existing keys."""
import json, pathlib, collections

ROOT = pathlib.Path("/root/workspace/wishlist-board")
wl = json.loads((ROOT / "wishlist.json").read_text())
langs = {}
for line in open("/root/workspace/langs.txt"):
    k, _, spec = line.strip().partition("|")
    if spec:
        pairs = [p.split(":") for p in spec.split(",")]
        langs[k] = [(n, int(v)) for p in pairs if len(p) == 2 for n, v in [p]]

COMPLEX_KW = ["kubernetes", "microservic", "monorepo", "matrix", "bigbluebutton", "jitsi",
              "web conferencing", "video conferencing", "erp", "mail hosting", "mail server",
              "bridge", "cassandra", "elasticsearch", "groupware", "office suite", "suite for",
              "multi-user", "crm", "learning management", "lms", "collection management suite"]
OVERRIDE = {
    # easy: single binary / tiny service
    "goatcounter": "easy", "yggdrasil": "easy", "ipfs": "easy", "docker-registry": "easy",
    "endlessh": "easy", "znc": "easy", "boinc": "easy", "klaxon": "easy",
    "smokeping": "regular", "taskwarrior": "easy", "mailpit": "easy", "inbucket": "easy",
    "grafana": "easy", "prometheus": "easy", "uptime-kuma": "easy", "anubis": "easy",
    "altcha": "easy", "mosparo": "regular", "yarr": "easy", "youtubedl-server": "easy",
    # complex: multi-service / exotic infra / heavy
    "supabase": "complex", "docspell": "complex", "taiga": "complex", "inventaire": "complex",
    "modoboa": "complex", "bigbluebutton": "complex", "greenlight": "complex",
    "mastodon": "complex", "takahe": "complex", "socialhome": "complex", "pixelfed": "complex",
    "flarum": "complex", "nodebb": "complex", "discourse": "complex", "mattermost": "regular",
    "rocketchat": "complex", "protonmails-webclient": "complex", "exo-platform": "complex",
    "ox-open-xchange": "complex", "openproject": "complex", "dataverse": "complex",
    "archivematica": "complex", "arsnova": "complex", "hypothes-is": "complex",
    "crabgrass": "complex", "officelife": "regular", "passbolt": "regular", "trilium": "easy",
    "mailpile": "complex", "nitter": "regular", "invidious": "regular", "forgejo": "easy",
    "vaultwarden": "easy", "mailtrain": "complex", "listmonk": "regular",
}
EASY_LANGS = {"Go", "Rust", "C", "C++", "Shell", "Lua", "Zig", "Nim", "HTML"}

def primary(k):
    ls = langs.get(k) or []
    tot = sum(v for _, v in ls)
    return ls[0][0] if tot and ls[0][1] / tot > 0.4 else None

out = {}
for k, v in wl.items():
    text = f"{v.get('name','')} {v.get('description','')}".lower()
    if k in OVERRIDE:
        out[k] = OVERRIDE[k]
    elif any(w in text for w in COMPLEX_KW):
        out[k] = "complex"
    else:
        lang = primary(k)
        if lang in EASY_LANGS:
            out[k] = "easy"
        else:
            out[k] = "regular"

path = ROOT / "difficulty.toml"
existing = {}
if path.exists():
    for line in path.read_text().splitlines():
        if "=" in line and not line.strip().startswith("#"):
            key, val = line.split("=", 1)
            existing[key.strip()] = val.strip().strip('"')
merged = {**out, **existing}
lines = ['# app-key = "easy" | "regular" | "complex" — expected packaging effort',
         "# keys missing here are shown untagged", ""]
lines += [f'{k} = "{merged[k]}"' for k in sorted(merged)]
path.write_text("\n".join(lines) + "\n")
print(dict(collections.Counter(merged.values())))
