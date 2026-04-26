"""
Resource Finder — real links via DuckDuckGo. Zero hallucination.
"""
import time
from duckduckgo_search import DDGS


def find_resources(skill: str, level: str = "beginner",
                   n: int = 4) -> list[dict]:
    """Search for real learning resources for a skill."""
    queries = [
        f"learn {skill} {level} tutorial 2024 site:youtube.com OR site:freecodecamp.org OR site:docs.python.org OR site:roadmap.sh",
        f"{skill} {level} complete guide free course",
    ]

    results  = []
    seen     = set()

    for query in queries:
        try:
            with DDGS() as ddgs:
                hits = list(ddgs.text(query, max_results=n))
            for r in hits:
                url = r.get("href", "")
                if url and url not in seen:
                    seen.add(url)
                    results.append({
                        "title":       r.get("title", "")[:80],
                        "url":         url,
                        "description": r.get("body",  "")[:150],
                    })
            time.sleep(0.4)
        except Exception as e:
            print(f"Resource search failed for '{query}': {e}")
            continue
        if len(results) >= n:
            break

    return results[:n]


def find_project_ideas(skill: str) -> list[dict]:
    """Search for hands-on project ideas."""
    try:
        with DDGS() as ddgs:
            hits = list(ddgs.text(
                f"{skill} hands-on project ideas portfolio 2024",
                max_results=3
            ))
        return [
            {
                "title": r.get("title", "")[:80],
                "url":   r.get("href",  ""),
            }
            for r in hits if r.get("href")
        ]
    except Exception:
        return []