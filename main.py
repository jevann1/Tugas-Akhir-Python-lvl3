import os
import asyncio
from datetime import datetime
import discord
from collections import Counter
from discord.ext import commands
from study_field_quiz.src.db import init_db, save_response
from config import TOKEN

INTENTS = discord.Intents.default()
INTENTS.message_content = True
bot = commands.Bot(command_prefix="!", intents=INTENTS, help_command=None)

# Quiz questions
QUESTIONS = [
    {"text": "Mata pelajaran apa yang paling kamu sukai di sekolah?", "options": ["Matematika", "Sains", "Seni", "Bahasa"]},
    {"text": "Suka bekerja sama di tim atau sendiri?", "options": ["Tim", "Sendiri", "Keduanya", "Tergantung"]},
    {"text": "Apa tujuan karier utamamu?", "options": ["Manajerial", "Teknis", "Kreatif", "Wirausaha"]},
    {"text": "Seberapa penting keseimbangan kerja dan hidup bagimu?", "options": ["Sangat penting", "Cukup penting", "Tidak terlalu penting", "Tidak penting sama sekali"]},
    {"text": "Apakah kamu lebih suka bekerja di lingkungan yang terstruktur atau fleksibel?", "options": ["Terstruktur", "Fleksibel", "Keduanya", "Tergantung situasi"]},
    {"text": "Seberapa suka kamu dengan hal yang berbasis teknologi?", "options": ["Sangat suka", "Cukup suka", "Sedikit suka", "Tidak suka"]},
    {"text": "Aktivitas seperti apa yang membuatmu lupa waktu saat melakukannya?", "options": ["Membaca", "Olahraga", "Berkreasi seni", "Bermain alat/tech"]},
    {"text": "Kamu lebih suka bekerja dengan data & angka, orang & emosi, atau alat & benda nyata?", "options": ["Data & angka", "Orang & emosi", "Alat & benda nyata", "Campuran"]},
    {"text": "Kamu lebih suka memecahkan masalah logika atau mengekspresikan ide kreatif?", "options": ["Memecahkan logika", "Mengekspresikan kreatif", "Keduanya", "Tergantung masalah"]},
    {"text": "Topik apa yang sering kamu cari tahu secara sukarela di internet atau YouTube?", "options": ["Teknologi", "Seni & Desain", "Bisnis & Kewirausahaan", "Pengembangan Diri"]},
    {"text": "Kamu lebih mudah memahami lewat praktik, penjelasan logis, atau visualisasi?", "options": ["Praktik langsung", "Penjelasan logis", "Visualisasi/gambar", "Gabungan"]},
    {"text": "Menurut teman atau guru, kamu kuat di bidang apa?", "options": ["Komunikasi", "Analisis", "Seni", "Kepemimpinan"]},
    {"text": "Apakah kamu tipe yang teliti & sistematis, atau imajinatif & spontan?", "options": ["Teliti & sistematis", "Imajinatif & spontan", "Keduanya", "Tergantung situasi"]},
    {"text": "Bagaimana kamu menangani tugas sulit — sendiri, diskusi, atau coba berbagai cara?", "options": ["Berpikir sendiri", "Diskusi dengan orang lain", "Mencoba berbagai cara", "Minta bantu"]},
    {"text": "Apa yang paling kamu inginkan dari pekerjaan masa depan?", "options": ["Stabilitas", "Penghasilan tinggi", "Pengaruh sosial", "Kreativitas"]},
    {"text": "Kamu ingin pekerjaan yang membantu orang langsung atau menghasilkan inovasi/produk baru?", "options": ["Membantu orang langsung", "Menghasilkan inovasi/produk", "Keduanya", "Tidak pasti"]},
    {"text": "Seberapa penting bekerja di luar negeri / fleksibilitas waktu / berdampak sosial bagimu?", "options": ["Sangat penting", "Penting", "Biasa saja", "Tidak penting"]},
    {"text": "Kamu lebih suka bekerja sendiri atau dalam tim?", "options": ["Sendiri", "Dalam tim", "Tergantung pekerjaan", "Keduanya"]},
    {"text": "Kamu nyaman dengan rutinitas atau lebih suka tantangan baru tiap waktu?", "options": ["Suka rutinitas", "Suka tantangan baru", "Keduanya", "Tergantung"]},
    {"text": "Kamu lebih suka bekerja di dalam ruangan dengan komputer, di lapangan, atau interaksi langsung?", "options": ["Dalam ruangan (komputer)", "Di lapangan", "Interaksi banyak orang", "Campuran"]},
    {"text": "Jika uang & waktu bukan masalah, kegiatan apa yang mau kamu lakukan setiap hari?", "options": ["Belajar & riset", "Berkarya seni/kreasi", "Melancong & eksplorasi", "Membantu orang"]},
    {"text": "Siapa tokoh yang kamu kagumi — dan apa yang kamu kagumi darinya?", "options": ["Pemimpin/activist", "Ilmuwan/teknolog", "Seniman/creator", "Pengusaha/inovator"]},
    {"text": "Bayangkan 10 tahun ke depan — kamu ingin dikenal sebagai orang seperti apa?", "options": ["Pemimpin", "Ahli teknis", "Kreator", "Pengusaha/innovator"]},
]

