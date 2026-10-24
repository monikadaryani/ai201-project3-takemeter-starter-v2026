#!/usr/bin/env python3
"""
Turn saved Reddit threads into rows of labels.csv, ready for you to label.

Save each thread from your browser into `data/raw/` first, either as an
ordinary web page (Cmd+S, "Webpage, HTML Only") or as the `.json` view: add
`.json` to the end of the URL
(e.g. `https://www.reddit.com/r/Cooking/comments/abc123/x/.json`) and save
that. Then:

    python extract_comments.py
    python extract_comments.py --per-thread 20

New comments are appended to labels.csv with an empty label. Rows already in
the file are never changed, so it's safe to run again after saving more
threads.
"""

import argparse
import csv
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path

SKIP_AUTHORS = {"AutoModerator", "[deleted]"}
SKIP_BODIES = {"[deleted]", "[removed]"}
# Embedded videos put CSS and a "something went wrong" message inside the body.
SKIP_TAGS = {"style", "script", "template", "shreddit-player", "shreddit-player-2"}


class ThreadPageParser(HTMLParser):
    """Pull comments out of a thread saved as a normal Reddit web page.

    Each comment is a <shreddit-comment author=...> element whose text sits in
    a <div slot="comment">. Replies nest inside their parent, but the body div
    always comes before them, so the most recent author is the right one.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.comments = []
        self.author = None
        self.depth = 0  # divs open inside the current body; 0 = not in one
        self.skipping = 0  # inside an embedded player's styles or error text
        self.paragraphs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in SKIP_TAGS:
            if self.depth:
                self.skipping += 1
        elif tag == "shreddit-comment":
            self.author = attrs.get("author")
        elif tag == "div" and self.depth:
            self.depth += 1
        elif tag == "div" and attrs.get("slot") == "comment":
            self.depth, self.paragraphs = 1, [""]
        elif self.depth and tag in ("p", "li", "br", "blockquote"):
            self.paragraphs.append("")

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS:
            if self.skipping:
                self.skipping -= 1
            return
        if tag != "div" or not self.depth:
            return
        self.depth -= 1
        if self.depth == 0:
            self.skipping = 0
            text ="\n\n".join(" ".join(p.split()) for p in self.paragraphs if p.strip())
            self.comments.append({"body": text, "author": self.author})

    def handle_data(self, data):
        if self.depth and not self.skipping:
            self.paragraphs[-1] += data


def load_thread(path):
    """Read a saved thread and return its comments, replies included.

    Accepts the `.json` view (some browsers wrap it in an HTML page) or the
    thread saved as an ordinary web page.
    """
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if text.startswith("<"):
        match = re.search(r"<pre[^>]*>(.*?)</pre>", text, re.S)
        if not match:
            parser = ThreadPageParser()
            parser.feed(text)
            if not parser.comments:
                raise ValueError("web page with no comments in it")
            return parser.comments
        text = html.unescape(match.group(1))
    return list(walk_comments(json.loads(text)[1]["data"]["children"]))


def walk_comments(children):
    """Yield every comment in a thread, replies included, in page order."""
    for child in children:
        if child.get("kind") != "t1":
            continue  # "more" stubs and anything that isn't a comment
        data = child["data"]
        yield data
        replies = data.get("replies")
        if isinstance(replies, dict):
            yield from walk_comments(replies["data"]["children"])


def keep(comment, min_chars, max_chars):
    body = (comment.get("body") or "").strip()
    if body in SKIP_BODIES or comment.get("author") in SKIP_AUTHORS:
        return False
    if comment.get("stickied") or comment.get("distinguished") == "moderator":
        return False
    return min_chars <= len(body) <= max_chars


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--raw", default="data/raw", help="folder of saved .json threads")
    parser.add_argument("--out", default="labels.csv", help="CSV to append to")
    parser.add_argument("--per-thread", type=int, default=30,
                        help="max comments taken from one thread, so no thread dominates")
    parser.add_argument("--min-chars", type=int, default=15)
    parser.add_argument("--max-chars", type=int, default=1500)
    args = parser.parse_args()

    out = Path(args.out)
    existing = set()
    if out.exists():
        with out.open(newline="", encoding="utf-8") as f:
            existing = {row["text"].strip() for row in csv.DictReader(f)}

    new_rows = []
    paths = [p for p in Path(args.raw).iterdir() if p.suffix in (".json", ".html", ".htm")]
    for path in sorted(paths):
        try:
            comments = load_thread(path)
        except (ValueError, KeyError, IndexError, TypeError) as e:
            print(f"skipped {path.name}: not a Reddit thread ({e})")
            continue
        taken = 0
        for comment in comments:
            body = comment["body"].strip() if comment.get("body") else ""
            if taken >= args.per_thread or not keep(comment, args.min_chars, args.max_chars):
                continue
            if body in existing:
                continue
            existing.add(body)
            new_rows.append({"text": body, "label": "", "note": ""})
            taken += 1
        print(f"{path.name}: {taken} comments")

    write_header = not out.exists() or out.stat().st_size == 0
    with out.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label", "note"])
        if write_header:
            writer.writeheader()
        writer.writerows(new_rows)

    print(f"\nadded {len(new_rows)} comments to {out} ({len(existing)} total)")


if __name__ == "__main__":
    main()
