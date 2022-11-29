import datetime
import itertools
from utils.music.models import LavalinkPlayer
import disnake
from utils.music.converters import time_format, fix_characters


def load(player: LavalinkPlayer) -> dict:

    data = {
        "content": None,
        "embeds": [],
    }

    embed_color = player.bot.get_color(player.guild.me)

    embed = disnake.Embed(
        color=embed_color,
        description=f"[`{player.current.single_title}`]({player.current.uri})"
    )
    embed_queue = None
    queue_size = len(player.queue)

    if not player.paused:
        embed.set_author(
            name="Tocando Agora:",
            icon_url="https://media.discordapp.net/attachments/480195401543188483/987633257178882108/Equalizer.gif",
        )

    else:
        embed.set_author(
            name="Em Pausa:",
            icon_url="https://cdn.discordapp.com/attachments/480195401543188483/896013933197013002/pause.png"
        )

    if player.current.track_loops:
        embed.description += f" `[🔂 {player.current.track_loops}]`"

    elif player.loop:
        if player.loop == 'current':
            embed.description += ' `[🔂 música atual]`'
        else:
            embed.description += ' `[🔁 fila]`'

    embed.description += f" `[`<@{player.current.requester}>`]`"

    duration = "🔴 Livestream" if player.current.is_stream else \
        time_format(player.current.duration)

    embed.add_field(name="⏰ **⠂Duração:**", value=f"```ansi\n[34;1m{duration}[0m\n```")
    embed.add_field(name="💠 **⠂Uploader/Artista:**",
                    value=f"```ansi\n[34;1m{fix_characters(player.current.author, 18)}[0m\n```")

    if player.command_log:
        embed.add_field(name=f"{player.command_log_emoji} **⠂Última Interação:**",
                        value=f"{player.command_log}", inline=False)

    player.mini_queue_feature = True

    if queue_size:

        embed.description += f" `({queue_size})`"

        if player.mini_queue_enabled:
            embed_queue = disnake.Embed(
                color=embed_color,
                description="\n".join(
                    f"`{(n + 1):02}) [{time_format(t.duration) if not t.is_stream else '🔴 Livestream'}]` [`{fix_characters(t.title, 38)}`]({t.uri})"
                    for n, t in (enumerate(itertools.islice(player.queue, 5)))
                )
            )
            embed_queue.set_image(url="https://cdn.discordapp.com/attachments/480195401543188483/795080813678559273/rainbow_bar2.gif")

    embed.set_thumbnail(url=player.current.thumb)
    embed.set_image(url="https://cdn.discordapp.com/attachments/480195401543188483/795080813678559273/rainbow_bar2.gif")

    if player.current_hint:
        embed.set_footer(text=f"💡 Dica: {player.current_hint}")

    player.auto_update = 0

    data["embeds"] = [embed_queue, embed] if embed_queue else [embed]

    return data