# mapping options to fields (used to pick relevant fields)
OPTION_TO_CATEGORY = {
    "Matematika": ["Sains & Matematika"], "Sains": ["Sains & Matematika"], "Seni": ["Seni & Desain"], "Bahasa": ["Komunikasi & Humaniora"],
    "Tim": ["Komunikasi & Humaniora", "Bisnis & Manajemen"], "Sendiri": ["Riset & Teknologi"], "Keduanya": ["Interdisipliner"], "Tergantung": ["Interdisipliner"],
    "Manajerial": ["Bisnis & Manajemen"], "Teknis": ["Teknologi & IT", "Teknik & Rekayasa"], "Kreatif": ["Seni & Desain"], "Wirausaha": ["Kewirausahaan", "Bisnis & Manajemen"],
    "Sangat penting": ["Humaniora & Sosial"], "Cukup penting": ["Humaniora & Sosial"], "Tidak terlalu penting": ["Teknologi & IT"], "Tidak penting sama sekali": ["Teknologi & IT"],
    "Terstruktur": ["Teknik & Rekayasa", "Bisnis & Manajemen"], "Fleksibel": ["Seni & Desain", "Kewirausahaan"], "Tergantung situasi": ["Interdisipliner"],
    "Sangat suka": ["Teknologi & IT"], "Cukup suka": ["Teknologi & IT"], "Sedikit suka": ["Seni & Desain"], "Tidak suka": ["Humaniora & Sosial"],
    "Membaca": ["Humaniora & Penelitian"], "Olahraga": ["Kesehatan & Olahraga"], "Berkreasi seni": ["Seni & Desain"], "Bermain alat/tech": ["Teknologi & IT"],
    "Data & angka": ["Sains & Matematika", "Teknologi & IT"], "Orang & emosi": ["Psikologi & Humaniora"], "Alat & benda nyata": ["Teknik & Rekayasa"], "Campuran": ["Interdisipliner"],
    "Memecahkan logika": ["Teknologi & IT", "Sains & Matematika"], "Mengekspresikan kreatif": ["Seni & Desain"],
    "Teknologi": ["Teknologi & IT"], "Seni & Desain": ["Seni & Desain"], "Bisnis & Kewirausahaan": ["Bisnis & Manajemen"], "Pengembangan Diri": ["Humaniora & Sosial"],
    "Praktik langsung": ["Teknik & Terapan"], "Penjelasan logis": ["Sains & Matematika"], "Visualisasi/gambar": ["Seni & Desain"], "Gabungan": ["Interdisipliner"],
    "Komunikasi": ["Komunikasi & Humaniora"], "Analisis": ["Sains & Matematika"], "Kepemimpinan": ["Bisnis & Manajemen"],
    "Teliti & sistematis": ["Sains & Rekayasa"], "Imajinatif & spontan": ["Seni & Desain"],
    "Berpikir sendiri": ["Riset & Teknologi"], "Diskusi dengan orang lain": ["Komunikasi & Humaniora"], "Mencoba berbagai cara": ["Teknik & Desain"],
    "Stabilitas": ["Bisnis & Manajemen"], "Penghasilan tinggi": ["Bisnis & Manajemen"], "Pengaruh sosial": ["Humaniora & Sosial"], "Kreativitas": ["Seni & Desain"],
    "Membantu orang langsung": ["Kesehatan & Sosial"], "Menghasilkan inovasi/produk": ["Teknologi & Rekayasa"],
    "Dalam ruangan (komputer)": ["Teknologi & IT"], "Di lapangan": ["Kesehatan & Terapan"], "Interaksi banyak orang": ["Komunikasi & Humaniora"],
    "Belajar & riset": ["Riset & Akademik"], "Berkarya seni/kreasi": ["Seni & Desain"], "Melancong & eksplorasi": ["Hospitality & Pariwisata"], "Membantu orang": ["Kesehatan & Sosial"],
    "Pemimpin/activist": ["Bisnis & Manajemen", "Humaniora & Sosial"], "Ilmuwan/teknolog": ["Sains & Teknologi"], "Seniman/creator": ["Seni & Desain"], "Pengusaha/inovator": ["Kewirausahaan"],
    "Pemimpin": ["Bisnis & Manajemen"], "Ahli teknis": ["Teknologi & IT"], "Kreator": ["Seni & Desain"], "Pengusaha/innovator": ["Kewirausahaan"],
}

