from Entity.Player import *
from SteeringBehaviour.Seek import seek


# evader is a Player entity object; agent is a zombie entity
def pursuit(evader, agent):
    to_evader = pg.Vector2()
    to_evader = evader.pos - agent.pos
    relative_face = dot(agent.face_target, evader.face_target)
    if (dot(to_evader, evader.face_target) > 0) and (relative_face < -0.95):
        return seek(agent, evader.pos)
    else:
        look_ahead_time = distance(agent.pos, evader.pos) / (agent.speed + evader.speed)
        return seek(agent, evader.pos + [c * look_ahead_time for c in evader.vel])
