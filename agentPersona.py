from mesa import Agent
from agentBoscBolets import AgentBoscBolets


class AgentPersona(Agent):
    vida = 200
    bosc_bolets_verinosos = []
    enverinada = False

    def __init__(self, unique_id, model, vida):
        super().__init__(unique_id, model)
        self.vida = vida
        self.bosc_bolets_verinosos = []
        self.enverinada = False

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        bosc = self.hi_ha_bosc_adjacent(possible_steps)
        if (self.vida < 30 or self.enverinada) and bosc is not None:
            nova_posicio = bosc
        else:
            nova_posicio = self.random.choice(possible_steps)
            while nova_posicio in self.bosc_bolets_verinosos:
                nova_posicio = self.random.choice(possible_steps)

        self.model.grid.move_agent(self, nova_posicio)

    def step(self):
        if self.vida > 0:
            self.move()
            bolets = self.hi_ha_bolets()
            if bolets is not None:
                self.menjar_bolet(bolets)
                bolets.decrementar_quantitat()

        self.vida -= 1
        if self.vida < 0:
            self.vida = 0

    def hi_ha_bolets(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for mate in cellmates:
            if isinstance(mate, AgentBoscBolets) and not mate.es_bosc_mort():
                return mate
        return None

    def menjar_bolet(self, bolets):
        if bolets.es_bosc_verinos():
            self.vida -= 10
            self.enverinada = True
            self.bosc_bolets_verinosos.append(bolets.pos)
        else:
            if self.vida < 100:
                self.vida += 10
                if self.vida > 100:
                    self.vida = 100
            self.enverinada = False

    def hi_ha_bosc_adjacent(self, celes_adjacents):
        for cela in celes_adjacents:
            cellmates = self.model.grid.get_cell_list_contents([cela])
            for mate in cellmates:
                if isinstance(mate, AgentBoscBolets) and not mate.es_bosc_mort() and mate not in self.bosc_bolets_verinosos:
                    return cela
        return None

    def informar(self, boscos_no_verinosos):
        for i in range(len(self.bosc_bolets_verinosos)):
            if i < len(self.bosc_bolets_verinosos):
                if self.bosc_bolets_verinosos[i] in boscos_no_verinosos:
                    self.bosc_bolets_verinosos.pop(i)
                    i -= 1



