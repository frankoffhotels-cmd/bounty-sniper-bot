import logging
import os

import aiohttp

GITHUB_SEARCH_URL = "https://api.github.com/search/issues"
IGNORED_REPOS = ["bounty-plaza", "bounty-bot", "TentOfTrials", "zeroeye"]
IGNORED_KEYWORDS = ["Bounty Seguro", "Bounty Plaza", "Answer the question"]
logger = logging.getLogger(__name__)


async def fetch_github_bounties() -> list[dict[str, int | str]]:
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "bounty-aggregator",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    else:
        logger.warning(
            "GITHUB_TOKEN is not set; GitHub API rate limits may be lower."
        )

    params = {
        "q": (
            "is:issue is:open is:public label:bounty language:python "
            "-repo:zhangjiayang6835-cyber/bounty-plaza "
            "-repo:alfrexo95/bounty-bot"
        ),
        "sort": "created",
        "order": "desc",
        "per_page": 10,
    }
    timeout = aiohttp.ClientTimeout(total=30)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(
            GITHUB_SEARCH_URL,
            params=params,
            headers=headers,
        ) as response:
            response.raise_for_status()
            payload = await response.json()

    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise ValueError("Unexpected response format from GitHub Issues API.")

    bounties: list[dict[str, int | str]] = []
    for issue in payload["items"]:
        if not isinstance(issue, dict):
            continue
        issue_id = issue.get("id")
        title = issue.get("title")
        url = issue.get("html_url")
        repository_url = issue.get("repository_url", "")
        user = issue.get("user", {})
        username = user.get("login", "") if isinstance(user, dict) else ""

        if (
            not isinstance(issue_id, int)
            or not isinstance(title, str)
            or not isinstance(url, str)
            or not isinstance(repository_url, str)
            or not isinstance(username, str)
        ):
            continue

        normalized_title = title.casefold()
        if any(repo.casefold() in repository_url.casefold() for repo in IGNORED_REPOS):
            continue
        if any(keyword.casefold() in normalized_title for keyword in IGNORED_KEYWORDS):
            continue
        if normalized_title.count("bounty") >= 3:
            continue

        bounties.append({"id": issue_id, "title": title, "url": url})

    return bounties
