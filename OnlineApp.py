from typing import Dict, List
from json import dumps

from discord import Client
from discord.message import Message
from discord.guild import Guild, Member
from discord.role import Role
from discord.channel import TextChannel
from discord.errors import Forbidden, DiscordException

from Logger import Logger
from MessageSender import MessageSender
from cfg import DEFAULT_LANG, prefix, refresh_emoji, owner_id, invite_link
from messages_cfg import help_links, command_descriptions
from Command import Command
from FileManager import FileManager, StatFileManager
from ApiManager import ApiManager

def needs_guild_file(func):
    async def wrapped_func(self=None, message: Message=None, guild_data=None):
        if not guild_data:
            await MessageSender.sendNotLinked(message.channel, DEFAULT_LANG)
            return
        await func(self, message, guild_data)
    return wrapped_func

def owner_command(func):
    async def wrapped_func(self=None, message: Message=None):
        if message.author.id != owner_id:
            return
        await func(self, message)
    return wrapped_func

class OnlineApp():
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.commands: Dict[str, Command] = {
            "start": Command("start", self.__startCommand, f"{prefix}start"),
            "create": Command("create", self.__createCommand, f"{prefix}create"),
            "delete": Command("delete", self.__deleteCommand, f"{prefix}delete"),
            "set_role": Command("set_role", self.__setRoleCommand, f"{prefix}set_role <@role>"),
            "set_ip": Command("set_ip", self.__setIpCommand, f"{prefix}set_ip <minecraft server ip>"),
            "cfg": Command("cfg", self.__cfgCommand, f"{prefix}cfg"),
            "help": Command("help", self.__helpCommand, f"{prefix}help"),
            "ru": Command("ru", self.__setLangRuCommand, f"{prefix}ru"),
            "en": Command("en", self.__setLangEnCommand, f"{prefix}en"),
        }
        self.owner_commands: Dict[str, Command] = {
            "data": Command("data", self.__dataOwnerCommand, "-"),
            "stat": Command("stat", self.__statOwnerCommand, "-"),
        }
        Logger.printLog("App inited")

    async def onMessage(self, message: Message) -> None:
        command = self.__retrieveCommandFromMessageStr(message.content)
        if not command:
            return

        if command in self.commands and type(message.channel) == TextChannel:
            Logger.writeApiLog(f"Guild {message.guild}({message.guild.id}) called '{message.content}'")
            guild_data = FileManager.getGuildData(message.guild.id)
            if self.__isPermitted(message):
                await self.commands[command].handler(message, guild_data)
            else:
                await MessageSender.sendNotPermitted(message.channel, guild_data["lang"])
        elif command in self.owner_commands:
            await self.owner_commands[command].handler(message)

    def __isPermitted(self, message: Message) -> bool:
        mgr_role_id = FileManager.getRole(message.guild.id)
        mgr_role: Role = message.guild.get_role(mgr_role_id)
        if not mgr_role:
            return True
        return mgr_role in message.author.roles

    async def onReactionAdd(self, payload) -> None:
        guild_data = FileManager.getGuildData(payload.guild_id)
        # ignoring reactions from not set up guilds or dms
        if not guild_data:
            return
        guild: Guild = payload.member.guild
        if guild_data["message"] == payload.message_id and not payload.member.bot:
            channel: TextChannel = guild.get_channel(guild_data["channel"])
            if not channel:
                Logger.printLog(f'Cant get channel from reaction!!! Channel id: {guild_data["channel"]} | Guild id: {guild.id} name: {guild.name}', True)
                return
            online_msg: Message = await channel.fetch_message(guild_data["message"])
            if not online_msg:
                Logger.printLog(f'Cant get message from reaction!!! Message id: {guild_data["message"]} | Guild id: {guild.id} name: {guild.name} | channel id: {channel.id}', True)
                return
            api_result = ApiManager.getOnlineList(guild_data["server_ip"], guild_data["port"])
            await MessageSender.editOnlineMsg(online_msg, api_result, guild_data["lang"], api_result != False)
            await online_msg.remove_reaction(refresh_emoji, payload.member)
            # recording statistics and logs
            StatFileManager.incCallStat(payload.guild_id)
            member: Member = await guild.fetch_member(payload.user_id)
            Logger.writeApiLog(f"{member.display_name} from {guild.name} refreshed the list | guild:{guild.id} member: {member.id}")

    def __retrieveCommandFromMessageStr(self, msg_str: str) -> str:
        """Returns whatever goes after prefix. If message does not start with prefix, returns False"""
        if not msg_str.startswith(prefix):
            return False
        tmp_list = msg_str.split(" ")
        return tmp_list[0].replace(prefix, "")

    def __retrieveArgFromMessageStr(self, msg_str: str) -> str:
        """Returns whatever goes after command"""
        return msg_str.split()[1:]
            
    async def __startCommand(self, message: Message, guild_data):
        if not guild_data:
            FileManager.createNewGuild(message.guild.id)
            await MessageSender.sendGuildInited(message.channel, DEFAULT_LANG)
            Logger.printLog(f"{message.guild.name} joined! Id: {message.guild.id}")
        else:
            await MessageSender.sendGuildAlreadyInited(message.channel, guild_data["lang"])

    @needs_guild_file
    async def __createCommand(self, message: Message, guild_data):
        if guild_data["server_ip"] == "":
            await MessageSender.sendNotSetUp(message.channel, guild_data["lang"])
            return
        api_result = ApiManager.getOnlineList(guild_data["server_ip"], guild_data["port"])
        if api_result == False:
            await MessageSender.sendCantConnect(message.channel, guild_data["lang"])
        else:
            online_msg: Message = await MessageSender.sendOnlineMsg(message.channel, api_result, guild_data["lang"])
            await online_msg.add_reaction(refresh_emoji)
            FileManager.setMessage(message.guild.id, online_msg)
            FileManager.setChannel(message.guild.id, message.channel)

    @needs_guild_file
    async def __deleteCommand(self, message: Message, guild_data):
        if guild_data["message"] == -1:
            await MessageSender.sendMessageMissing(message.channel, guild_data["lang"])
            return
        await message.guild.fetch_channels()
        try:
            channel: TextChannel = message.guild.get_channel(guild_data["channel"])
        except DiscordException:
            await MessageSender.sendMessageMissing(message.channel, guild_data["lang"])
            return
        if not channel:
            await MessageSender.sendMessageMissing(message.channel, guild_data["lang"])
            return
        try:
            online_msg: Message = await channel.fetch_message(guild_data["message"])
        except DiscordException:
            await MessageSender.sendMessageMissing(message.channel, guild_data["lang"])
            return
        if not online_msg:
            await MessageSender.sendMessageMissing(message.channel, guild_data["lang"])
            return
        await online_msg.delete()
        FileManager.resetChannel(message.guild.id)
        FileManager.resetMessage(message.guild.id)
        await MessageSender.sendMessageDeleted(message.channel, guild_data["lang"])

    @needs_guild_file
    async def __setRoleCommand(self, message: Message, guild_data):
        raw_role_id = self.__retrieveArgFromMessageStr(message.content)
        if len(raw_role_id) == 0:
            await MessageSender.sendInvalidSyntax(message.channel, "role_arg_missing", guild_data["lang"])
            return
        try:
            role_id: int = int(''.join([i for i in raw_role_id[0] if i.isdigit()]))
        except ValueError:
            await MessageSender.sendInvalidSyntax(message.channel, "invalid_role", guild_data["lang"])
            return
        role: Role = message.guild.get_role(role_id)
        if role:
            FileManager.setRole(message.guild.id, role)
            await MessageSender.sendParameterSet(message.channel, "manager_role", role.mention, guild_data["lang"])
        else:
            await MessageSender.sendInvalidSyntax(message.channel, "invalid_role", guild_data["lang"])

    @needs_guild_file
    async def __setIpCommand(self, message: Message, guild_data):
        ip_str = self.__retrieveArgFromMessageStr(message.content)
        if len(ip_str) == 0:
            await MessageSender.sendInvalidSyntax(message.channel, "ip_arg_missing", guild_data["lang"])
            return
        FileManager.setServerIp(message.guild.id, ip_str[0])
        await MessageSender.sendParameterSet(message.channel, "ip", ip_str[0], guild_data["lang"])

    @needs_guild_file
    async def __cfgCommand(self, message: Message, guild_data):
        await MessageSender.sendCfg(message.channel, guild_data, guild_data["lang"])

    async def __helpCommand(self, message: Message, guild_data):
        if not guild_data:
            lang = DEFAULT_LANG
        else:
            lang = guild_data["lang"]
        await MessageSender.sendEmbed(
            message.channel,
            [[f"**`{cmd.syntax}`**" for _, cmd in self.commands.items()] + 
            help_links[lang],
            [f"*{command_descriptions[cmd.command][lang]}*" for _, cmd in self.commands.items()] + 
            ["https://www.curseforge.com/minecraft/bukkit-plugins/onlinemc", invite_link]], 
            lang
        )

    @needs_guild_file
    async def __setLangRuCommand(self, message: Message, guild_data):
        FileManager.setLangRu(message.guild.id)
        guild_data = FileManager.getGuildData(message.guild.id)
        await MessageSender.sendLangSwitched(message.channel, guild_data["lang"])

    @needs_guild_file
    async def __setLangEnCommand(self, message: Message, guild_data):
        FileManager.setLangEn(message.guild.id)
        guild_data = FileManager.getGuildData(message.guild.id)
        await MessageSender.sendLangSwitched(message.channel, guild_data["lang"])
    
    @owner_command
    async def __dataOwnerCommand(self, message: Message):
        guild_ids = FileManager.getGuildsIds()
        guilds_data: List = []
        guild_names: List[str] = []
        for id_ in guild_ids:
            try:
                guild: Guild = await self.client.fetch_guild(guild_id=id_)
                if not guild:
                    guild_names.append(f"Name: *`Cant fetch guild`* Id: `{id_}`")
                else:
                    guild_names.append(f"Name: `{guild.name}` Id: `{id_}`")
            except Forbidden:
                guild_names.append(f"Name: *`Guild is forbidden`* Id: `{id_}`")

            guilds_data.append(f"```{dumps(FileManager.getGuildData(id_), indent=4)}```")

        await MessageSender.sendEmbed(
            message.channel,
            [guild_names, guilds_data],
            guild_footer=False
        )

    @owner_command
    async def __statOwnerCommand(self, message: Message):
        guild_ids = StatFileManager.getGuildsIds()
        guilds_data: List = []
        guild_names: List[str] = []
        for id_ in guild_ids:
            try:
                guild: Guild = await self.client.fetch_guild(guild_id=id_)
                if not guild:
                    guild_names.append(f"Name: *`Cant fetch guild`* Id: `{id_}`")
                else:
                    guild_names.append(f"Name: `{guild.name}` Id: `{id_}`")
            except Forbidden:
                guild_names.append(f"Name: *`Guild is forbidden`* Id: `{id_}`")

            guilds_data.append(f"```{dumps(StatFileManager.getStats(id_), indent=4)}```")

        await MessageSender.sendEmbed(
            message.channel,
            [guild_names, guilds_data],
            guild_footer=False
        )