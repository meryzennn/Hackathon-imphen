#!/usr/bin/env python3
"""Normalisasi link sesuai aturan duplikat Hackathon Berantas Web Ilegal di Indo.

Bentuk catat (yang dipakai panitia untuk cek duplikat) membuang:
skema http/https, www., huruf besar di nama domain, query setelah ?,
bagian setelah #, dan garis miring di akhir. Path tetap dihitung dan
peka huruf besar-kecil.

Sumber aturan: https://imphnen.dev/hackaton-anti-judol/info#aturan

Pemakaian:
    python3 tools/normalize.py <link> [link...]
    python3 tools/normalize.py --check entries.md <link> [link...]

Kode keluar: 0 kalau semua link sah dan tidak duplikat, 1 kalau ada yang bermasalah.
"""

import argparse
import ipaddress
import re
import sys
from pathlib import Path

MAX_LENGTH = 300


def normalize(link: str) -> str:
    """Ubah link ke bentuk catat resmi."""
    s = link.strip()
    # Buang skema http:// atau https://
    s = re.sub(r"^https?://", "", s, flags=re.IGNORECASE)
    # Buang bagian setelah #
    s = s.split("#", 1)[0]
    # Buang query setelah ?
    s = s.split("?", 1)[0]
    # Buang garis miring di akhir
    s = s.rstrip("/")
    # Buang info pengguna (user:pass@) kalau ada
    if "@" in s.split("/", 1)[0]:
        s = s.split("@", 1)[1]
    # Pisahkan host dan path
    if "/" in s:
        host, path = s.split("/", 1)
        path = "/" + path
    else:
        host, path = s, ""
    # Buang port dari host (kalau ada; validasi terpisah akan menandai ini tidak sah)
    host = host.split(":", 1)[0]
    # Huruf kecil untuk domain, buang www.
    host = host.lower()
    if host.startswith("www."):
        host = host[len("www."):]
    return host + path


def validate(link: str) -> list[str]:
    """Cek format entri. Kembalikan daftar masalah (kosong = sah)."""
    problems = []
    s = link.strip()
    if not s:
        return ["link kosong"]
    if len(s) > MAX_LENGTH:
        problems.append(f"lebih dari {MAX_LENGTH} karakter")
    rest = re.sub(r"^https?://", "", s, flags=re.IGNORECASE)
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", s) and not re.match(r"^https?://", s, flags=re.IGNORECASE):
        problems.append("skema harus http atau https")
    authority = rest.split("/", 1)[0].split("?", 1)[0].split("#", 1)[0]
    if "@" in authority:
        problems.append("tidak boleh ada nama pengguna atau kata sandi")
        authority = authority.rsplit("@", 1)[1]
    if ":" in authority:
        problems.append("tidak boleh ada port")
        host = authority.split(":", 1)[0]
    else:
        host = authority
    host_lower = host.lower()
    if host_lower == "localhost" or host_lower.endswith(".localhost"):
        problems.append("tidak boleh localhost")
    try:
        ipaddress.ip_address(host)
        problems.append("tidak boleh alamat IP")
    except ValueError:
        pass
    if not host or "." not in host:
        problems.append("domain tidak lengkap")
    return problems


def recorded_forms(entries_path: Path) -> set[str]:
    """Ambil semua bentuk catat dari tabel di entries.md."""
    forms = set()
    text = entries_path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        # Lewati baris contoh dan baris pemisah/header
        if "contoh:" in cells[1] or set(cells[0]) <= {"-", " ", ":"}:
            continue
        m = re.search(r"`([^`]+)`", cells[2])
        if m:
            forms.add(m.group(1))
    return forms


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalisasi link ke bentuk catat resmi dan cek duplikat."
    )
    parser.add_argument(
        "--check",
        metavar="ENTRIES",
        help="file entries.md untuk cek duplikat terhadap entri yang sudah tercatat",
    )
    parser.add_argument("links", nargs="+", help="link yang mau dicek")
    args = parser.parse_args()

    known = set()
    if args.check:
        path = Path(args.check)
        if not path.exists():
            print(f"file tidak ditemukan: {args.check}", file=sys.stderr)
            return 2
        known = recorded_forms(path)

    seen_in_batch = {}
    bad = False
    for link in args.links:
        form = normalize(link)
        problems = validate(link)
        notes = []
        if problems:
            notes.append("TIDAK SAH: " + "; ".join(problems))
            bad = True
        if form in known:
            notes.append("DUPLIKAT: sudah ada di entries.md")
            bad = True
        if form in seen_in_batch:
            notes.append(f"DUPLIKAT: sama dengan {seen_in_batch[form]!r} di daftar ini")
            bad = True
        seen_in_batch.setdefault(form, link)
        status = " | ".join(notes) if notes else "OK"
        print(f"{link}\n  -> {form}  [{status}]")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
