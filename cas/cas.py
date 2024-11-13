import httpx

from cas.messages import *


CAS_HOST = "127.0.0.1",
CAS_PORT = 8881


async def make_post_to_cas(path, json: dict):
    try:
        cas_url = f"http://{CAS_HOST}:{CAS_PORT}"
        async with httpx.AsyncClient() as client:
            await client.post(cas_url + path, json=json)
    except httpx.HTTPError as e:
        print("CAS Exception:", type(e).__name__, "–", e) 


async def show_message(cas_message: CASmssg):
    await make_post_to_cas("/show_message", {"message": str(cas_message)})
    print(cas_message)


async def show_message_alarm(cas_message: CASmssg):
    await make_post_to_cas("/show_message", {"message": str(cas_message)})
    print(cas_message)


async def hide_message(cas_message: CASmssg):
    await make_post_to_cas("/hide_message", {"message": str(cas_message)})
    print(cas_message)

