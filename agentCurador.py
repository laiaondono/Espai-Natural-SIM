from mesa import Agent

from agentBoscBolets import AgentBoscBolets
from agentPersona import AgentPersona


class AgentCurador(Agent):
    antidot = 0
    antidot_inicial = 0
    recarregar_antidot = False
    cnt_steps_recarregant = 0
    boscos_curats = []
    cnt_steps_buscant_boscos = 0

    def __init__(self, unique_id, model, antidot):
        super().__init__(unique_id, model)
        self.antidot = antidot
        self.antidot_inicial = antidot
        self.recarregar_antidot = False
        self.cnt_steps_recarregant = 0
        self.boscos_curats = []
        self.cnt_steps_buscant_boscos = 0

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        boscos = self.hi_ha_boscos_verinos_adjacents(possible_steps)
        if boscos is not None:
            bosc_a_curar = self.minteressa(boscos)
            if bosc_a_curar is not None:
                nova_posicio = bosc_a_curar.pos
            else:
                nova_posicio = self.random.choice(possible_steps)
                while nova_posicio in boscos:
                    nova_posicio = self.random.choice(possible_steps)
        else:
            nova_posicio = self.random.choice(possible_steps)
            bosc_a_curar = None

        self.model.grid.move_agent(self, nova_posicio)
        return bosc_a_curar

    def step(self):
        if not self.recarregar_antidot:
            bosc = self.move()
            if bosc is not None:
                self.curar_bosc(bosc)
                self.boscos_curats.append(bosc.pos)
                self.cnt_steps_buscant_boscos = 0
            else:
                self.cnt_steps_buscant_boscos += 1
            self.avisar_persones()

            if self.cnt_steps_buscant_boscos == 20:
                self.recarregar_antidot = True
                self.antidot = 0
                self.cnt_steps_recarregant = 0

        if self.antidot <= 0:
            self.recarregar_antidot = True
            self.boscos_curats = []

        if self.recarregar_antidot:
            self.cnt_steps_recarregant += 1
            if self.cnt_steps_recarregant >= 10:
                self.recarregar_antidot = False
                self.cnt_steps_recarregant = 0
                self.antidot = self.antidot_inicial

    def hi_ha_boscos_verinos_adjacents(self, celes_adjacents):
        boscos = []
        for cela in celes_adjacents:
            cellmates = self.model.grid.get_cell_list_contents([cela])
            for mate in cellmates:
                if isinstance(mate, AgentBoscBolets) and mate.es_bosc_verinos():
                    boscos.append(mate)
        boscos.sort()
        return boscos

    def minteressa(self, boscos):
        interes_mes_alt = -1
        bosc_mes_interessant = None

        for bosc in boscos:
            if bosc.quantitat <= 30 and self.antidot >= bosc.quantitat:
                if interes_mes_alt < 0:
                    interes_mes_alt = 0
                    bosc_mes_interessant = bosc
            elif 30 < bosc.quantitat <= 150:
                if self.antidot > 4 * bosc.quantitat:
                    if interes_mes_alt < 2:
                        interes_mes_alt = 2
                        bosc_mes_interessant = bosc
                elif self.antidot >= bosc.quantitat:
                    if interes_mes_alt < 1:
                        interes_mes_alt = 1
                        bosc_mes_interessant = bosc
            else:
                if self.antidot > 2 * bosc.quantitat:
                    if interes_mes_alt < 4:
                        interes_mes_alt = 4
                        bosc_mes_interessant = bosc
                elif self.antidot >= bosc.quantitat:
                    if interes_mes_alt < 3:
                        interes_mes_alt = 3
                        bosc_mes_interessant = bosc

        if interes_mes_alt == -1 and self.antidot <= 50:
            self.antidot = 0
            return None

        return bosc_mes_interessant

    def curar_bosc(self, bosc):
        bosc.curar()
        self.antidot -= bosc.quantitat

    def avisar_persones(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True)
        for cela in possible_steps:
            cellmates = self.model.grid.get_cell_list_contents([cela])
            for mate in cellmates:
                if isinstance(mate, AgentPersona):
                    mate.informar(self.boscos_curats)

    def get_antidot(self):
        return self.antidot















