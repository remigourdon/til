#!/usr/bin/env python3
import pathlib
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator, Optional
import argparse
import shutil

import git


@dataclass(frozen=True)
class FileMeta:
    path: pathlib.Path
    creation_time: datetime
    modification_time: Optional[datetime]


def extract_file_metadata(repo_path: pathlib.Path) -> Iterator[FileMeta]:
    repo = git.Repo(path=repo_path)
    markdown_files = [f for f in repo_path.glob("*/*.md")]
    for md in markdown_files:
        commits = list(repo.iter_commits(paths=md.relative_to(repo_path)))
        if len(commits) == 0:
            continue
        elif len(commits) == 1:
            created = commits[0]
            modified = None
        else:
            created = commits[-1]
            modified = commits[0]
        file_meta = FileMeta(
            path=md,
            creation_time=created.committed_datetime,
            modification_time=modified.committed_datetime if modified else None,
        )
        yield file_meta


def copy_file_with_front_matter(meta: FileMeta, content_dir: pathlib.Path):
    source_content = meta.path.read_text()
    title_line = source_content.splitlines()[0]
    title = title_line[2:] if title_line.startswith("# ") else ""
    category = meta.path.parent.name
    front_matter = "+++\n"
    front_matter += f"title = '{title}'\n"
    front_matter += f"categories = ['{category}']\n"
    front_matter += f"date = {meta.creation_time}\n"
    if meta.modification_time:
        front_matter += f"lastmod = {meta.creation_time}\n"
    front_matter += "+++\n"
    destination_dir = content_dir / category
    destination_dir.mkdir(exist_ok=True)
    destination_file = destination_dir / meta.path.name
    destination_file.write_text(front_matter + source_content)


def initialize_content_dir(content_dir: pathlib.Path):
    shutil.rmtree(content_dir, ignore_errors=True)
    content_dir.mkdir(exist_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process TIL Markdown files for Hugo rendering"
    )
    parser.add_argument(
        "--repo-root",
        type=pathlib.Path,
        required=True,
        help="Repository containing Markdown files to process",
    )
    parser.add_argument(
        "--dest-dir",
        type=pathlib.Path,
        required=True,
        help="Directory to place processed Markdown files into",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    initialize_content_dir(args.dest_dir)
    total = 0
    for file_meta in extract_file_metadata(args.repo_root):
        if file_meta.modification_time is None:
            print(f"New file added: {file_meta.path.relative_to(args.repo_root)}")
        copy_file_with_front_matter(file_meta, args.dest_dir)
        total += 1
    print(f"Processed a total of {total} Markdown files")
