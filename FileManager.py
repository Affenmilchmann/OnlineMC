from os import listdir
from os.path import isfile, join
from json import load, dump
from json.decoder import JSONDecodeError
from typing import List

from discord.guild import Guild
from discord.role import Role
from discord.channel import TextChannel
from discord.message import Message

from cfg import DATA_FOLDER, DEFAULT_PORT
from Logger import Logger

class FileManager():
    @classmethod
    def __getFileList(cls) -> List[str]:
        return [f for f in listdir(DATA_FOLDER) if isfile(join(DATA_FOLDER, f))]

    @classmethod
    def getGuildsIds(cls) -> List[int]:
        rtrn = []
        for file in cls.__getFileList():
            try:
                rtrn.append(int(file.replace(".json", "")))
            except ValueError:
                Logger.printLog(f"{file} had invalid name. Its ignored in statistics")
        return rtrn

    @classmethod
    def getGuildData(cls, guild: Guild):
        """Returns guild data. If file is not present returns False"""
        return cls.getGuildDataById(guild_id=guild.id)

    @classmethod
    def getGuildDataById(cls, guild_id: int):
        """Returns guild data. If file is not present returns False"""
        try:
            with open(f"{DATA_FOLDER}{guild_id}.json", 'r') as f:
                data = load(f)
            if not "total_refreshes" in data:
                data["total_refreshes"] = 0
                with open(f"{DATA_FOLDER}{guild_id}.json", 'w') as f:
                    dump(data, f)
            return data
        except FileNotFoundError:
            return False
        except JSONDecodeError:
            cls.createNewGuildById(guild_id)
            Logger.printLog(f"Guild file with id {guild_id} had invalid json format. It was overwritten")
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
        cls.createNewGuildById(guild.id)

    @classmethod
    def createNewGuildById(cls, guild_id: int):
        """Creates new guild file with default empty values"""
        cls.__setGuildDataById(
            guild_id=guild_id,
            manager_role_id=-1,
            channel_id=-1,
            message_id=-1,
            server_ip="",
            port=DEFAULT_PORT,
            total_rfrsh=0
        )

    @classmethod
    def __setGuildData(cls, guild: Guild, manager_role_id: int, channel_id: int, message_id: int, server_ip: str, port: str, total_rfrsh: int):
        """Saves dict {'mgr_role': manager_role.id, 'channel': channel.id, 'message': message.id} in file <id>.json"""
        cls.__setGuildDataById(guild.id, manager_role_id, channel_id, message_id, server_ip, port, total_rfrsh)

    @classmethod
    def __setGuildDataById(cls, guild_id: int, manager_role_id: int, channel_id: int, message_id: int, server_ip: str, port: str, total_rfrsh: int):
        """Saves dict {'mgr_role': manager_role.id, 'channel': channel.id, 'message': message.id} in file <id>.json"""
        with open(f"{DATA_FOLDER}{guild_id}.json", 'w') as f:
            dump({
                "mgr_role": manager_role_id,
                "channel": channel_id,
                "message": message_id,
                "server_ip": server_ip,
                "port": port,
                "total_refreshes": total_rfrsh
            }, f)

    @classmethod
    def setRole(cls, guild: Guild, new_manager_role: Role):
        """Sets manager role for guild. Returns False if file is not present"""
        data = cls.getGuildData(guild)
        if not data:
            return False
        cls.__setGuildData(guild, new_manager_role.id, data["channel"], data["message"], data["server_ip"], data["port"], data["total_refreshes"])

    @classmethod
    def setChannel(cls, guild: Guild, new_channel: TextChannel):
        """Sets channel for guild. Returns False if file is not present"""
        data = cls.getGuildData(guild)
        if not data:
            return False
        cls.__setGuildData(guild, data["mgr_role"], new_channel.id, data["message"], data["server_ip"], data["port"], data["total_refreshes"])

    @classmethod
    def setMessage(cls, guild: Guild, new_message: Message):
        """Sets channel for guild. Returns False if file is not present"""
        data = cls.getGuildData(guild)
        if not data:
            return False
        cls.__setGuildData(guild, data["mgr_role"], data["channel"], new_message.id, data["server_ip"], data["port"], data["total_refreshes"])

    @classmethod
    def setServerIp(cls, guild: Guild, new_ip: str):
        """Sets channel for guild. Returns False if file is not present"""
        data = cls.getGuildData(guild)
        if not data:
            return False
        cls.__setGuildData(guild, data["mgr_role"], data["channel"], data["message"], new_ip, data["port"], data["total_refreshes"])

    @classmethod
    def setPort(cls, guild: Guild, new_port: str):
        """Sets channel for guild. Returns False if file is not present"""
        data = cls.getGuildData(guild)
        if not data:
            return False
        cls.__setGuildData(guild, data["mgr_role"], data["channel"], data["message"], data["server_ip"], new_port, data["total_refreshes"])

    @classmethod
    def setTotalRefreshes(cls, guild: Guild, total_refreshes: int = 0):
        """Sets channel for guild. Returns False if file is not present"""
        data = cls.getGuildData(guild)
        if not data:
            return False
        cls.__setGuildData(guild, data["mgr_role"], data["channel"], data["message"], data["server_ip"], data["port"], total_refreshes)

    @classmethod
    def setTotalRefreshesById(cls, guild_id: int, total_refreshes: int = 0):
        """Sets channel for guild. Returns False if file is not present"""
        data = cls.getGuildDataById(guild_id)
        if not data:
            return False
        cls.__setGuildDataById(guild_id, data["mgr_role"], data["channel"], data["message"], data["server_ip"], data["port"], total_refreshes)

    @classmethod
    def incTotalRefreshesById(cls, guild_id: int):
        """Sets channel for guild. Returns False if file is not present"""
        data = cls.getGuildDataById(guild_id)
        if not data:
            return False
        cls.__setGuildDataById(guild_id, data["mgr_role"], data["channel"], data["message"], data["server_ip"], data["port"], data["total_refreshes"] + 1)

    @classmethod
    def resetChannel(cls, guild: Guild):
        """Sets channel for guild. Returns False if file is not present"""
        data = cls.getGuildData(guild)
        if not data:
            return False
        cls.__setGuildData(guild, data["mgr_role"], -1, data["message"], data["server_ip"], data["port"], data["total_refreshes"])

    @classmethod
    def resetMessage(cls, guild: Guild):
        """Sets channel for guild. Returns False if file is not present"""
        data = cls.getGuildData(guild)
        if not data:
            return False
        cls.__setGuildData(guild, data["mgr_role"], data["channel"], -1, data["server_ip"], data["port"], data["total_refreshes"])