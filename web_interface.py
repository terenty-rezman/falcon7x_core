from collections import defaultdict

from quart import Quart, request
from quart_schema import QuartSchema, validate_request, validate_response

from dataclasses import dataclass


import sane_tasks
import util
import xplane as xp
import scenario
from xp_aircraft_state import ACState


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
    pages = {
        "STAT": 0,
        "ENG": 1,
        "ELEC": 2,
        "FUEL": 3,
        "HYD": 4,
        "ECS": 5, 
        "BLD": 6,
        "FCS": 7,
        "TEST": 8
    }
    data = await request.get_data(as_text=True)
    page_name = data.partition("=")[2]
    page = pages.get(page_name)
    if page is None:
        return {"result": "error", "string": "wrong synoptic page name"}

    await xp.set_param(xp.Params["sim/cockpit/weapons/firing_rate"], page)

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


async def run_server_task(listen_host, listen_port):
    global quart_task

    quart_task = app.run_task(host=listen_host, port=listen_port)
    quart_task = sane_tasks.spawn(quart_task)
