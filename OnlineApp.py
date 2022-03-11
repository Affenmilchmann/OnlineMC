from typing import Dict, List
from json import dumps

from discord import Client
from discord.message import Message
from discord.guild import Guild, Member
from discord.role import Role
from discord.channel import TextChannel
from discord.errors import Forbidden

from Logger import Logger
from MessageSender import MessageSender
from cfg import prefix, refresh_emoji, owner_id
from Command import Command
from FileManager import FileManager
from ApiManager import ApiManager

def needs_guild_file(func):
    async def wrapped_func(self=None, message: Message=None, guild_data=None):
        if not guild_data:
            await MessageSender.sendNotSetUp(message.channel)
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
            "start": Command("start", self.__startCommand, 
            "Start! Call this command to start using bot", f"{prefix}start"),
            "create": Command("create", self.__createCommand, 
            "Creates online list updateable message in the channel where this command was recieved. This may take up to 10 seconds!", f"{prefix}create"),
            "delete": Command("delete", self.__deleteCommand, 
            "Deletes current online list updateable message.", f"{prefix}delete"),
            "set_role": Command("set_role", self.__setRoleCommand, 
            "Sets role that is able to manage bot settings. If no role was set, everbody will be able to change bot settings!", f"{prefix}set_role <@role>"),
            "set_ip": Command("set_ip", self.__setIpCommand, 
            "Sets minecraft server ip. Bot will request player data from there", f"{prefix}set_ip <minecraft server ip>"),
            "cfg": Command("cfg", self.__cfgCommand, 
            "Shows current bot's settings", f"{prefix}cfg"),
            "help": Command("help", self.__helpCommand, 
            "Shows help message", f"{prefix}help"),
        }
        self.owner_commands: Dict[str, Command] = {
            "stat": Command("stat", self.__statOwnerCommand, 
            "-", "-"),
        }
        Logger.printLog("App inited")

    async def onMessage(self, message: Message) -> None:
        command = self.__retrieveCommandFromMessageStr(message.content)
        if not command:
            return

        if command in self.commands and type(message.channel) == TextChannel:
            if self.__isPermitted(message):
                guild_data = FileManager.getGuildData(message.guild)
                await self.commands[command].handler(message, guild_data)
            else:
                await MessageSender.sendNotPermitted(message.channel)
        elif command in self.owner_commands:
            await self.owner_commands[command].handler(message)

    def __isPermitted(self, message: Message) -> bool:
        mgr_role_id = FileManager.getRole(message.guild)
        mgr_role: Role = message.guild.get_role(mgr_role_id)
        if not mgr_role:
            return True
        return mgr_role in message.author.roles

    async def onReactionAdd(self, payload) -> None:
        guild_data = FileManager.getGuildDataById(payload.guild_id)
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
            await MessageSender.editOnlineMsg(online_msg, api_result, api_result != False)
            await online_msg.remove_reaction(refresh_emoji, payload.member)
            FileManager.incTotalRefreshesById(guild.id)

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
            FileManager.createNewGuild(message.guild)
            await MessageSender.sendGuildInited(message.channel)
            Logger.printLog(f"{message.guild.name} joined! Id: {message.guild.id}")
        else:
            await MessageSender.sendGuildAlreadyInited(message.channel)

    @needs_guild_file
    async def __createCommand(self, message: Message, guild_data):
        if guild_data["server_ip"] == "":
            await MessageSender.sendNotSetUp(message.channel)
            return
        api_result = ApiManager.getOnlineList(guild_data["server_ip"], guild_data["port"])
        if api_result == False:
            await MessageSender.sendCantConnect(message.channel)
        else:
            online_msg: Message = await MessageSender.sendOnlineMsg(message.channel, api_result)
            await online_msg.add_reaction(refresh_emoji)
            FileManager.setMessage(message.guild, online_msg)
            FileManager.setChannel(message.guild, message.channel)

    @needs_guild_file
    async def __deleteCommand(self, message: Message, guild_data):
        if guild_data["message"] == -1:
            await MessageSender.sendMessageMissing(message.channel)
            return
        await message.guild.fetch_channels()
        channel: TextChannel = message.guild.get_channel(guild_data["channel"])
        if not channel:
            await MessageSender.sendMessageMissing(message.channel)
            return
        online_msg: Message = await channel.fetch_message(guild_data["message"])
        if not online_msg:
            await MessageSender.sendMessageMissing(message.channel)
            return
        await online_msg.delete()
        FileManager.resetChannel(message.guild)
        FileManager.resetMessage(message.guild)
        await MessageSender.sendMessageDeleted(message.channel)

    @needs_guild_file
    async def __setRoleCommand(self, message: Message, guild_data):
        raw_role_id = self.__retrieveArgFromMessageStr(message.content)
        if len(raw_role_id) == 0:
            MessageSender.sendInvalidSyntax(message.channel, "Role argument is missing")
            return
        role_id: int = int(''.join([i for i in raw_role_id[0] if i.isdigit()]))
        role: Role = message.guild.get_role(role_id)
        if role:
            FileManager.setRole(message.guild, role)
            await MessageSender.sendParameterSet(message.channel, "Manager role", role.mention)
        else:
            MessageSender.sendInvalidSyntax(message.channel, "Invalid role")

    @needs_guild_file
    async def __setIpCommand(self, message: Message, guild_data):
        ip_str = self.__retrieveArgFromMessageStr(message.content)
        if len(ip_str) == 0:
            await MessageSender.sendInvalidSyntax(message.channel, "Ip argument is missing")
            return
        FileManager.setServerIp(message.guild, ip_str[0])
        await MessageSender.sendParameterSet(message.channel, "Ip", ip_str[0])

    @needs_guild_file
    async def __cfgCommand(self, message: Message, guild_data):
        await MessageSender.sendCfg(message.channel, guild_data)

    async def __helpCommand(self, message: Message, guild_data):
        await MessageSender.sendEmbed(
            message.channel,
            [[f"**`{cmd.syntax}`**" for _, cmd in self.commands.items()] + 
            ["**Get the plugin:**", "**Have a question? Found bug? Contact us here!**"],
            [f"*{cmd.description}*" for _, cmd in self.commands.items()] + 
            ["https://www.curseforge.com/minecraft/bukkit-plugins/onlinemc", "https://discord.gg/Y7cnUV58Rn"]],
        )
    
    @owner_command
    async def __statOwnerCommand(self, message: Message):
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

            guilds_data.append(f"```{dumps(FileManager.getGuildDataById(id_), indent=4)}```")

        await MessageSender.sendEmbed(
            message.channel,
            [guild_names, guilds_data],
            guild_footer=False
        )