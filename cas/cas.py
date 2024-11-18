import asyncio
import httpx

from cas.messages import *


CAS_HOST = "127.0.0.1",

# 2 instances of CAS for left & right pilots
CAS_PORT_LEFT = 8881
CAS_PORT_RIGHT = 8882


async def make_post_to_cas(path, json: dict, cas_host: str, cas_port: int):
    try:
        cas_url = f"http://{cas_host}:{cas_port}"
        async with httpx.AsyncClient() as client:
            await client.post(cas_url + path, json=json)
    except httpx.HTTPError as e:
        print("CAS Exception:", type(e).__name__, "–", e) 


def post_to_all_cas(path: str, json: dict):
    # dont wait for cas
    asyncio.create_task(
        make_post_to_cas(path, json, CAS_HOST, CAS_PORT_LEFT)
    )

    # dont wait for cas
    asyncio.create_task(
        make_post_to_cas(path, json, CAS_HOST, CAS_PORT_RIGHT)
    )


async def show_message(cas_message: CASmssg):
    post_to_all_cas("/show_message", {"message": str(cas_message)})
    print(cas_message)


async def show_message_alarm(cas_message: CASmssg):
    post_to_all_cas("/show_message", {"message": str(cas_message)})
    print(cas_message)


async def hide_message(cas_message: CASmssg):
    post_to_all_cas("/hide_message", {"message": str(cas_message)})
    print(cas_message)

