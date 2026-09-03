#!/usr/bin/env python3
"""
Normalize a folder of .txt files and create a merged corpus.

- Cleans Unicode (NFKC), converts smart punctuation (optional), removes
  Gutenberg-style artifacts ([Illustration], decorative lines, etc.).
- Reflows hard-wrapped lines by paragraph, fixes simple hyphenation-at-linebreak.
- Writes per-file cleaned texts and one merged corpus file (optionally size-capped).

Usage:
  python normalize_and_merge.py --in_dir data/raw_A --out_dir clean/A \
      --merged clean/corpus_A.txt --max_mb 2 --ascii_quotes

"""
from __future__ import annotations
import argparse, re, unicodedata, random, sys
from pathlib import Path

DECOR_LINE = re.compile(r'^\s*[*~_=#\-–—]+\s*$')
ILLUSTRATION_LINE = re.compile(r'^\s*\[.*?(illustration|image|plate).*?\]\s*$', re.I)
BLANK = re.compile(r'\s+')

def normalize_unicode(text: str, ascii_quotes: bool=False) -> str:
    # NFKC fold
    text = unicodedata.normalize("NFKC", text)
    # unify whitespace
    text = text.replace('\u00A0', ' ')  # NBSP
    # punctuation mapping (safe, small)
    if ascii_quotes:
        trans = {
            ord('“'): '"', ord('”'): '"',
            ord('‘'): "'", ord('’'): "'",
            ord('«'): '"', ord('»'): '"',
            ord('—'): '-', ord('–'): '-', ord('−'): '-',
            ord('…'): '...',
        }
    else:
        trans = {ord('…'): '…'}  # keep fancy quotes/dashes; just pass ellipsis
    return text.translate(trans)

def strip_gutenberg_boilerplate(text: str) -> str:
    """Heuristic removal; safe if markers are absent."""
    # Users said they removed it, but keep as safety.
    start = re.search(r'\*\*\*\s*START OF (THIS|THE) PROJECT GUTENBERG', text, re.I)
    end   = re.search(r'\*\*\*\s*END OF (THIS|THE) PROJECT GUTENBERG', text, re.I)
    if start and end and end.start() > start.end():
        return text[start.end():end.start()]
    return text

def clean_lines(text: str) -> str:
    """Remove obvious non-content lines and decorative blocks."""
    out_lines = []
    for ln in text.splitlines():
        if ILLUSTRATION_LINE.match(ln):
            continue
        if DECOR_LINE.match(ln):
            continue
        # strip stray control chars
        ln = ''.join(ch for ch in ln if ch == '\t' or ch == '\n' or unicodedata.category(ch)[0] != 'C')
        out_lines.append(ln.rstrip())
    return "\n".join(out_lines)

def reflow_paragraphs(text: str) -> str:
    """Join hard-wrapped lines within paragraphs; keep blank line between paragraphs."""
    lines = text.splitlines()
    paras = []
    buf = []
    def flush():
        if not buf:
            return
        # join with spaces, fix hyphenation across line breaks
        rebuilt = []
        for i, line in enumerate(buf):
            line = line.strip()
            if not rebuilt:
                rebuilt.append(line)
            else:
                prev = rebuilt[-1]
                if prev.endswith('-') and not prev.endswith('--'):
                    # de-hyphenate word split at line end
                    rebuilt[-1] = prev[:-1] + line.lstrip()
                else:
                    rebuilt[-1] = prev + ' ' + line.lstrip()
        para = rebuilt[-1]
        # collapse inner whitespace
        para = BLANK.sub(' ', para).strip()
        if para:
            paras.append(para)
        buf.clear()

    for ln in lines:
        if ln.strip() == '':
            flush()
        else:
            buf.append(ln)
    flush()
    return "\n\n".join(paras) + "\n"

def normalize_text(raw: str, ascii_quotes: bool=False) -> str:
    t = strip_gutenberg_boilerplate(raw)
    t = normalize_unicode(t, ascii_quotes=ascii_quotes)
    t = clean_lines(t)
    t = reflow_paragraphs(t)
    # optional light dedup of repeated blank lines already handled by reflow
    return t

def read_text(p: Path) -> str:
    return p.read_text(encoding='utf-8', errors='ignore')

def write_text(p: Path, s: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding='utf-8')

def size_mb(s: str) -> float:
    return len(s.encode('utf-8')) / (1024*1024)

def clamp_bytes(s: str, max_mb: float|None) -> str:
    if not max_mb:
        return s
    b = s.encode('utf-8')
    limit = int(max_mb * 1024 * 1024)
    if len(b) <= limit:
        return s
    # try to cut at a paragraph boundary before the limit
    cut = b[:limit].decode('utf-8', errors='ignore')
    last_para = cut.rfind("\n\n")
    if last_para > 0:
        cut = cut[:last_para+2]
    return cut

def collect_txt_files(in_dir: Path) -> list[Path]:
    return sorted([p for p in in_dir.glob("**/*") if p.suffix.lower() == ".txt" and p.is_file()])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in_dir", required=True, help="Folder with raw .txt files")
    ap.add_argument("--out_dir", required=True, help="Folder to write cleaned per-file texts")
    ap.add_argument("--merged", required=True, help="Path to write merged corpus")
    ap.add_argument("--max_mb", type=float, default=None, help="Cap merged corpus to this many MB")
    ap.add_argument("--shuffle", action="store_true", help="Shuffle file order when merging (recommended)")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--ascii_quotes", action="store_true", help="Map smart quotes/dashes to ASCII")
    args = ap.parse_args()

    in_dir = Path(args.in_dir)
    out_dir = Path(args.out_dir)
    merged_path = Path(args.merged)

    files = collect_txt_files(in_dir)
    if not files:
        print(f"[warn] No .txt files under {in_dir}", file=sys.stderr)
        sys.exit(1)

    # Clean per-file
    cleaned_paths = []
    total_chars = 0
    for p in files:
        raw = read_text(p)
        cleaned = normalize_text(raw, ascii_quotes=args.ascii_quotes)
        rel = p.relative_to(in_dir)
        outp = out_dir / rel.with_suffix(".clean.txt")
        write_text(outp, cleaned)
        cleaned_paths.append(outp)
        total_chars += len(cleaned)
        print(f"[cleaned] {p.name:40s}  -> {outp}")

    # Merge
    if args.shuffle:
        random.seed(args.seed)
        random.shuffle(cleaned_paths)

    merged_parts = []
    for cp in cleaned_paths:
        # add a simple document boundary marker (helps tiny LMs)
        merged_parts.append(f"<|doc|> {cp.stem}\n\n")
        merged_parts.append(read_text(cp))
        merged_parts.append("\n")  # single newline between docs
    merged = "".join(merged_parts)
    merged = clamp_bytes(merged, args.max_mb)
    write_text(merged_path, merged)

    # Stats
    mb = size_mb(merged)
    num_docs = len(cleaned_paths)
    approx_words = len(merged.split())
    print("\n=== Summary ===")
    print(f"in_dir          : {in_dir}")
    print(f"files processed : {num_docs}")
    print(f"merged path     : {merged_path}")
    print(f"merged size     : {mb:.2f} MB")
    print(f"approx words    : {approx_words:,}")
    print(f"ascii_quotes    : {args.ascii_quotes}")
    print("Done.")

if __name__ == "__main__":
    main()
