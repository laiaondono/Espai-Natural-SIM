from mesa.visualization.UserParam import UserSettableParameter

from model import *
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.7}

    if isinstance(agent, AgentPersona):
        if agent.enverinada:
            portrayal["Color"] = "purple"
            portrayal["Layer"] = 0
        else:
            portrayal["Color"] = "grey"
            portrayal["Layer"] = 0
        if agent.vida < 20:
            portrayal["r"] = 0.6
        if agent.vida == 0:
            portrayal["Color"] = "white"
            portrayal["r"] = 0.5

    elif isinstance(agent, AgentBoscBolets):
        portrayal["r"] = 0.5
        if not agent.es_verinos:
            portrayal["Color"] = "brown"
            portrayal["Layer"] = 1
        else:
            portrayal["Color"] = "red"
            portrayal["Layer"] = 1
        if agent.es_bosc_mort():
            portrayal["Color"] = "black"
            portrayal["Layer"] = 1

    elif isinstance(agent, AgentCurador):
        portrayal["r"] = 0.4
        if not agent.recarregar_antidot:
            portrayal["Color"] = "yellow"
            portrayal["Layer"] = 2
        else:
            portrayal["Color"] = "white"
            portrayal["Layer"] = 0
            portrayal["r"] = 0.5

    return portrayal


def get_antidot_agent_curador(model):
    curador = None
    for a in model.schedule.agents:
        if isinstance(a, AgentCurador):
            curador = a
    return curador.antidot


model_params = {
    "width": 15,
    "height": 15,
    "num_agents_persona": UserSettableParameter(
        "slider", "Personas", 150, 1, 200, description="Nombre inicial d'agents Persona"
    ),
    "num_agents_boscbolets_no_verinosos": UserSettableParameter(
        "slider", "Boscos de bolets no verinosos", 60, 0, 80,
        description="Nombre inicial d'agents BoscBolets no verinosos"
    ),
    "num_agents_boscbolets_verinosos": UserSettableParameter(
        "slider", "Boscos de bolets verinosos", 30, 0, 60, description="Nombre inicial d'agents BoscBolets verinosos"
    ),
    "vida_persona": UserSettableParameter(
        "slider", "Vida de les persones", 400, 50, 400, description="Vida inicial dels agents Persona"
    ),
    "antidot_curador": UserSettableParameter(
        "slider", "Quantitat d'antidot", 2000, 500, 3000, description="Quantitat inicial de l'antídot del curador"
    ),
    "quantitat_bolets_al_bosc": UserSettableParameter(
        "slider", "Bolets per bosc", 250, 100, 300, description="Quantitat de bolets a cada bosc"
    ),
}

grid = CanvasGrid(agent_portrayal, 15, 15, 700, 700)

chart = ChartModule([{"Label": "Antidot",
                      "Color": "Yellow"}],
                    data_collector_name='datacollector')

server = ModularServer(Model,
                       [grid, chart],
                       "Model Espai Natural",
                       model_params=model_params)

server.port = 8521  # The default
server.launch()
