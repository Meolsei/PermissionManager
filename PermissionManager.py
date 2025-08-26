import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

client = commands.Bot(command_prefix="~", intents=intents)

@client.event
async def on_ready():
    print(f"Logged in at {client.user}")

@client.command()
@commands.has_permissions(administrator=True)
async def setPermission(ctx, operation: bool, permission: str, role: int):
    guild = ctx.guild
    role = guild.get_role(role)
    channels = []

    if role is None:
        await ctx.send(f"No role found with `{role}`.")
        return

    if permission not in discord.Permissions.VALID_FLAGS:
        await ctx.send("You must specify a valid permission, (e.g., `'send_messages'`)")
        return

    progress = await ctx.send(f"Setting `{permission}` to `{operation}` for `{role.name}`...")

    for idx, channel in enumerate(guild.channels, start=1):
        overwrites = channel.overwrites_for(role)
        value = getattr(overwrites, permission)

        if value == operation:
            print(f"{permission} is already set to {operation} for {channel.name}.")
            continue
    
        try:
            await channel.set_permissions(role, overwrite=discord.PermissionOverwrite(**{permission: operation}))
            channels.append(channel.name)

            await progress.edit(content=(
                    f"Setting `{permission}` to `{operation}` for `{role.name}`...\n"
                    f"Last channel: `{channel.name}` ({idx}/{len(guild.channels)})\n"
                    f"Updated so far: {len(channels)}"
                ))
        
        except Exception as e:
            print(f"{permission} couldn't be set for {channel.name}: {e}")

        await asyncio.sleep(1)

    await progress.edit(content=(
        f"Finished setting `{permission}` to `{operation}` for `{role.name}`...\n"
        f"{len(channels)} have been updated."
    ))

client.run('TOKEN')
