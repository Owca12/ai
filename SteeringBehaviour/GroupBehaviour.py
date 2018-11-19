from SteeringBehaviour.SingleBehaviour import *


class GroupBehaviour:
    def __init__(self, agent):
        self.agent = agent
        pass

    def cohesion(self, agent_neighbours):
        center_of_mass = pg.math.Vector2()
        if len(agent_neighbours) > 0:
            for agentItr in agent_neighbours:
                center_of_mass = add(center_of_mass, agentItr.pos)
            return SingleBehaviour(self.agent).seek([coord / len(agent_neighbours) for coord in center_of_mass])

