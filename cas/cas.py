import asyncio
import httpx

from cas.messages import *


CAS_HOST = "127.0.0.1",

# 2 instances of CAS for left & right pilots
CAS_PORT_LEFT = 8881
CAS_PORT_RIGHT = 8882

client = httpx.AsyncClient(timeout=0.5)


async def make_post_to_cas(path, json: dict, cas_host: str, cas_port: int):
    try:
        cas_url = f"http://{cas_host}:{cas_port}"
        await client.post(cas_url + path, json=json)
    except httpx.HTTPError as e:
        print("CAS Exception:", type(e).__name__, "–", e) 


async def post_to_all_cas(path: str, json: dict):
    await make_post_to_cas(path, json, CAS_HOST, CAS_PORT_LEFT)
    await make_post_to_cas(path, json, CAS_HOST, CAS_PORT_RIGHT)
    # asyncio.create_task(make_post_to_cas(path, json, CAS_HOST, CAS_PORT_LEFT))
    # asyncio.create_task(make_post_to_cas(path, json, CAS_HOST, CAS_PORT_RIGHT))


async def show_message(cas_message: CASmssg):
    await post_to_all_cas("/api/show_message", {"message": str(cas_message)})
    print("show", cas_message)


async def show_message_alarm(cas_message: CASmssg):
    await post_to_all_cas("/api/show_message", {"message": str(cas_message)})
    print("show + alarm", cas_message)


async def remove_message(cas_message: CASmssg):
    await post_to_all_cas("/api/remove_message", {"message": str(cas_message)})
    print("remove", cas_message)


async def set_regime(cas_regime: Regimes):
    await post_to_all_cas("/api/set_regime", {"regime": str(cas_regime)})
    print(cas_regime)


async def remove_all_messages():
    await post_to_all_cas("/api/remove_all_messages", None)
