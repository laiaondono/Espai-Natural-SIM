from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from agentBoscBolets import AgentBoscBolets
from agentPersona import AgentPersona
from agentCurador import AgentCurador


def get_antidot_agent_curador(model):
    curador = None
    for a in model.schedule.agents:
        if isinstance(a, AgentCurador):
            curador = a
    return curador.antidot


class Model(Model):
    """A model with some number of agents."""

    def __init__(self, width, height,
                 num_agents_persona, num_agents_boscbolets_no_verinosos, num_agents_boscbolets_verinosos,
                 vida_persona, antidot_curador, quantitat_bolets_al_bosc):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        id = 0
        # Agent curador
        a = AgentCurador(id, self, antidot_curador)
        id += 1
        self.schedule.add(a)
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        self.grid.place_agent(a, (x, y))

        # Agents persona
        for i in range(num_agents_persona):
            a = AgentPersona(id, self, vida_persona)
            id += 1
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        # Agents boscos bolets
        nbsocos_total = num_agents_boscbolets_no_verinosos + num_agents_boscbolets_verinosos
        for i in range(nbsocos_total):
            if i < num_agents_boscbolets_verinosos:
                verinos = True
            else:
                verinos = False
            a = AgentBoscBolets(id, self, verinos, quantitat_bolets_al_bosc)
            id += 1
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            pos = [x, y]
            while self.posicio_ocupada(pos):
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                pos = [x, y]
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(
            model_reporters={"Antidot": get_antidot_agent_curador},
            agent_reporters={"Antidot": "unique_id"})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    def posicio_ocupada(self, pos):
        cellmates = self.grid.get_cell_list_contents([(pos[0], pos[1])])
        for mate in cellmates:
            if isinstance(mate, AgentBoscBolets):
                return True
        return False
