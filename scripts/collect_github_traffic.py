#!/usr/bin/env python3
"""Save GitHub traffic history using the repository traffic REST API."""

import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

OUTPUT = Path("data/github-traffic.json")


def get_traffic(repository, token, metric):
    url = f"https://api.github.com/repos/{repository}/traffic/{metric}?per=day"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "university-learning-traffic-archive",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Traffic API '{metric}' returned HTTP {error.code}: {body[:300]}"
        ) from error


def main():
    token = os.environ.get("TRAFFIC_TOKEN")
    repository = os.environ.get("GITHUB_REPOSITORY", "LiaoTian724/University-Learning")

    if not token:
        raise RuntimeError(
            "Missing TRAFFIC_TOKEN. Add a repository Actions secret with "
            "fine-grained PAT permission: Administration (read)."
        )

    # Fetch both endpoints before changing the saved file.
    clones = get_traffic(repository, token, "clones")
    views = get_traffic(repository, token, "views")

    if OUTPUT.exists():
        data = json.loads(OUTPUT.read_text(encoding="utf-8"))
        if data.get("repository") != repository:
            raise RuntimeError("Existing traffic file belongs to another repository")
    else:
        data = {"repository": repository, "daily": {}, "rolling_14_day": {}}

    daily = data.setdefault("daily", {})

    # Each API request returns only the last 14 days. Update overlapping days
    # while keeping older dates already saved in the JSON file.
    for metric, result, daily_unique_key in [
        ("clones", clones, "unique_cloners"),
        ("views", views, "unique_visitors"),
    ]:
        for entry in result.get(metric, []):
            day = entry["timestamp"][:10]  # UTC date, YYYY-MM-DD
            daily.setdefault(day, {})
            daily[day][metric] = entry["count"]
            daily[day][daily_unique_key] = entry["uniques"]

    # The 14-day 'uniques' values cannot be summed to calculate all-time users.
    now = datetime.now(timezone.utc)
    today = now.date().isoformat()
    data.setdefault("rolling_14_day", {})[today] = {
        "clones": clones["count"],
        "unique_cloners": clones["uniques"],
        "views": views["count"],
        "unique_visitors": views["uniques"],
    }
    data["daily"] = dict(sorted(daily.items()))
    data["rolling_14_day"] = dict(sorted(data["rolling_14_day"].items()))
    data["last_collected_utc"] = now.isoformat(timespec="seconds")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        f"Saved {len(daily)} days of traffic history to {OUTPUT}. "
        f"14-day totals: {clones['count']} clones, {views['count']} views."
    )


if __name__ == "__main__":
    main()
