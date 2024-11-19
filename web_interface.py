from collections import defaultdict

from quart import Quart, request
from quart_schema import QuartSchema, validate_request, validate_response

from dataclasses import dataclass


import sane_tasks
import util
import xplane as xp
import scenario
from xp_aircraft_state import ACState
from mfi import mfi
from aircraft_systems.synoptic_screen import SynopticScreen


quart_task = None
app = Quart(__name__)

# fix bug KeyError: 'QUART_SCHEMA_CONVERT_CASING'
app.config["QUART_SCHEMA_CONVERT_CASING"] = None
app.config["QUART_SCHEMA_CONVERSION_PREFERENCE"] = None


@app.route("/api")
async def json():
    return {"hello": "world"}


@app.route("/api/situation_list")
async def situation_list():
    return [
        {"situation_name": "Hа земле", "file_name": "1.sit"},
        {"situation_name": "В воздухе", "file_name": "2.sit"}
    ]


@dataclass
class LoadSit:
    file_name: str


@app.post("/api/load_situation")
@validate_request(LoadSit)
async def load_situation(data: LoadSit):
    await util.load_sit(f"Output/situations/{data.file_name}")
    return {"result": "ok"}


@app.post("/api/synoptic")
async def synoptic():
    data = await request.get_data(as_text=True)
    page_name = data.partition("=")[2]

    if SynopticScreen.set_active_page(page_name) == False:
        return {"result": "error", "string": "wrong synoptic page name"}

    return {"result": "ok"}


@dataclass
class RunProcedure:
    procedure_type: str
    procedure_path: str
    procedure_name: str


@app.post("/api/run_procedure")
@validate_request(RunProcedure)
async def run_procedure(data: RunProcedure):
    await scenario.Scenario.run_scenario_task((data.procedure_type, data.procedure_path, data.procedure_name), ACState)
    return {"result": "ok"}


@app.get("/api/procedure_list")
async def procedure_list():
    proc_list = []

    for _type, path, name in scenario.scenarios:
        proc_list.append({
            "procedure_type": _type,
            "procedure_path": path,
            "procedure_name": name 
        })

    return proc_list


@dataclass
class MfiMouseClick:
    x: int
    y: int
    w: int
    h: int
    window_name: str


@app.post("/api/mfi_mouse_click")
@validate_request(MfiMouseClick)
async def mfi_mouse_click(data: MfiMouseClick):
    print(data)
    mfi.mfi_click(data.window_name, data.x, data.y, data.w, data.h)
    return {"result": "ok"}


# @app.post("/api/mfi_mouse_click")
# async def mfi_mouse_click():
#     data = await request.json
#     print(data)
#     return {"result": "ok"}


async def run_server_task(listen_host, listen_port):
    global quart_task

    quart_task = app.run_task(host=listen_host, port=listen_port)
    quart_task = sane_tasks.spawn(quart_task)
