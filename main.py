import os
import asyncio
from datetime import datetime
import discord
from discord.ext import commands
from study_field_quiz.src.db import init_db, save_response

INTENTS = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=INTENTS, help_command=None)

# Simple quiz data (ganti/luaskan sesuai kebutuhan)
QUESTIONS = [
    {
        "text": "Bidang kuliah mana yang paling kamu suka?",
        "options": ["Teknik Informatika", "Akuntansi", "Psikologi", "Desain"],
    },
    {
        "text": "Suka bekerja sama di tim atau sendiri?",
        "options": ["Tim", "Sendiri", "Keduanya", "Tergantung"],
    },
    {
        "text": "Apa tujuan karier utamamu?",
        "options": ["Manajerial", "Teknis", "Kreatif", "Wirausaha"],
    },
    {

    }
]

class QuizView(discord.ui.View):
    def __init__(self, user_id: int, question_index: int = 0):
        super().__init__(timeout=120)  # timeout dalam detik
        self.user_id = user_id
        self.question_index = question_index
        self.add_option_buttons()

    def add_option_buttons(self):
        # clear existing items (on rebuild)
        for item in list(self.children):
            self.remove_item(item)
        q = QUESTIONS[self.question_index]
        for opt in q["options"]:
            btn = discord.ui.Button(label=opt, style=discord.ButtonStyle.primary)
            # set callback via closure
            async def _callback(interaction: discord.Interaction, choice=opt):
                if interaction.user.id != self.user_id:
                    await interaction.response.send_message("Ini bukan quiz kamu.", ephemeral=True)
                    return
                # simpan ke DB
                await save_response(
                    user_id=self.user_id,
                    username=str(interaction.user),
                    question=q["text"],
                    answer=choice,
                )
                await interaction.response.defer()  # acknowledge
                # lanjut ke pertanyaan berikutnya atau selesai
                if self.question_index + 1 < len(QUESTIONS):
                    self.question_index += 1
                    self.add_option_buttons()
                    new_q = QUESTIONS[self.question_index]["text"]
                    await interaction.followup.send(f"Pertanyaan berikutnya: {new_q}", view=self, ephemeral=True)
                else:
                    await interaction.followup.send("Terima kasih! Quiz selesai.", ephemeral=True)
                    self.stop()
            btn.callback = _callback
            self.add_item(btn)

@bot.command(name="quiz")
async def start_quiz(ctx: commands.Context):
    """Mulai quiz singkat (jawaban disimpan ke DB)."""
    view = QuizView(user_id=ctx.author.id, question_index=0)
    q0 = QUESTIONS[0]["text"]
    await ctx.author.send(f"Mulai quiz:\n{q0}", view=view)
    await ctx.send(f"{ctx.author.mention}, aku sudah kirim DM untuk quiz.")

@bot.event
async def on_ready():
    print(f"Bot ready as {bot.user} ({bot.user.id})")

async def main():
    await init_db()  # pastikan DB siap
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("Set DISCORD_TOKEN environment variable.")
    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())