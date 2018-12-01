from Entity.Player import *


def get_hiding_position(player_position, obstacle_position):
    distance_from_obstacle_position = 80
    obstacle_player_vector = normalize(sub(obstacle_position, player_position))
    obstacle_player_vector[0] = distance_from_obstacle_position * obstacle_player_vector[0]
    obstacle_player_vector[1] = distance_from_obstacle_position * obstacle_player_vector[1]

    return add(obstacle_position, obstacle_player_vector)


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

    def avoid_obstacle(self):
        move_vector = pg.Vector2(0, 0)
        for obstacle in self.agent.obstacles:
            distance_to_obstacle = distance(self.agent.pos, obstacle.pos)
            if distance_to_obstacle < (30 + obstacle.radius):
                speed = obstacle.radius / distance_to_obstacle
                move_vector = [c * speed * self.agent.speed for c in normalize(sub(self.agent.pos, obstacle.pos))]
                if distance_to_obstacle < obstacle.radius:
                    move_vector = [c * self.agent.speed for c in normalize(sub(self.agent.pos, obstacle.pos))]

        return move_vector

    def hide(self, player_position):
        move_vector = pg.math.Vector2()
        best_distance_to_obstacle = 1000
        best_hiding_spot = pg.math.Vector2()
        Found_Hideout = False
        for obstacle in self.agent.obstacles:
            if distance(self.agent.pos, player_position) < 400:
                # Calculating distance from position to agent and to playet to compare
                distance_to_obstacle = distance(self.agent.pos, obstacle.pos)
                player_distance_to_obstacle = distance(player_position, obstacle.pos)
                # Now going over every position and evaluating which is the closest and which isn't closer to the player
                if distance_to_obstacle < best_distance_to_obstacle:
                    if distance_to_obstacle < player_distance_to_obstacle:
                        best_distance_to_obstacle = distance_to_obstacle
                        best_hiding_spot = obstacle.pos
                        Found_Hideout = True

                else:
                    best_distance_to_obstacle = best_distance_to_obstacle

        if Found_Hideout:
            move_vector = [c * self.agent.speed for c in normalize(sub(get_hiding_position(
                player_position, best_hiding_spot), self.agent.pos
            ))]
            Found_Hideout = False

        return move_vector

