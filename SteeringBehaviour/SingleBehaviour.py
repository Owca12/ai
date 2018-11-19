from Entity.Player import *


class SingleBehaviour:
    def __init__(self, agent):
        self.agent = agent
        pass

    def seek(self, target_pos):
        return [c * self.agent.speed for c in normalize(sub(target_pos, self.agent.pos))]

    def pursuit(self, evader):
        to_evader = pg.Vector2()
        to_evader = evader.pos - self.agent.pos
        relative_face = dot(self.agent.face_target, evader.face_target)
        if (dot(to_evader, evader.face_target) > 0) and (relative_face < -0.95):
            return self.seek(evader.pos)
        else:
            look_ahead_time = distance(self.agent.pos, evader.pos) / (self.agent.speed + evader.speed)
            return self.seek(evader.pos + [c * look_ahead_time for c in evader.vel])