def map_option_to_fields(option: str):
    """Heuristik pemetaan jawaban ke 1+ bidang."""
    o = option.lower()
    fields = []
    if any(k in o for k in ("matematika", "data", "angka", "analisis", "logika", "memecahkan")):
        fields.append("Teknologi & Ilmu Data")
    if any(k in o for k in ("sains", "ilmuwan", "riset")):
        fields.append("Sains & Riset")
    if any(k in o for k in ("seni", "kreatif", "desain", "creator", "berkreasi")):
        fields.append("Seni & Desain")
    if any(k in o for k in ("bahasa", "komunikasi", "pengaruh", "pengembangan diri")):
        fields.append("Humaniora & Sosial")
    if any(k in o for k in ("wirausaha", "pengusaha", "bisnis", "manajer", "manajerial")):
        fields.append("Bisnis & Manajemen")
    if any(k in o for k in ("teknis", "teknologi", "alat", "tech", "komputer")):
        fields.append("Teknologi & IT")
    if any(k in o for k in ("membantu", "langsung", "melayani", "kesehatan")):
        fields.append("Kesehatan & Pelayanan")
    if any(k in o for k in ("lapangan", "praktik", "terapan", "teknik")):
        fields.append("Teknik & Terapan")
    if not fields:
        fields.append("Umum / Multidisiplin")
    return fields

def compute_suggestion(answers):
    """
    Hitung skor bidang dari daftar jawaban.
    Kembalikan 3 bidang teratas berdasarkan jawaban.
    """
    counter = Counter()
    # Hitung skor untuk setiap jawaban
    for answer in answers:
        if answer in OPTION_TO_CATEGORY:
            fields = OPTION_TO_CATEGORY[answer]
            for field in fields:
                counter[field] += 1
    
    if not counter:
        return (["Tidak cukup data"], {})

    # Ambil 3 bidang dengan skor tertinggi
    top_fields = [field for field, _ in counter.most_common(3)]
    
    # Detail untuk 3 bidang teratas
    details = {
        "Teknologi & IT": {
            "desc": "Fokus pada pengembangan software dan sistem IT",
            "jobs": ["Software Developer", "System Engineer", "IT Consultant"]
        },
        "Sains & Matematika": {
            "desc": "Fokus pada penelitian ilmiah dan analisis matematis",
            "jobs": ["Data Scientist", "Peneliti", "Analis Kuantitatif"]
        },
        "Seni & Desain": {
            "desc": "Fokus pada kreativitas dan desain visual",
            "jobs": ["UI/UX Designer", "Graphic Designer", "Digital Artist"]
        },
        "Bisnis & Manajemen": {
            "desc": "Fokus pada pengelolaan bisnis dan kepemimpinan",
            "jobs": ["Business Manager", "Project Manager", "Consultant"]
        },
        "Komunikasi & Humaniora": {
            "desc": "Fokus pada interaksi manusia dan komunikasi",
            "jobs": ["Content Creator", "PR Specialist", "Communications Officer"]
        },
        "Teknik & Rekayasa": {
            "desc": "Fokus pada pengembangan teknologi praktis",
            "jobs": ["Software Engineer", "System Architect", "DevOps Engineer"]
        },
        "Kesehatan & Sosial": {
            "desc": "Fokus pada pelayanan kesehatan dan sosial",
            "jobs": ["Healthcare IT", "Medical Technologist", "Health Informatics"]
        },
        "Kewirausahaan": {
            "desc": "Fokus pada inovasi dan membangun bisnis",
            "jobs": ["Tech Entrepreneur", "Startup Founder", "Business Developer"]
        }
    }

    return top_fields, details

