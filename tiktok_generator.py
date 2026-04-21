"""
TikTok Content Auto-Generator — Gaya Ferry Irwandi
Versi: Google Gemini API (GRATIS)

Cara pakai:
  1. pip install google-genai
  2. Set API key: export GEMINI_API_KEY="AIza..."
  3. Jalankan: python tiktok_generator.py
  4. Batch: python tiktok_generator.py --batch 5 --output konten_minggu_ini.md
"""

import google.genai as genai
import argparse
import json
import os
import random
from datetime import datetime, timedelta
from pathlib import Path


# ─── Konfigurasi ─────────────────────────────────────────────────────────────

EBOOK_CONTEXT = """
E-book: Kumpulan 50+ prompt Claude AI yang sudah terbukti meningkatkan produktivitas 10x
Target: Gen Z Indonesia (18-25 tahun)
Harga: [isi harga Anda]
Link: [isi link bio Anda]
Manfaat utama:
  - Hemat 2-3 jam kerja per hari
  - Prompt siap pakai untuk konten, bisnis, belajar, dan karir
  - Tidak perlu trial-error berbulan-bulan
"""

CONTENT_FORMATS = [
    {
        "nama": "Hook Data Mengejutkan",
        "deskripsi": "Buka dengan statistik atau fakta yang bikin orang berhenti scroll",
        "contoh_hook": "90% orang pakai AI salah. Ini bedanya."
    },
    {
        "nama": "Storytelling Personal",
        "deskripsi": "Cerita pengalaman pribadi yang relatable sebelum kasih solusi",
        "contoh_hook": "Gue dulu buang 3 jam sehari buat hal yang sekarang kelar 8 menit."
    },
    {
        "nama": "Analogi Sederhana",
        "deskripsi": "Jelasin konsep AI yang rumit pakai perbandingan sehari-hari",
        "contoh_hook": "Minta tolong ke AI itu kayak minta tolong ke orang baru kerja."
    },
    {
        "nama": "Pain Point Attack",
        "deskripsi": "Langsung sentuh frustrasi yang dirasakan Gen Z soal AI",
        "contoh_hook": "Udah install 10 tools AI tapi hidup lo masih sama aja?"
    },
    {
        "nama": "Before vs After",
        "deskripsi": "Tunjukkan perbedaan hasil sebelum dan sesudah pakai prompt yang tepat",
        "contoh_hook": "Ini bedanya prompt orang biasa vs orang yang udah baca e-book ini."
    },
    {
        "nama": "Soft CTA",
        "deskripsi": "Closing yang natural tanpa kesan maksa beli",
        "contoh_hook": "Gue kumpulin ini 6 bulan. Lo bisa pake dalam 6 menit."
    },
]

TOPIK_LIST = [
    "cara pakai AI untuk nulis email profesional",
    "prompt untuk riset bisnis dalam 5 menit",
    "belajar skill baru 3x lebih cepat dengan AI",
    "cara AI bantu Gen Z dapat side income",
    "prompt untuk persiapan interview kerja",
    "AI untuk nulis CV dan cover letter",
    "cara pakai AI buat presentasi yang meyakinkan",
    "prompt untuk analisis kompetitor bisnis",
]


# ─── Generator ────────────────────────────────────────────────────────────────

