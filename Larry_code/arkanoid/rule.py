"""
The template of the main script of the machine learning process
"""
point_a = [-1, -1]
point_b = [-1, -1]
destination = None

# when ball hit the platform clear the data
def clear_data():
    global point_a, point_b, destination
    point_a = [-1, -1]
    point_b = [-1, -1]
    destination = None

# reflect
def reflect_wall(m, b,):
    # if y = 395 then x is in [0, 195] => destination
    if (395 - b) / m > 0 and (395 - b) / m < 195:
        return None
    else:
        if m > 0:
            # x = 195
            p_b = [195, m * 195 + b]
            b = p_b[1] - (-m * p_b[0])
            return -m, b, p_b
        else:
            # x = 0
            p_b = [0, b]
            b = p_b[1] - (-m * p_b[0])
            return -m, b, p_b

def reflect_bricks_bottom(m, b, p_b):
    global bricks
    if m > 0:
        for i in range(len(bricks) - 1, 0, -1):
            if bricks[i][0] < p_b[0] and bricks[i][1] < p_b[1]:
                # y = brick + 10 = mx + b
                if ((bricks[i][1] + 10 - b) / m) > bricks[i][0] and ((bricks[i][1] + 10 - b) / m) < bricks[i][0] + 25:
                    p_b = [(bricks[i][1] + 10 - b) / m, bricks[i][1] + 10]
                    m = -m
                    b = p_b[1] - m * p_b[0]
                    return m, b, p_b
        return None
    else:
        for i in range(len(bricks) - 1, 0, -1):
            if bricks[i][0] > p_b[0] and bricks[i][1] < p_b[1]:
                # y = brick + 10 = mx + b
                if ((bricks[i][1] + 10 - b) / m) > bricks[i][0] and ((bricks[i][1] + 10 - b) / m) < bricks[i][0] + 25:
                    p_b = [(bricks[i][1] + 10 - b) / m, bricks[i][1] + 10]
                    m = -m
                    b = p_b[1] - m * p_b[0]
                    return m, b, p_b
        return None

def reflect_bricks_side(m, b, p_b):
    global bricks
    if m > 0:
        for i in range(len(bricks)):
            if bricks[i][0] > p_b[0] and bricks[i][1] > p_b[1]:
                if (m * bricks[i][0] + b) > bricks[i][1] and (m * bricks[i][0] + b) < bricks[i][1] + 10:
                    p_b = [bricks[i][0], m * bricks[i][0] + b]
                    m = -m
                    b = p_b[1] - m * p_b[0]
                    return m, b, p_b
        return None
    else:
        for i in range(len(bricks)):
            if bricks[i][0] < p_b[0] and bricks[i][1] > p_b[1]:
                if (m * (bricks[i][0] + 25) + b) > bricks[i][1] and (m * (bricks[i][0] + 25) + b) < bricks[i][1] + 10:
                    p_b = [bricks[i][0] + 25, m * (bricks[i][0] + 25) + b]
                    m = -m
                    b = p_b[1] - m * p_b[0]
                    return m, b, p_b
        return None

# predict the destination
def predict_des(p_a, p_b):
    # the ball is going upward and hit the brick's bottom (for level 4):
    if p_b[1] < p_a[1]:
        # y = mx + b
        m = (p_b[1] - p_a[1]) / (p_b[0] - p_a[0])
        b = p_a[1] - m * p_a[0]
        while True:
            if reflect_bricks_bottom(m, b, p_b) is None:
                return None
            else:
                m, b, p_b = reflect_bricks_bottom(m, b, p_b)
                # reflect by bricks and wall
                while True:
                    if reflect_bricks_side(m, b, p_b) is None:
                        if reflect_wall(m, b) is None:
                            break
                        else:
                            m, b, p_b = reflect_wall(m, b)
                    else:
                        m, b, p_b = reflect_bricks_side(m, b, p_b)
                return (395 - b) / m


    # the ball is going downward
    if p_b[1] > p_a[1]:
        # y = mx + b
        m = (p_b[1] - p_a[1]) / (p_b[0] - p_a[0])
        b = p_a[1] - m * p_a[0]

        # reflect by bricks and wall
        while True:
            if reflect_bricks_side(m, b, p_b) is None:
                if reflect_wall(m, b) is None:
                    break
                else:
                    m, b, p_b = reflect_wall(m, b)
            else:
                m, b, p_b = reflect_bricks_side(m, b, p_b)
        return (395 - b) / m
    else:
        return None



class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
            scene_info["status"] == "GAME_PASS"):
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            command = "SERVE_TO_RIGHT"

        # Your code here!
        else:
            global point_a, point_b, destination, bricks
            bricks = []
            # save bricks data:
            for i in range(len(scene_info['bricks'])):
                bricks.append([scene_info['bricks'][i][0], scene_info["bricks"][i][1]])

            if destination is None:
                command = 'NONE'
                if point_a[0] < 0:
                    point_a[0] = scene_info['ball'][0]
                    point_a[1] = scene_info['ball'][1]

                # predict the destination
                elif point_b[0] < 0:
                    point_b[0] = scene_info['ball'][0]
                    point_b[1] = scene_info['ball'][1]
                    destination = predict_des(point_a, point_b)

                else:
                    # point_a and point_b exist && destination doesn't exist
                    # clear point_a and point_b
                    point_a = [-1, -1]
                    point_b = [-1, -1]

            # destination has already been
            else:
                # generate the command according to the destination
                if scene_info['platform'][0] + 10 < destination:
                    command = 'MOVE_RIGHT'
                elif scene_info['platform'][0] + 30 > destination:
                    command = 'MOVE_LEFT'
                else:
                    command = 'NONE'

                point_a[0] = point_b[0]
                point_a[1] = point_b[1]
                point_b[0] = scene_info['ball'][0]
                point_b[1] = scene_info['ball'][1]
                destination = predict_des(point_a, point_b)

                # clear the data (hit the ball)
                if scene_info['ball'][1] >= 390:
                    clear_data()
        return command
    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