class QuizView(discord.ui.View):
    def __init__(self, user_id: int, question_index: int = 0):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.question_index = question_index
        self.answers = []
        self.add_option_buttons()

    def add_option_buttons(self):
        # clear existing items (on rebuild)
        for item in list(self.children):
            self.remove_item(item)
        q = QUESTIONS[self.question_index]
        local_q_text = q["text"]
        local_index = self.question_index
        for opt in q["options"]:
            btn = discord.ui.Button(label=opt, style=discord.ButtonStyle.primary)
            async def _callback(interaction: discord.Interaction, choice=opt, qtext=local_q_text, qidx=local_index):
                if interaction.user.id != self.user_id:
                    await interaction.response.send_message("Ini bukan quiz kamu.", ephemeral=True)
                    return
                # simpan ke DB (tahan error supaya tidak crash)
                try:
                    await save_response(user_id=self.user_id, username=str(interaction.user), question=qtext, answer=choice)
                except Exception:
                    pass
                # catat jawaban
                self.answers.append(choice)

                # jika masih ada pertanyaan berikutnya -> rebuild view dan edit message
                if self.question_index + 1 < len(QUESTIONS):
                    self.question_index += 1
                    self.add_option_buttons()
                    next_q = QUESTIONS[self.question_index]["text"]
                    # edit pesan asli supaya menampilkan pertanyaan berikutnya dan view yang diperbarui
                    try:
                        await interaction.response.edit_message(content=f"Pertanyaan berikutnya: {next_q}", view=self)
                    except Exception:
                        # fallback: kirim pesan baru (ephemeral) jika edit gagal
                        await interaction.response.send_message(f"Pertanyaan berikutnya: {next_q}", view=self, ephemeral=True)
                else:
                    suggested_fields, details = compute_suggestion(self.answers)
                    lines = ["🎓 Berdasarkan jawabanmu, 3 bidang yang paling cocok:"]
                    
                    for i, field in enumerate(suggested_fields, 1):
                        info = details.get(field, {})
                        desc = info.get("desc", "")
                        jobs = ", ".join(info.get("jobs", []))
                        lines.append(f"\n{i}. {field}")
                        lines.append(f"   {desc}")
                        lines.append(f"   Contoh karier: {jobs}")
                    
                    summary_text = "\n".join(lines)
                    try:
                        await interaction.response.edit_message(content=summary_text, view=None)
                    except Exception:
                        await interaction.response.send_message(summary_text, ephemeral=True)
                    # kirim DM ringkasan (opsional)
                    try:
                        await interaction.user.send(summary_text)
                    except Exception:
                        pass
                    self.stop()
                    # ===============================================
            btn.callback = _callback
            self.add_item(btn)
    

@bot.command(name="quiz")
async def start_quiz(ctx: commands.Context):
    """Mulai quiz singkat (jawaban disimpan ke DB)."""
    view = QuizView(user_id=ctx.author.id, question_index=0)
    q0 = QUESTIONS[0]["text"]
    try:
        await ctx.author.send(f"Mulai quiz:\n{q0}", view=view)
        await ctx.send(f"{ctx.author.mention}, aku sudah kirim DM untuk quiz.")
    except discord.Forbidden:
        await ctx.send(f"{ctx.author.mention}, aku tidak bisa mengirim DM. Buka DM agar quiz bisa dimulai.")

@bot.event
async def on_ready():
    print(f"Bot ready as {bot.user} ({bot.user.id})")

async def main():
    await init_db()
    token = TOKEN
    if not token:
        raise RuntimeError("Set DISCORD_TOKEN environment variable.")
    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
