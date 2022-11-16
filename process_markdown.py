#!/usr/bin/env python3
import pathlib
import glob
from dataclasses import dataclass
from datetime import datetime
from sys import argv
from typing import Iterator, Optional

import git

repo_root = pathlib.Path(__file__).parent.resolve()


@dataclass(frozen=True)
class FileMeta:
    path: pathlib.Path
    creation_time: datetime
    modification_time: Optional[datetime]


def extract_file_metadata(repo_path: pathlib.Path) -> Iterator[FileMeta]:
    repo = git.Repo(path=repo_path)
    markdown_files = [pathlib.Path(f) for f in glob.glob("*/*.md")]
    for md in markdown_files:
        commits = list(repo.iter_commits(paths=md))
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
    front_matter = "+++\n"
    front_matter += f"categories = ['{meta.path.parent}']\n"
    front_matter += f"date = {meta.creation_time}\n"
    if meta.modification_time:
        front_matter += f"lastmod = {meta.creation_time}\n"
    front_matter += "+++\n"
    destination_file = content_dir / meta.path.name
    destination_file.write_text(front_matter + meta.path.read_text())


if __name__ == "__main__":
    content_dir = pathlib.Path(argv[1])
    for file_meta in extract_file_metadata(repo_root):
        copy_file_with_front_matter(file_meta, content_dir)