def generate_tiktok_script(client, format_konten: dict, topik_spesifik: str = None) -> dict:
    topik = topik_spesifik or random.choice(TOPIK_LIST)

    prompt = f"""Kamu adalah content creator TikTok Indonesia yang ahli di bidang AI dan produktivitas.
Gaya kamu persis seperti Ferry Irwandi: bicara natural, buka dengan konflik atau fakta mengejutkan,
jelasin hal rumit pakai analogi sederhana, selipkan sisi manusia lewat cerita personal.

ATURAN PENULISAN:
- Kalimat pendek-pendek, maksimal 10 kata per kalimat
- Sering pakai baris kosong untuk jeda dramatik
- Bahasa Indonesia campur sedikit Inggris (natural)
- JANGAN pakai kata: "kawan", "teman-teman", "guys", "sob"
- Hook yang bikin orang berhenti scroll dalam 3 detik pertama
- Durasi bicara: 45-60 detik (sekitar 120-150 kata)
- Akhiri dengan insight kuat, BUKAN "semoga bermanfaat"

FORMAT KONTEN: {format_konten['nama']}
DESKRIPSI: {format_konten['deskripsi']}
CONTOH HOOK REFERENSI (jangan copy, cari yang lebih segar): {format_konten['contoh_hook']}
TOPIK: {topik}

KONTEKS E-BOOK:
{EBOOK_CONTEXT}

Balas HANYA dengan JSON ini, tanpa teks lain, tanpa markdown fence:
{{
  "hook": "kalimat pembuka saja",
  "script": "skrip lengkap dengan baris kosong sebagai jeda",
  "hashtags": ["#tag1", "#tag2", "#tag3", "#tag4", "#tag5"],
  "durasi_estimasi": "XX detik",
  "tips_delivery": "1 tips cara bawain video ini"
}}"""

    response = client.models.generate_content(model="gemini-2.0-flash-lite", contents=prompt)
    raw = response.text.strip()

    # Bersihkan markdown fence jika ada
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    result = json.loads(raw)
    result["format"] = format_konten["nama"]
    result["topik"] = topik
    result["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return result


def generate_daily_batch(client, jumlah: int = 3) -> list:
    print(f"\n Generating {jumlah} skrip TikTok...\n")
    formats = (CONTENT_FORMATS * 3)[:jumlah]
    random.shuffle(formats)

    results = []
    for i, fmt in enumerate(formats, 1):
        print(f"  [{i}/{jumlah}] {fmt['nama']}...", end=" ", flush=True)
        try:
            script = generate_tiktok_script(client, fmt)
            results.append(script)
            print("OK")
        except Exception as e:
            print(f"Error: {e}")
    return results


# ─── Output ───────────────────────────────────────────────────────────────────

def format_markdown(scripts: list, mulai_tanggal: str = None) -> str:
    tanggal = datetime.strptime(mulai_tanggal, "%Y-%m-%d") if mulai_tanggal else datetime.today()
    lines = [
        "# Konten TikTok — E-book AI",
        f"Dibuat: {datetime.now().strftime('%d %B %Y, %H:%M')}",
        f"Total: {len(scripts)} skrip\n---\n",
    ]
    for i, s in enumerate(scripts, 1):
        tgl = (tanggal + timedelta(days=i - 1)).strftime("%A, %d %B %Y")
        lines += [
            f"## Video {i} — {tgl}",
            f"**Format:** {s.get('format')}",
            f"**Topik:** {s.get('topik')}",
            f"**Durasi:** {s.get('durasi_estimasi')}",
            f"\n### Hook\n> {s.get('hook')}\n",
            f"### Skrip\n```\n{s.get('script')}\n```\n",
            f"### Hashtags\n{' '.join(s.get('hashtags', []))}",
            f"\n### Tips Delivery\n{s.get('tips_delivery')}\n\n---\n",
        ]
    return "\n".join(lines)


def print_single(s: dict):
    print("\n" + "=" * 55)
    print(f"FORMAT : {s.get('format')}")
    print(f"TOPIK  : {s.get('topik')}")
    print(f"DURASI : {s.get('durasi_estimasi')}")
    print("-" * 55)
    print(f"HOOK:\n  {s.get('hook')}")
    print("-" * 55)
    print("SKRIP:")
    print(s.get("script"))
    print("-" * 55)
    print("HASHTAGS:", " ".join(s.get("hashtags", [])))
    print(f"TIPS   : {s.get('tips_delivery')}")
    print("=" * 55 + "\n")


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Auto-generate skrip TikTok pakai Gemini AI (gratis)")
    parser.add_argument("--batch", type=int, default=1, help="Jumlah skrip (default: 1)")
    parser.add_argument("--output", type=str, default=None, help="Simpan ke file .md")
    parser.add_argument("--topik", type=str, default=None, help="Topik spesifik (opsional)")
    parser.add_argument("--mulai-tanggal", type=str, default=None, help="Format: YYYY-MM-DD")
    args = parser.parse_args()

    # Setup Gemini
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY belum di-set!")
        print("Cara set: export GEMINI_API_KEY='AIza...'")
        return

    client = genai.Client(api_key=api_key)
    

    print("TikTok Content Generator — Gemini AI (Gratis)")
    print("Model: gemini-2.0-flash")

    if args.batch == 1:
        fmt = random.choice(CONTENT_FORMATS)
        print(f"\nGenerating 1 skrip (format: {fmt['nama']})...", end=" ", flush=True)
        script = generate_tiktok_script(client, fmt, topik_spesifik=args.topik)
        print("OK")
        print_single(script)
        scripts = [script]
    else:
        scripts = generate_daily_batch(client, jumlah=args.batch)

    if args.output:
        md = format_markdown(scripts, mulai_tanggal=args.mulai_tanggal)
        Path(args.output).write_text(md, encoding="utf-8")
        print(f"\nTersimpan: {args.output} ({len(scripts)} skrip)")
    elif args.batch > 1:
        for s in scripts:
            print_single(s)


if __name__ == "__main__":
    main()
