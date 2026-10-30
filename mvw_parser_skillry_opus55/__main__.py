"""Source: skillry.dev/ai-videos/opus-5-5 (listing page, server-rendered).

Downloads original + remake mp4 per slug. Prompts/metadata come from
mvw-parser-awesome-opus55 for the same slug.
"""
import re

from mvw_core import Item, cli_args, fetch_text

SOURCE = "skillry-opus55"
PAGE = "https://skillry.dev/ai-videos/opus-5-5"
MEDIA = re.compile(r"https://media\.skillry\.dev/opus-5-5/([a-z0-9-]+)/(original-card|remake-card|original|remake)\.[0-9a-f]+\.(mp4|webp)")


def main():
    args = cli_args(__doc__)
    html = fetch_text(PAGE)
    by_slug = {}
    for m in MEDIA.finditer(html):
        slug, kind, ext = m.group(1), m.group(2), m.group(3)
        by_slug.setdefault(slug, {})[(kind, ext)] = m.group(0)
    slugs = sorted(by_slug)
    if args.limit:
        slugs = slugs[: args.limit]
    new = 0
    for slug in slugs:
        files = by_slug[slug]
        it = Item(SOURCE, slug)
        new += it.is_new
        if not args.no_media:
            for (kind, ext), url in files.items():
                name = {"original-card": "original.mp4", "remake-card": "remake.mp4",
                        "original": "poster.webp", "remake": "remake-poster.webp"}[kind]
                if ext == "mp4" or kind in ("original", "remake"):
                    it.download(name, url)
        it.save_meta(title=slug, source_url=f"{PAGE}/{slug}")
    print(f"{SOURCE}: {len(slugs)} items, {new} new")


main()
