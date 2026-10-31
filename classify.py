#!/usr/bin/env python3
"""One-off helper: seed categorize.toml by keyword-matching wishlist descriptions.
Re-running only fills keys not already present (categorize.toml is user-owned after that)."""
import json, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent
wl = json.loads((ROOT / "wishlist.json").read_text())

# ordered: first match wins
RULES = [
    ("games", ["game", "minecraft", "factorio", "terraria", "dont starve", "project zomboid",
               "chess", "sudoku", "mindustry", "osu!", "zelda", "mario", "pokemon",
               "party game", "board game", "d&d", "dnd", "openrct", "5etools", "race for"]),
    ("iot", ["home automation", "homeassistant", "home assistant", "domotic", "zigbee", "mqtt",
             "smart home", "esphome", "tasmota", "openhab", "irrigation", "energy monitor",
             "weather station", "weather"]),
    ("communication", ["chat", "forum", "meeting", "video call", "voip", "xmpp", "sms",
                       "messaging", "newsletter", "email", "e-mail", "mailing", "webmail",
                       "smtp", "imap", "notification", "webrtc", "comment section",
                       "q&a", "real-time"]),
    ("multimedia", ["music", "photo", "picture", "image", "video", "movie", "torrent",
                    "podcast", "radio", "media server", "media center", "gallery", "streaming",
                    "download", "youtube", "spotify", "audio", "ebook", "subtitle",
                    "transcod", "ocr", "diashow", "tv show"]),
    ("reading", ["rss", "news feed", "feed reader", "news reader", "book librar",
                 "ebook librar", "comic", "kindle", "epub", "wikipedia", "kiwix"]),
    ("social_media", ["microblog", "mastodon", "fediverse", "lemmy", "reddit", "instagram",
                      "facebook", "twitter", "social network", "snapchat", "tiktok", "bluesky",
                      "tumblr", "peertube", "social"]),
    ("publishing", ["cms", "blog", "wiki", "website", "static site", "portfolio", "analytics",
                    "landing page", "documentation", "headless", "e-commerce", "storefront",
                    "webshop", "site builder", "page builder", "link in bio", "linktree",
                    "publish", "shop"]),
    ("synchronization", ["sync", "contact manager", "calendar", "contacts", "password manager",
                         "passwords", "2fa", "otp", "vault", "e2ee"]),
    ("office", ["document", "office", "text editor", "collaborative edit", "spreadsheet",
                "whiteboard", "mind map", "draw.io", "diagram", "form", "survey",
                "onlyoffice", "records management", "scanning", "pdf", "signature",
                "presentation", "slide"]),
    ("productivity_and_management", ["task", "todo", "kanban", "poll", "accounting", "invoice",
                                     "erp", "crm", "budget", "expense", "bookmark", "time track",
                                     "project management", "ticket", "helpdesk", "help desk",
                                     "inventory", "asset manage", "event manag", "reservation",
                                     "booking", "scheduling", "checklist", "habit",
                                     "household", "grocer", "recipe", "fitness",
                                     "workout", "meal plan", "wedding", "genealog",
                                     "family tree", "customer"]),
    ("dev", ["git", "forge", "ci/cd", "continuous integration", "code review", "jupyter",
             "notebook", "develop", "programming", "snippet", "regex", "json",
             "database admin", "sql", "swagger", "openapi", "version control", "skeleton",
             "boilerplate", "translation", "localization", "localisation", "gitea", "api doc",
             "container registry", "docker registry", "package registry", "webhook", "cron"]),
    ("education", ["learning", "lms", "moodle", "flashcard", "quiz", "school", "education",
                   "student", "teacher", "exam", "course", "vocabular", "spaced repetition"]),
    ("system_tools", ["monitor", "backup", "network", "dns", "firewall", "syslog", "log ",
                      "ssh", "vpn", "wireguard", "uptime", "metric", "grafana", "prometheus",
                      "snmp", "fail2ban", "proxmox", "speedtest", "smokeping",
                      "endlessh", "mail queue", "ntp", "routing", "mesh network",
                      "reverse proxy", "admin panel", "certificate", "letsencrypt",
                      "single sign", "ldap", "identity", "terminal", "shell",
                      "rsync", "zfs", "file server", "storage"]),
    ("small_utilities", ["pastebin", "url shortener", "shorten", "proxy", "file manager",
                         "dashboard", "launcher", "start page", "startpage", "screenshot",
                         "qr code", "sharex", "share x", "notes app", "notes", "snippets",
                         "calculator", "countdown", "timer", "clipboard",
                         "markdown", "convert", "tool", "status page", "watch",
                         "reminder", "upload", "search engine", "translate"]),
]

CATS = ["synchronization", "publishing", "communication", "office",
        "productivity_and_management", "small_utilities", "reading", "education",
        "multimedia", "social_media", "games", "dev", "system_tools", "iot", "wat"]

out = {}
for k, v in wl.items():
    text = f"{k} {v.get('name','')} {v.get('description','')}".lower()
    for cat, kws in RULES:
        if any(w in text for w in kws):
            out[k] = cat
            break

path = ROOT / "categorize.toml"
existing = {}
if path.exists():
    for line in path.read_text().splitlines():
        if "=" in line and not line.strip().startswith("#"):
            key, val = line.split("=", 1)
            existing[key.strip()] = val.strip().strip('"')
merged = {**out, **existing}
lines = ["# app-key = \"category\"   (categories: " + ", ".join(CATS) + ")",
         "# keys missing here show up under 'To categorize' in README.md", ""]
for key in sorted(merged):
    lines.append(f'{key} = "{merged[key]}"')
path.write_text("\n".join(lines) + "\n")
print("classified", len(merged), "of", len(wl))
print(dict(collections.Counter(merged.values())))
un = sorted(set(wl) - set(merged))
print("uncategorized:", len(un))
for k in un:
    print(f"  {k:30} {wl[k].get('description','')[:70]}")
