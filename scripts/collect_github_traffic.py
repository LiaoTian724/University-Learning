#!/usr/bin/env python3
"""Archive daily GitHub traffic for all public repositories owned by this account.

This script intentionally skips private repositories because the archive is
committed to a public repository.
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

OUTPUT = Path("data/github-traffic.json")
API_ROOT = "https://api.github.com"


def github_get(path, token, params=None):
    url = API_ROOT + path
    if params:
        url += "?" + urllib.parse.urlencode(params)

    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "github-traffic-history-collector",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")[:250]
        raise RuntimeError(
            f"GitHub API returned HTTP {error.code} for {path}: {detail}"
        ) from error


def list_public_owned_repositories(token, owner):
    """Only list publicly visible repositories owned by the selected account."""
    repositories = []
    page = 1

    while True:
        batch = github_get(
            "/user/repos",
            token,
            {
                "affiliation": "owner",
                "visibility": "public",
                "per_page": 100,
                "page": page,
            },
        )
        if not isinstance(batch, list):
            raise RuntimeError("Unexpected response when listing repositories")

        for item in batch:
            if (
                item.get("owner", {}).get("login", "").lower() == owner.lower()
                and not item.get("private", True)
            ):
                repositories.append(item["full_name"])

        if len(batch) < 100:
            break
        page += 1

    return sorted(set(repositories))


def load_existing_history():
    if not OUTPUT.exists():
        return {"repositories": {}}

    data = json.loads(OUTPUT.read_text(encoding="utf-8"))
    if "repositories" in data:
        return data

    # Upgrade the previous single-repository archive without losing its data.
    if "repository" in data:
        return {
            "repositories": {
                data["repository"]: {
                    "daily": data.get("daily", {}),
                    "rolling_14_day": data.get("rolling_14_day", {}),
                }
            }
        }
    raise RuntimeError("Unrecognized existing GitHub traffic archive format")


def merge_metrics(history, clones, views, today):
    daily = history.setdefault("daily", {})

    # Overwrite overlapping dates with the latest 14-day API data,
    # but never discard dates that have already aged out.
    for metric, response, unique_key in (
        ("clones", clones, "unique_cloners"),
        ("views", views, "unique_visitors"),
    ):
        for entry in response.get(metric, []):
            date = entry["timestamp"][:10]
            daily.setdefault(date, {})
            daily[date][metric] = entry["count"]
            daily[date][unique_key] = entry["uniques"]

    history.setdefault("rolling_14_day", {})[today] = {
        "clones": clones["count"],
        "unique_cloners": clones["uniques"],
        "views": views["count"],
        "unique_visitors": views["uniques"],
    }
    history["daily"] = dict(sorted(history["daily"].items()))
    history["rolling_14_day"] = dict(sorted(history["rolling_14_day"].items()))


def main():
    token = os.environ.get("TRAFFIC_TOKEN")
    if not token:
        raise RuntimeError(
            "Missing TRAFFIC_TOKEN GitHub Actions secret. "
            "Use a fine-grained PAT with All repositories and Administration: Read."
        )

    owner = os.environ.get("GITHUB_REPOSITORY_OWNER", "LiaoTian724")
    now = datetime.now(timezone.utc)
    today = now.date().isoformat()

    repositories = list_public_owned_repositories(token, owner)
    if not repositories:
        raise RuntimeError(
            f"No public repositories found for {owner}. Check token repository access."
        )

    data = load_existing_history()
    data["owner"] = owner
    data["scope"] = "owned_public_repositories_only"

    successes = 0
    failures = []

    for repository in repositories:
        escaped = urllib.parse.quote(repository, safe="/")
        try:
            clones = github_get(f"/repos/{escaped}/traffic/clones", token, {"per": "day"})
            views = github_get(f"/repos/{escaped}/traffic/views", token, {"per": "day"})
        except RuntimeError as error:
            print(f"WARNING: {error}")
            failures.append(repository)
            continue

        history = data["repositories"].setdefault(repository, {})
        merge_metrics(history, clones, views, today)
        successes += 1
        print(
            f"{repository}: {clones['count']} clones, "
            f"{views['count']} views (last 14 days)"
        )

    if not successes:
        raise RuntimeError(
            "Could not retrieve traffic for any repository. "
            "Check Administration: Read on all repositories."
        )

    data["last_collected_utc"] = now.isoformat(timespec="seconds")
    data["last_run"] = {
        "public_repositories_found": len(repositories),
        "updated": successes,
        "failed": failures,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"Saved traffic for {successes}/{len(repositories)} public repositories "
        f"to {OUTPUT}"
    )


if __name__ == "__main__":
    main()
