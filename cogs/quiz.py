import discord
from discord.ext import commands
from discord.ui import Button, View
import json
import os
import random
import re
from utils.ai import generate_dummy_answers

class QuizButton(Button):
    def __init__(self, label, correct):
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.correct = correct

    async def callback(self, interaction: discord.Interaction):
        if self.correct:
            content = "正解だにぇ！🎉\n5分後にまた遊んでにぇ〜"
        else:
            content = "不正解だにぇ...\n5分後にまた挑戦してにぇ〜"
        await interaction.response.edit_message(content=content, view=None,embed=None)

class QuizView(View):
    def __init__(self, correct_answer, answers):
        super().__init__()
        for answer in answers:
            self.add_item(QuizButton(label=answer, correct=answer == correct_answer))

    def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        self.stop()

class QuizCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.quiz_data_path = 'data/quiz_data.json'
        self.quiz_data = self.load_quiz_data()

    def remove_numbers_from_answers(self, answers):
        """ダミーの答えから数字を除去する関数"""
        cleaned_answers = []
        for answer in answers:
            pattern = r'\d+\)\s*|\d+\.\s*'
            cleaned_answer = re.sub(pattern, '', answer)
            cleaned_answers.append(cleaned_answer)
        return cleaned_answers


    def load_quiz_data(self):
        if os.path.exists(self.quiz_data_path):
            with open(self.quiz_data_path, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                else:
                    return []
        return []

    def save_quiz_data(self):
        with open(self.quiz_data_path, 'w') as f:
            json.dump(self.quiz_data, f, ensure_ascii=False, indent=2)
    
    @commands.hybrid_group(name='quiz', invoke_without_command=True)
    async def quiz_group(self, ctx):
        """クイズコマンドのグループにぇ"""
        await ctx.send("クイズコマンドのサブコマンドを使ってにぇ！")

    @quiz_group.command(name='add')
    async def add_quiz(self, ctx, question: str, correct_answer: str):
        """クイズを追加するにぇ"""
        await ctx.send("ダミーの答えを生成しているにぇ...")
        dummy_answers = generate_dummy_answers(correct_answer)
        cleaned_answers = self.remove_numbers_from_answers(dummy_answers)
        cleaned_and_split_answers = []
        for answer in cleaned_answers:
            split_answers = answer.split('\n')
            cleaned_and_split_answers.extend(split_answers)

        all_answers = [correct_answer] + cleaned_and_split_answers
        self.quiz_data.append({
            "question": question,
            "correct_answer": correct_answer,
            "answers": all_answers
        })
        self.save_quiz_data()
        await ctx.send("クイズを追加したにぇ！")

    @quiz_group.command(name='start')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def start_quiz(self, ctx):
        """クイズを開始するにぇ"""
        if not self.quiz_data:
            await ctx.send("クイズがないみたいだにぇ...\n`h/quiz add`でクイズを追加してにぇ！")
            return
        quiz = random.choice(self.quiz_data)
        question = quiz['question']
        correct_answer = quiz['correct_answer']
        answers = quiz['answers']
        random.shuffle(answers)

        embed = discord.Embed(title="クイズの時間だにぇ！", color=discord.Color.blue())
        embed.add_field(name="問題！", value=question, inline=False)
        embed.set_footer(text="下の選択肢から正解の答えを選んでにぇ！")
        view = QuizView(correct_answer=correct_answer, answers=answers)
        await ctx.send(embed=embed, view=view)

    @start_quiz.error
    async def start_quiz_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            remaining_time = error.retry_after
            if remaining_time < 60:
                seconds = int(remaining_time)
                await ctx.send(f"クールダウン中です。{seconds}秒後にもう一度試してください。")
            else:
                minutes = remaining_time // 60
                seconds = remaining_time % 60
                seconds = int(seconds)
                await ctx.send(f"クールダウン中です。{int(minutes)}分{seconds}秒後にもう一度試してください。")
        else:
            await ctx.send("エラーが発生しました。もう一度やり直してください。")

    @quiz_group.command(name='remove')
    async def remove_quiz(self, ctx, question: str):
        """クイズを削除するにぇ"""
        for quiz in self.quiz_data:
            if quiz['question'] == question:
                self.quiz_data.remove(quiz)
                self.save_quiz_data()
                await ctx.send("クイズを削除したにぇ！")
                return
        await ctx.send("そのクイズは見つからなかったにぇ...")

    @quiz_group.command(name='list')
    @commands.is_owner()
    async def list_quiz(self, ctx):
        """クイズのリストを表示するにぇ"""
        if not self.quiz_data:
            await ctx.send("クイズがないみたいだにぇ...\n`h/quiz add`でクイズを追加してにぇ！")
            return
        embed = discord.Embed(title="クイズのリストだにぇ！", color=discord.Color.blue())
        for quiz in self.quiz_data:
            embed.add_field(name=quiz['question'], value=f"正解: {quiz['correct_answer']}", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(QuizCog(bot))