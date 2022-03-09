from os import listdir
from os.path import isfile, join
from json import load, dump

from discord.guild import Guild
from discord.role import Role
from discord.channel import TextChannel
from discord.message import Message

from cfg import DATA_FOLDER, DEFAULT_PORT
from Logger import Logger

class FileManager():
    @classmethod
    def __getFileList(cls):
        return [f for f in listdir(DATA_FOLDER) if isfile(join(DATA_FOLDER, f))]

    @classmethod
    def getGuildData(cls, guild: Guild):
        """Returns guild data. If file is not present returns False"""
        try:
            with open(f"{DATA_FOLDER}{guild.id}.json", 'r') as f:
                return load(f)
        except FileNotFoundError:
            return False

    @classmethod
    def getGuildDataById(cls, guild_id: int):
        """Returns guild data. If file is not present returns False"""
        try:
            with open(f"{DATA_FOLDER}{guild_id}.json", 'r') as f:
                return load(f)
        except FileNotFoundError:
            return False

    @classmethod
    def getRole(cls, guild: Guild):
        data = cls.getGuildData(guild)
        if data:
            return data["mgr_role"]
        else:
            return False

    @classmethod
    def createNewGuild(cls, guild: Guild):
        """Creates new guild file with default empty values"""
        cls.setGuildData(
            guild=guild,
            manager_role_id=-1,
            channel_id=-1,
            message_id=-1,
            server_ip="",
            port=DEFAULT_PORT
        )

    @classmethod
    def setGuildData(cls, guild: Guild, manager_role_id: int, channel_id: int, message_id: int, server_ip: str, port: str):
        """Saves dict {'mgr_role': manager_role.id, 'channel': channel.id, 'message': message.id} in file <id>.json"""
        with open(f"{DATA_FOLDER}{guild.id}.json", 'w') as f:
            dump({
                "mgr_role": manager_role_id,
                "channel": channel_id,
                "message": message_id,
                "server_ip": server_ip,
                "port": port
            }, f)

    @classmethod
    def setRole(cls, guild: Guild, new_manager_role: Role):
        """Sets manager role for guild. Returns False if file is not present"""
        data = cls.getGuildData(guild)
        if not data:
            return False
        cls.setGuildData(guild, new_manager_role.id, data["channel"], data["message"], data["server_ip"], data["port"])

    @classmethod
    def setChannel(cls, guild: Guild, new_channel: TextChannel):
        """Sets channel for guild. Returns False if file is not present"""
        data = cls.getGuildData(guild)
        if not data:
            return False
        cls.setGuildData(guild, data["mgr_role"], new_channel.id, data["message"], data["server_ip"], data["port"])

    @classmethod
    def setMessage(cls, guild: Guild, new_message: Message):
        """Sets channel for guild. Returns False if file is not present"""
        data = cls.getGuildData(guild)
        if not data:
            return False
        cls.setGuildData(guild, data["mgr_role"], data["channel"], new_message.id, data["server_ip"], data["port"])

    @classmethod
    def setServerIp(cls, guild: Guild, new_ip: str):
        """Sets channel for guild. Returns False if file is not present"""
        data = cls.getGuildData(guild)
        if not data:
            return False
        cls.setGuildData(guild, data["mgr_role"], data["channel"], data["message"], new_ip, data["port"])

    @classmethod
    def setPort(cls, guild: Guild, new_port: str):
        """Sets channel for guild. Returns False if file is not present"""
        data = cls.getGuildData(guild)
        if not data:
            return False
        cls.setGuildData(guild, data["mgr_role"], data["channel"], data["message"], data["server_ip"], new_port)

    @classmethod
    def resetChannel(cls, guild: Guild):
        """Sets channel for guild. Returns False if file is not present"""
        data = cls.getGuildData(guild)
        if not data:
            return False
        cls.setGuildData(guild, data["mgr_role"], -1, data["message"], data["server_ip"], data["port"])

    @classmethod
    def resetMessage(cls, guild: Guild):
        """Sets channel for guild. Returns False if file is not present"""
        data = cls.getGuildData(guild)
        if not data:
            return False
        cls.setGuildData(guild, data["mgr_role"], data["channel"], -1, data["server_ip"], data["port"])