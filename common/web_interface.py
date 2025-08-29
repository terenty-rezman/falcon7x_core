from quart import Quart, request
from quart_schema import QuartSchema, validate_request, validate_response

from dataclasses import dataclass


import common.sane_tasks as sane_tasks
import common.util as util
import common.scenario as scenario
from common.xp_aircraft_state import ACState
from mfi import mfi
from aircraft_systems.synoptic_screen import SynopticScreen
from aircraft_systems.misc import FlightRegime
from common.instrument_panel import light_all_lamps


quart_task = None
app = Quart(__name__)

# fix bug KeyError: 'QUART_SCHEMA_CONVERT_CASING'
app.config["QUART_SCHEMA_CONVERT_CASING"] = None
app.config["QUART_SCHEMA_CONVERSION_PREFERENCE"] = None


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
async def synoptic_click():
    data = await request.get_data(as_text=True)
    page_name = data.partition("=")[2]

    if await SynopticScreen.set_active_page(page_name) == False:
        return {"result": "error", "string": "wrong synoptic page name"}

    return {"result": "ok"}


@dataclass
class RunProcedure:
    procedure_type: str | None
    procedure_path: str | None
    procedure_name: str | None


block_scenario_run = False

@app.post("/api/run_procedure")
@validate_request(RunProcedure)
async def run_procedure(data: RunProcedure):
    global block_scenario_run

    data.procedure_path = None if data.procedure_path == 'null' else data.procedure_path

    if not block_scenario_run:
        block_scenario_run = True
        await scenario.Scenario.run_scenario_task((data.procedure_type, data.procedure_path, data.procedure_name), ACState)
    block_scenario_run = False

    return {"result": "ok"}


@app.post("/api/stop_procedure")
async def stop_procedure():
    await scenario.Scenario.kill_current_scenario()

    return {"result": "ok"}


@app.get("/api/status")
async def status():
    status = {}

    procedure_name = scenario.Scenario.current_scenario_name
    if procedure_name:
        _type, path, name = procedure_name
        status.update({
            "current_procedure": {
                "procedure_type": _type,
                "procedure_path": path,
                "procedure_name": name 
            }
        })
    else:
        status.update({"current_procedure": None})
    
    # flight regime
    status.update({
        "flight_regime": FlightRegime.regime
    })

    return status


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


@app.post("/api/light_all_lamps")
async def light_lamps():
    sane_tasks.spawn(light_all_lamps(2))
    return {"result": "ok"}


async def run_server_task(listen_host, listen_port):
    global quart_task

    quart_task = app.run_task(host=listen_host, port=listen_port)
    quart_task = sane_tasks.spawn(quart_task)
