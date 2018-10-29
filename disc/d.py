import requests
from . import config

auth = "Bot {}".format(config.token)
common_header = {"Authorization": auth}
base_url = "https://discordapp.com/api/"


def get_user(d_id: int):
    r = requests.get(base_url + "users/" + str(d_id), headers=common_header)
    return r.json()


def get_pfp_url(user_id: int):
    user = requests.get(
        base_url + "users/" + str(user_id), headers=common_header
    ).json()
    return "https://cdn.discordapp.com/avatars/{}/{}".format(user_id, user["avatar"])


def get_guild_member(guild_id: int, member_id: int):
    member = requests.get(
        base_url + "guilds/{}/members/{}".format(guild_id, member_id),
        headers=common_header,
    ).json()
    return member


def get_guild_roles(guild_id: int):
    return requests.get(
        base_url + "guilds/{}/roles".format(guild_id), headers=common_header
    ).json()


def get_guild_role(guild_id: int, role_id: int):
    roles = get_guild_roles(guild_id)
    for role in roles:
        if role["id"] == role_id:
            return role
