from mesa import Agent


class AgentBoscBolets(Agent):
    quantitat = 250
    quantitat_inicial = 250
    es_verinos = False
    tornant_a_creixer = False
    steps_desde_mort = 0

    def __init__(self, unique_id, model, es_verinos, quantitat):
        super().__init__(unique_id, model)
        self.quantitat = quantitat
        self.quantitat_inicial = quantitat
        self.es_verinos = es_verinos
        self.tornant_a_creixer = False
        self.steps_desde_mort = 0

    def __lt__(self, other):
        return self.quantitat > other.quantitat

    def step(self):
        if self.tornant_a_creixer and self.steps_desde_mort >= 10:
            self.quantitat += 10
            if self.quantitat == self.quantitat_inicial:
                self.tornant_a_creixer = False
                self.steps_desde_mort = 0

        if self.es_bosc_mort():
            self.steps_desde_mort += 1
            self.es_verinos = True

    def decrementar_quantitat(self):
        self.quantitat -= 10
        if self.quantitat == 0:
            self.tornant_a_creixer = True

    def es_bosc_mort(self):
        return self.quantitat == 0

    def es_bosc_verinos(self):
        return self.es_verinos

    def curar(self):
        self.es_verinos = False


