from datetime import datetime, timedelta
from time import mktime

from discord.message import Message
from discord.channel import TextChannel
from discord.embeds import Embed
from discord.colour import Colour
from discord.guild import Member, Guild

from cfg import default_embeds_colour, prefix, DEFAULT_PORT
from Logger import Logger

class MessageSender():
    @classmethod
    def __getDiscordNowTime(cls):
        return f"<t:{int(mktime(datetime.now().timetuple()))}>"

    @classmethod
    async def sendEmbed(cls, channel: TextChannel, fields: list[list[str]], thumbnail_url="", colour: Colour=default_embeds_colour, guild_thumbnail: bool=False, guild_footer=True, delete_after=-1, author: Member=None):
        embed_ = Embed(colour=colour)
        if len(fields) != 2:
            raise ValueError(f"fields argument have to have len of 2. Len of fields is {len(fields)}")
        if type(fields[0]) != list or type(fields[1]) != list:
            raise ValueError(f"fields argument have to be list of lists. Got [{type(fields[0])}, {type(fields[1])}]")
        if len(fields[0]) != len(fields[1]):
            raise ValueError(f"'fields's inner lists must be same size. Sizes are {len(fields[0])} and {len(fields[1])}")

        for i in range(len(fields[0])):
            embed_.add_field(name=fields[0][i], value=fields[1][i], inline=False)

        try:
            guild_icon_url = channel.guild.icon_url
        except ValueError:
            guild_icon_url = None

        if guild_thumbnail and guild_icon_url:
            embed_.set_thumbnail(url=guild_icon_url)
        if thumbnail_url != "":
            embed_.set_thumbnail(url=thumbnail_url)

        if guild_footer and guild_icon_url:
            embed_.set_footer(text="mcOnline | Found bug? Contact Affenmilchmann#2363", icon_url=guild_icon_url)

        if author:
            embed_.set_author(name=str(author.name)+'#'+str(author.discriminator), icon_url=author.avatar_url)

        if delete_after > 0:
            return await channel.send(embed=embed_, delete_after=delete_after)
        else:
            return await channel.send(embed=embed_)

    @classmethod 
    def __formPlayerListStr(cls, player_list: list[str], connection=True) -> str:
        player_list_str = ""
        if connection:
            for player in player_list:
                player_list_str += f"`{cls.clearFromFormattingChars(player)}`\n"
            player_list_str = player_list_str[:900]
            if len(player_list) == 0:
                player_list_str = "Nobody is online!\n"
        else:
            player_list_str = "Server is offline\n"
        player_list_str += f"\n *Last update: {cls.__getDiscordNowTime()}*"
        return player_list_str

    @classmethod
    async def sendOnlineMsg(cls, channel: TextChannel, player_list: list[str], connection=True):
        return await cls.sendEmbed(
            channel, 
            [["**Online players:**"],
            [cls.__formPlayerListStr(player_list, connection)]],
        )

    @classmethod
    async def editOnlineMsg(cls, message: Message, player_list: list[str], connection=True):
        if len(message.embeds) == 0:
            Logger.printLog(f"Message with id {message.id} was edited but it has 0 embeds to edit")
            return
        embed_: Embed = message.embeds[0]
        embed_.clear_fields()
        embed_.add_field(name="**Online players:**", value=cls.__formPlayerListStr(player_list, connection))
        await message.edit(embed=embed_)

    @classmethod
    async def sendGuildInited(cls, channel: TextChannel):
        await cls.sendEmbed(
            channel,
            [["**Your server was linked!**", "*Friendly reminder:*"],
            ["Before creating online player list message consider setting manager role and minecraft server ip.",
            "*This bot requires mcOnline plugin running on the server*"]],
            guild_thumbnail=True
        )

    @classmethod
    async def sendGuildAlreadyInited(cls, channel: TextChannel):
        await cls.sendEmbed(
            channel,
            [["**Oops!**"],
            ["Your server is already linked"]],
        )

    @classmethod
    async def sendInvalidSyntax(cls, channel: TextChannel, message: str):
        await cls.sendEmbed(
            channel,
            [["**Invalid syntax**"],
            [message]],
            colour=Colour.red()
        )

    @classmethod
    async def sendParameterSet(cls, channel: TextChannel, parameter_name: str, parameter_val: str):
        await cls.sendEmbed(
            channel,
            [["**Success!**"],
            [f"{parameter_name} was set to {parameter_val}"]],
        )

    @classmethod
    async def sendNotSetUp(cls, channel: TextChannel):
        await cls.sendEmbed(
            channel,
            [["**Server is not set up!**"],
            [f"Use `{prefix}start` first. Then make sure you set up your server's ip with `{prefix}set_ip`"]],
            colour=Colour.red()
        )

    @classmethod
    async def sendMessageMissing(cls, channel: TextChannel):
        await cls.sendEmbed(
            channel,
            [["**Cant find online list message!**"],
            [f"If message is present and you see this, delete online list message yourself"]],
            colour=Colour.red()
        )
        
    @classmethod
    async def sendMessageDeleted(cls, channel: TextChannel):
        await cls.sendEmbed(
            channel,
            [["**Message was deleted!**"],
            [f"-"]],
        )

    @classmethod
    async def sendCantConnect(cls, channel: TextChannel):
        await cls.sendEmbed(
            channel,
            [["**Failed to connect to minecraft server**"],
            [f"Make sure you have\n \
                installed mcOnline plugin\n \
                port {DEFAULT_PORT} is opened on your server"]],
            colour=Colour.red()
        )

    @classmethod
    async def sendCfg(cls, channel: TextChannel, cfg_data: dict):
        titels = []
        values = []
        titels.append("**Manager role**")
        values.append("> Missing" if cfg_data["mgr_role"] == -1 else f"> <@&{cfg_data['mgr_role']}>")
        titels.append("**Channel**")
        values.append("> Missing" if cfg_data["channel"] == -1 else f"> <#{cfg_data['channel']}>")
        titels.append("**Online list message**")
        values.append("> Missing" if cfg_data["message"] == -1 else "> Present")
        titels.append("**Server IP**")
        values.append(f"> {cfg_data['server_ip']}")
        await cls.sendEmbed(
            channel,
            [titels, values],
        )

    @classmethod
    async def sendUnknownCommand(cls, channel: TextChannel):
        await cls.sendEmbed(
            channel,
            [["**Unknown command!**"],
            [f"Try `{prefix}help`"]],
            colour=Colour.red()
        )

    @classmethod
    async def sendNotPermitted(cls, channel: TextChannel):
        await cls.sendEmbed(
            channel,
            [["**You are not permitted to use this command!**"],
            [f"-"]],
            colour=Colour.red()
        )

    @classmethod
    def clearFromFormattingChars(cls, inp: str) -> str:
        while "§" in inp:
            idx_ = inp.find("§")
            if idx_ + 2 <= len(inp):
                inp = inp[:idx_] + inp[idx_ + 2:]
            else:
                inp = inp[:idx_] + inp[idx_ + 1:]
        return inp