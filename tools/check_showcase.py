"""Check public artifacts only; does not execute the Agent application."""

import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {
    ".env.example", ".gitignore", "README.md", "NOTICE.md",
    "data/synthetic_handbook.md", "docs/architecture.md", "docs/demo.md",
    "docs/evaluation.md", "docs/contributions.md", "docs/public-scope.md",
    "docs/evidence.json", "tools/check_showcase.py",
    "docs/images/01-knowledge-answer.jpg",
    "docs/images/02-context-followup.jpg",
    "docs/images/03-restored-history.jpg",
}
PATTERNS = {
    "absolute_local_path": r"(?i)(?<![a-z0-9])[a-z]:[/\\]|/Users/|/home/",
    "private_key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "api_key_shape": r"\bsk-[A-Za-z0-9_-]{20,}",
    "github_token_shape": r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})",
    "jwt_shape": r"\beyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}",
    "credential_url": r"[a-zA-Z][a-zA-Z0-9+.-]*://[^\s/:]+:[^\s/@]+@",
    "private_network": r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staged", action="store_true")
    args = parser.parse_args()
    errors = []
    paths = {
        p.relative_to(ROOT).as_posix()
        for p in ROOT.rglob("*")
        if p.is_file() and ".git" not in p.relative_to(ROOT).parts
    }
    for name in sorted(paths ^ ALLOWED):
        errors.append(f"{name}: missing or unexpected public artifact")

    links = 0
    for name in sorted(paths & ALLOWED):
        path = ROOT / name
        if path.is_symlink():
            errors.append(f"{name}: symlink not allowed")
        if path.suffix == ".jpg":
            data = path.read_bytes()
            if not (data.startswith(b"\xff\xd8") and data.endswith(b"\xff\xd9")):
                errors.append(f"{name}: invalid JPEG boundary")
            if b"Exif\x00\x00" in data:
                errors.append(f"{name}: EXIF metadata requires review")
            continue
        content = path.read_text(encoding="utf-8")
        if name != "tools/check_showcase.py":
            for number, line in enumerate(content.splitlines(), 1):
                for label, pattern in PATTERNS.items():
                    if re.search(pattern, line):
                        errors.append(f"{name}:{number}: {label}")
        if name == ".env.example":
            for number, line in enumerate(content.splitlines(), 1):
                if line.strip() and not line.lstrip().startswith("#"):
                    if not re.fullmatch(r"[A-Z][A-Z0-9_]*=", line):
                        errors.append(f"{name}:{number}: configuration value is not empty")
        if path.suffix == ".json":
            json.loads(content)
        if path.suffix == ".py":
            ast.parse(content, filename=name)
        if path.suffix == ".md":
            for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", content):
                if re.match(r"(?:https?://|mailto:|#)", target):
                    continue
                destination = (path.parent / unquote(target.split("#", 1)[0])).resolve()
                if not destination.is_relative_to(ROOT) or not destination.is_file():
                    errors.append(f"{name}: invalid local Markdown link")
                links += 1

    evidence = json.loads((ROOT / "docs/evidence.json").read_text(encoding="utf-8"))
    for shot in evidence["screenshots"]:
        name = shot["path"]
        if name not in ALLOWED or hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != shot["sha256"]:
            errors.append(f"{name}: screenshot hash mismatch")

    if args.staged:
        tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
        if set(filter(None, tracked)) != ALLOWED:
            errors.append("git index: file set differs from public whitelist")
        for name in sorted(ALLOWED):
            staged = subprocess.check_output(["git", "show", f":{name}"], cwd=ROOT)
            if staged != (ROOT / name).read_bytes():
                errors.append(f"{name}: index differs from checked working file")

    if errors:
        print("\n".join(errors))
        return 1
    print(f"PASS: {len(paths)} whitelisted files; {links} local Markdown links; 3 screenshot hashes; empty example config; text scan; JSON/Python syntax")
    if args.staged:
        print("PASS: staged whitelist and staged bytes match checked artifacts")
    print("Scope: static public-artifact checks only; not application tests, rights clearance, or a complete secret audit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
