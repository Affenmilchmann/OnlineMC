from datetime import datetime, timedelta
from time import mktime
from typing import List

from discord.message import Message
from discord.channel import TextChannel
from discord.embeds import Embed
from discord.colour import Colour
from discord.guild import Member, Guild
from discord.errors import Forbidden

from cfg import default_embeds_colour, prefix, DEFAULT_PORT, DEFAULT_LANG
from messages_cfg import *
from Logger import Logger

class MessageSender():
    @classmethod
    def __getDiscordNowTime(cls):
        return f"<t:{int(mktime(datetime.now().timetuple()))}>"

    @classmethod
    async def sendEmbed(cls, channel: TextChannel, fields: List[List[str]], lang: str=DEFAULT_LANG, thumbnail_url="", colour: Colour=default_embeds_colour, guild_thumbnail: bool=False, guild_footer=True, delete_after=-1, author: Member=None):
        embed_ = Embed(colour=colour)
        if len(fields) != 2:
            raise ValueError(f"fields argument have to have len of 2. Len of fields is {len(fields)}")
        if type(fields[0]) != list or type(fields[1]) != list:
            raise ValueError(f"fields argument have to be list of lists. Got [{type(fields[0])}, {type(fields[1])}]")
        if len(fields[0]) != len(fields[1]):
            raise ValueError(f"'fields's inner lists must be same size. Sizes are {len(fields[0])} and {len(fields[1])}")

        for i in range(len(fields[0])):
            embed_.add_field(name=str(fields[0][i]), value=str(fields[1][i]), inline=False)

        try:
            guild_icon_url = channel.guild.icon_url
        except AttributeError:
            guild_icon_url = None

        if guild_thumbnail and guild_icon_url:
            embed_.set_thumbnail(url=guild_icon_url)
        if thumbnail_url != "":
            embed_.set_thumbnail(url=thumbnail_url)

        if guild_footer and guild_icon_url:
            embed_.set_footer(text=footer_text[lang], icon_url=guild_icon_url)

        if author:
            embed_.set_author(name=str(author.name)+'#'+str(author.discriminator), icon_url=author.avatar_url)

        try:
            if delete_after > 0:
                return await channel.send(embed=embed_, delete_after=delete_after)
            else:
                return await channel.send(embed=embed_)
        except Forbidden as e:
            Logger.printLog("Cant send message. Forbidden. Check logs", error=True)
            Logger.writeApiFatalLog(f"Forbidden. Guild: name:{channel.guild} id:{channel.guild.id}. Channel: name:{channel.name} id: {channel.id}")

    @classmethod 
    def __formPlayerListStr(cls, player_list: List[str], lang: str, connection=True) -> str:
        player_list_str = ""
        if connection:
            for player in player_list:
                player_list_str += f"`{cls.clearFromFormattingChars(player)}`\n"
            player_list_str = player_list_str[:900]
            if len(player_list) == 0:
                player_list_str = online_list_msg["server_empty"][lang] + "\n"
        else:
            player_list_str = online_list_msg["server_offline"][lang] + "\n"
        player_list_str += "\n" + online_list_msg["last_update"][lang].format(cls.__getDiscordNowTime())
        return player_list_str

    @classmethod
    async def sendOnlineMsg(cls, channel: TextChannel, player_list: List[str], lang: str, connection=True):
        return await cls.sendEmbed(
            channel, 
            [[online_list_msg["online_players"][lang]],
            [cls.__formPlayerListStr(player_list, lang, connection)]],
            lang
        )

    @classmethod
    async def editOnlineMsg(cls, message: Message, player_list: List[str], lang: str, connection=True):
        if len(message.embeds) == 0:
            Logger.printLog(f"Message with id {message.id} was edited but it has 0 embeds to edit")
            return
        embed_: Embed = message.embeds[0]
        embed_.clear_fields()
        embed_.add_field(name=online_list_msg["online_players"][lang], value=cls.__formPlayerListStr(player_list, lang, connection))
        await message.edit(embed=embed_)

    @classmethod
    async def sendGuildInited(cls, channel: TextChannel, lang: str):
        await cls.sendEmbed(
            channel,
            [info_msgs["guild_inited"]["name"][lang],
            info_msgs["guild_inited"]["value"][lang]],
            lang,
            guild_thumbnail=True
        )

    @classmethod
    async def sendGuildAlreadyInited(cls, channel: TextChannel, lang: str):
        await cls.sendEmbed(
            channel,
            [[info_msgs["guild_alr_inited"]["name"][lang]],
            [info_msgs["guild_alr_inited"]["value"][lang]]],
            lang,
        )

    @classmethod
    async def sendInvalidSyntax(cls, channel: TextChannel, error_type: str, lang: str):
        await cls.sendEmbed(
            channel,
            [[info_msgs["invalid_syntax"][lang]],
            [info_msgs["invalid_syntax_comments"][error_type][lang]]],
            lang,
            colour=Colour.red()
        )

    @classmethod
    async def sendParameterSet(cls, channel: TextChannel, parameter_name: str, parameter_val: str, lang: str):
        await cls.sendEmbed(
            channel,
            [[info_msgs["success"][lang]],
            [info_msgs["parameter_set"][lang].format(name=info_msgs["parameters"][parameter_name][lang], val=parameter_val)]],
            lang,
        )

    @classmethod
    async def sendNotSetUp(cls, channel: TextChannel, lang: str):
        await cls.sendEmbed(
            channel,
            [[info_msgs["guild_not_set_up"]["name"][lang]],
            [info_msgs["guild_not_set_up"]["value"][lang]]],
            lang,
            colour=Colour.red()
        )

    @classmethod
    async def sendNotLinked(cls, channel: TextChannel, lang: str):
        await cls.sendEmbed(
            channel,
            [[info_msgs["guild_not_linked"]["name"][lang]],
            [info_msgs["guild_not_linked"]["value"][lang]]],
            lang,
            colour=Colour.red()
        )

    @classmethod
    async def sendMessageMissing(cls, channel: TextChannel, lang: str):
        await cls.sendEmbed(
            channel,
            [[info_msgs["message_missing"]["name"][lang]],
            [info_msgs["message_missing"]["value"][lang]]],
            lang,
            colour=Colour.red()
        )
        
    @classmethod
    async def sendMessageDeleted(cls, channel: TextChannel, lang: str):
        await cls.sendEmbed(
            channel,
            [[info_msgs["message_deleted"][lang]],
            [f"-"]],
            lang,
        )

    @classmethod
    async def sendCantConnect(cls, channel: TextChannel, lang: str):
        await cls.sendEmbed(
            channel,
            [[info_msgs["cant_connect"]["name"][lang]],
            [info_msgs["cant_connect"]["value"][lang]]],
            lang,
            colour=Colour.red()
        )

    @classmethod
    async def sendCfg(cls, channel: TextChannel, cfg_data: dict, lang: str):
        titels = []
        values = []
        titels.append(cfg_msg["mgr_field_name"][lang])
        values.append(cfg_msg["missing_value"][lang] if cfg_data["mgr_role"] == -1 else f"> <@&{cfg_data['mgr_role']}>")
        titels.append(cfg_msg["channel_field_name"][lang])
        values.append(cfg_msg["missing_value"][lang] if cfg_data["channel"] == -1 else f"> <#{cfg_data['channel']}>")
        titels.append(cfg_msg["msg_field_name"][lang])
        values.append(cfg_msg["missing_value"][lang] if cfg_data["message"] == -1 else cfg_msg["present_value"][lang])
        titels.append(cfg_msg["ip_field_name"][lang])
        values.append(cfg_msg["missing_value"][lang] if cfg_data["server_ip"] == "" else f"> {cfg_data['server_ip']}")
        await cls.sendEmbed(
            channel,
            [titels, values],
            lang,
        )

    @classmethod
    async def sendLangSwitched(cls, channel: TextChannel, lang: str):
        await cls.sendEmbed(
            channel,
            [[lang_switched_msg[lang]],
            [f"-"]],
            lang,
            colour=Colour.green()
        )

    @classmethod
    async def sendUnknownCommand(cls, channel: TextChannel, lang: str):
        await cls.sendEmbed(
            channel,
            [[info_msgs["unknown_command"]["name"][lang]],
            [info_msgs["unknown_command"]["value"][lang]]],
            lang,
            colour=Colour.red()
        )

    @classmethod
    async def sendNotPermitted(cls, channel: TextChannel, lang: str):
        await cls.sendEmbed(
            channel,
            [[info_msgs["not_permitted"][lang]],
            [f"-"]],
            lang,
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