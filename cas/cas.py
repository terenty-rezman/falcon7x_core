import asyncio
import httpx

from cas.messages import *


CAS_HOST = "127.0.0.1",

# 2 instances of CAS for left & right pilots
CAS_PORT = 8881

client = httpx.AsyncClient(timeout=0.5)


async def make_post_to_cas(path, json: dict, cas_host: str, cas_port: int):
    try:
        cas_url = f"http://{cas_host}:{cas_port}"
        await client.post(cas_url + path, json=json)
    except httpx.HTTPError as e:
        # print("CAS Exception:", type(e).__name__, "–", e) 
        pass


async def post_to_all_cas(path: str, json: dict):
    await make_post_to_cas(path, json, CAS_HOST, CAS_PORT)


async def show_message(cas_message: CASmssg):
    await post_to_all_cas("/api/cas/show_message", {"message": str(cas_message)})
    print("show", cas_message)


async def remove_message(cas_message: CASmssg):
    await post_to_all_cas("/api/cas/remove_message", {"message": str(cas_message)})
    print("remove", cas_message)


async def set_regime(cas_regime: Regimes):
    await post_to_all_cas("/api/cas/set_regime", {"regime": str(cas_regime)})
    print(cas_regime)


async def remove_all_messages():
    await post_to_all_cas("/api/cas/remove_all_messages", None)


async def read_messages():
    await post_to_all_cas("/api/cas/read_message", {})
