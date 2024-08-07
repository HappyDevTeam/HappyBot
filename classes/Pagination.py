import discord
from typing import Callable, Optional


class Pagination(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, get_page: Callable, timeout: float):
        self.interaction = interaction
        self.get_page = get_page
        self.total_pages: Optional[int] = None
        self.index = 1
        super().__init__(timeout=timeout)

    async def navigate(self):
        emb, self.total_pages = await self.get_page(self.index)
        if self.total_pages == 1:
            await self.interaction.response.send_message(embed=emb)
        elif self.total_pages > 1:  # pyright: ignore
            self.update_buttons()
            await self.interaction.response.send_message(embed=emb, view=self)

    async def edit_page(self, interaction: discord.Interaction):
        emb, self.total_pages = await self.get_page(self.index)
        self.update_buttons()
        await interaction.response.edit_message(embed=emb, view=self)

    def update_buttons(self):
        self.children[0].disabled = self.index == 1  # pyright: ignore
        self.children[1].disabled = self.index == 1  # pyright: ignore
        self.children[2].disabled = self.index == self.total_pages  # pyright: ignore
        self.children[3].disabled = self.index == self.total_pages  # pyright: ignore

    @discord.ui.button(emoji="⏮️", style=discord.ButtonStyle.blurple)  # pyright: ignore
    async def start(self, interaction: discord.Interaction, button: discord.Button):
        self.index = 1
        await self.edit_page(interaction)

    @discord.ui.button(emoji="◀️", style=discord.ButtonStyle.blurple)  # pyright: ignore
    async def previous(self, interaction: discord.Interaction, button: discord.Button):
        self.index -= 1  # pyright: ignore
        await self.edit_page(interaction)

    @discord.ui.button(emoji="▶️", style=discord.ButtonStyle.blurple)  # pyright: ignore
    async def next(self, interaction: discord.Interaction, button: discord.Button):
        self.index += 1  # pyright: ignore
        await self.edit_page(interaction)

    @discord.ui.button(emoji="⏭️", style=discord.ButtonStyle.blurple)  # pyright: ignore
    async def end(self, interaction: discord.Interaction, button: discord.Button):
        self.index = self.total_pages
        await self.edit_page(interaction)

    async def on_timeout(self):
        # remove buttons on timeout
        message = await self.interaction.original_response()
        await message.edit(view=None)

    @staticmethod
    def compute_total_pages(total_results: int, results_per_page: int) -> int:
        return ((total_results - 1) // results_per_page) + 1
