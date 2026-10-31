# wishlist-board

Personal reference board over the [YunoHost app wishlist](https://apps.yunohost.org/wishlist): every requested app, categorized, with upstream release-churn data, to decide what to package next.

- `categorize.toml` — the human-editable part: `app-key = "category"` per app.
- `sync.py` — pulls the upstream wishlist, drops new requests into **To categorize**, regenerates `README.md`.
- `.github/workflows/sync.yml` — runs `sync.py` daily and on push; commits the regenerated README.

Nothing to do to keep in sync: new upstream wishlist requests appear in the README automatically. To categorize an app, add one line to `categorize.toml` and commit.

`classify.py` is the one-off keyword seeder used for the initial categorization; not run by the Action.
