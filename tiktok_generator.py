"""
TikTok Content Auto-Generator — Gaya Ferry Irwandi
Untuk promosi e-book AI / Claude Prompt

Cara pakai:
  1. pip install anthropic
  2. Set API key: export ANTHROPIC_API_KEY="sk-ant-..."
  3. Jalankan: python tiktok_generator.py
  4. Atau generate batch: python tiktok_generator.py --batch 5 --output konten_minggu_ini.md
"""

import anthropic
import argparse
import json
import random
from datetime import datetime, timedelta
from pathlib import Path


# ─── Konfigurasi ────────────────────────────────────────────────────────────

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

TONES = [
    "santai tapi berbobot, seperti ngobrol sama teman yang lebih tau",
    "direct dan to-the-point, tanpa basa-basi",
    "sedikit provokatif tapi tetap membangun",
    "penuh empati, seolah benar-benar ngerti struggle audiensnya",
]


# ─── Generator Utama ─────────────────────────────────────────────────────────

def generate_tiktok_script(
    client: anthropic.Anthropic,
    format_konten: dict,
    topik_spesifik: str = None,
    tone: str = None,
) -> dict:
    """Generate satu skrip TikTok lengkap."""

    tone = tone or random.choice(TONES)
    topik = topik_spesifik or random.choice([
        "cara pakai Claude untuk nulis email profesional",
        "prompt untuk riset bisnis dalam 5 menit",
        "belajar skill baru 3x lebih cepat dengan AI",
        "cara AI bantu Gen Z dapat side income",
        "prompt untuk persiapan interview kerja",
        "AI untuk nulis CV dan cover letter",
        "cara pakai AI buat presentasi yang meyakinkan",
        "prompt untuk analisis kompetitor bisnis",
    ])

    system_prompt = """Kamu adalah content creator TikTok Indonesia yang ahli di bidang AI dan produktivitas.
Gaya kamu persis seperti Ferry Irwandi: bicara natural, buka dengan konflik atau fakta mengejutkan,
jelasin hal rumit pakai analogi sederhana, selipkan sisi manusia lewat cerita personal.

ATURAN PENULISAN:
- Kalimat pendek-pendek. Maksimal 10 kata per kalimat.
- Sering pakai baris kosong untuk jeda dramatik
- Bahasa Indonesia campur sedikit Inggris (natural, bukan sok keren)
- JANGAN pakai kata: "kawan", "teman-teman", "guys", "sob"
- Mulai dengan hook yang bikin orang berhenti scroll dalam 3 detik pertama
- Durasi bicara: 45-60 detik (sekitar 120-150 kata)
- Akhiri dengan insight kuat, BUKAN dengan "semoga bermanfaat" atau sejenisnya

OUTPUT FORMAT (JSON):
{
  "hook": "kalimat pembuka saja",
  "script": "skrip lengkap dengan baris kosong sebagai jeda",
  "hashtags": ["#tag1", "#tag2", ...],
  "durasi_estimasi": "XX detik",
  "tips_delivery": "1 tips cara bawain video ini"
}"""

    user_prompt = f"""Buatkan skrip TikTok dengan format: {format_konten['nama']}
Deskripsi format: {format_konten['deskripsi']}
Contoh hook referensi (jangan copy, cari yang lebih segar): {format_konten['contoh_hook']}

Topik spesifik: {topik}
Tone: {tone}

Konteks e-book yang dipromosikan:
{EBOOK_CONTEXT}

Ingat: skrip ini untuk VIDEO, bukan tulisan. Tulis seperti orang ngomong, bukan seperti artikel.
Balas HANYA dengan JSON, tanpa teks lain."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": user_prompt}],
        system=system_prompt,
    )

    raw = response.content[0].text.strip()

    # Bersihkan jika ada markdown fence
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    result = json.loads(raw)
    result["format"] = format_konten["nama"]
    result["topik"] = topik
    result["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    return result


def generate_daily_batch(
    client: anthropic.Anthropic,
    jumlah: int = 5,
) -> list[dict]:
    """Generate sejumlah skrip sekaligus dengan format yang beragam."""

    print(f"\n🎬 Generating {jumlah} skrip TikTok...\n")

    # Pastikan format beragam — tidak ada yang sama berturut-turut
    formats = (CONTENT_FORMATS * 3)[:jumlah]
    random.shuffle(formats)

    results = []
    for i, fmt in enumerate(formats, 1):
        print(f"  [{i}/{jumlah}] Format: {fmt['nama']}...", end=" ", flush=True)
        try:
            script = generate_tiktok_script(client, fmt)
            results.append(script)
            print("✓")
        except Exception as e:
            print(f"✗ Error: {e}")

    return results


# ─── Output Formatter ────────────────────────────────────────────────────────

def format_markdown(scripts: list[dict], mulai_tanggal: str = None) -> str:
    """Format hasil sebagai Markdown siap copy-paste."""

    tanggal = datetime.strptime(mulai_tanggal, "%Y-%m-%d") if mulai_tanggal else datetime.today()
    lines = [
        f"# Content TikTok — E-book AI",
        f"Dibuat: {datetime.now().strftime('%d %B %Y, %H:%M')}",
        f"Total: {len(scripts)} skrip\n",
        "---\n",
    ]

    for i, s in enumerate(scripts, 1):
        posting_date = (tanggal + timedelta(days=i - 1)).strftime("%A, %d %B %Y")
        lines.append(f"## Video {i} — {posting_date}")
        lines.append(f"**Format:** {s.get('format', '-')}")
        lines.append(f"**Topik:** {s.get('topik', '-')}")
        lines.append(f"**Durasi:** {s.get('durasi_estimasi', '-')}")
        lines.append(f"**Dibuat:** {s.get('generated_at', '-')}\n")
        lines.append(f"### Hook")
        lines.append(f"> {s.get('hook', '')}\n")
        lines.append(f"### Skrip Lengkap")
        lines.append("```")
        lines.append(s.get("script", ""))
        lines.append("```\n")
        lines.append(f"### Hashtags")
        lines.append(" ".join(s.get("hashtags", [])))
        lines.append(f"\n### Tips Delivery")
        lines.append(f"💡 {s.get('tips_delivery', '-')}")
        lines.append("\n---\n")

    return "\n".join(lines)


def print_single(s: dict):
    """Print satu skrip ke terminal."""
    print("\n" + "=" * 60)
    print(f"FORMAT  : {s.get('format')}")
    print(f"TOPIK   : {s.get('topik')}")
    print(f"DURASI  : {s.get('durasi_estimasi')}")
    print(f"DIBUAT  : {s.get('generated_at')}")
    print("-" * 60)
    print(f"HOOK:\n  {s.get('hook')}")
    print("-" * 60)
    print("SKRIP:")
    print(s.get("script", ""))
    print("-" * 60)
    print("HASHTAGS:", " ".join(s.get("hashtags", [])))
    print(f"TIPS    : {s.get('tips_delivery')}")
    print("=" * 60 + "\n")


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Auto-generate skrip TikTok harian pakai Claude AI"
    )
    parser.add_argument(
        "--batch", type=int, default=1,
        help="Jumlah skrip yang di-generate (default: 1)"
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Simpan ke file .md (contoh: konten_minggu_ini.md)"
    )
    parser.add_argument(
        "--format", type=str, default=None,
        choices=[f["nama"] for f in CONTENT_FORMATS],
        help="Pilih format spesifik (opsional)"
    )
    parser.add_argument(
        "--topik", type=str, default=None,
        help="Topik spesifik yang ingin dibahas (opsional)"
    )
    parser.add_argument(
        "--mulai-tanggal", type=str, default=None,
        help="Tanggal mulai posting untuk kalender (format: YYYY-MM-DD)"
    )
    parser.add_argument(
        "--list-format", action="store_true",
        help="Tampilkan semua format yang tersedia"
    )
    args = parser.parse_args()

    # Tampilkan daftar format
    if args.list_format:
        print("\nFormat konten yang tersedia:\n")
        for i, f in enumerate(CONTENT_FORMATS, 1):
            print(f"  {i}. {f['nama']}")
            print(f"     {f['deskripsi']}")
            print(f"     Contoh hook: \"{f['contoh_hook']}\"\n")
        return

    # Inisialisasi client
    client = anthropic.Anthropic()  # Otomatis baca ANTHROPIC_API_KEY dari env

    print("🤖 TikTok Content Generator — E-book AI")
    print("   Model: claude-sonnet-4-20250514")

    if args.batch == 1:
        # Generate satu skrip
        fmt = next((f for f in CONTENT_FORMATS if f["nama"] == args.format), None) \
              or random.choice(CONTENT_FORMATS)
        print(f"\nGenerating 1 skrip (format: {fmt['nama']})...", end=" ", flush=True)
        script = generate_tiktok_script(client, fmt, topik_spesifik=args.topik)
        print("✓")
        print_single(script)
        scripts = [script]
    else:
        # Generate batch
        scripts = generate_daily_batch(client, jumlah=args.batch)

    # Simpan ke file jika diminta
    if args.output:
        md = format_markdown(scripts, mulai_tanggal=args.mulai_tanggal)
        Path(args.output).write_text(md, encoding="utf-8")
        print(f"\n✅ Tersimpan di: {args.output}")
        print(f"   Total: {len(scripts)} skrip siap posting")
    else:
        if args.batch > 1:
            for s in scripts:
                print_single(s)

    print(f"\n💡 Tips: Jalankan setiap pagi dengan cron job:")
    print(f"   0 7 * * * cd /path/to/folder && python tiktok_generator.py --batch 3 --output konten_hari_ini.md\n")


if __name__ == "__main__":
    main()
