import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(supabase_url, supabase_key)


def db() -> Client:
    return supabase


def check_if_log_channel_exists(guild_id: int) -> bool:
    res = db().table("logger").select("channel_id").eq("guild_id", guild_id).execute()
    if not res.data:
        return False
    return True


def get_log_channel(guild_id: int) -> int:
    res = db().table("logger").select("channel_id").eq("guild_id", guild_id).execute()
    if not res.data:
        return False
    return res.data[0].get("channel_id")


def set_log_channel(guild_id: int, channel_id: int):
    res = (
        db()
        .table("logger")
        .insert({"guild_id": guild_id, "channel_id": channel_id})
        .execute()
    )
    return res.data


def remove_log_channel(guild_id: int):
    res = db().table("logger").delete().eq("guild_id", guild_id).execute()
    return res.data


def update_log_channel(guild_id: int, channel_id: int):
    res = (
        db()
        .table("logger")
        .update({"channel_id": channel_id})
        .eq("guild_id", guild_id)
        .execute()
    )
    return res.data
