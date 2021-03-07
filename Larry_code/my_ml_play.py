"""
The template of the main script of the machine learning process
"""
# initialize hi_bricks = 0
hi_bricks = 0
point_a = [-1, -1]
point_b = [-1, -1]
destination = None

# when ball hit the platform clear the data
def clear_data():
    global point_a, point_b, destination
    point_a = [-1, -1]
    point_b = [-1, -1]
    destination = None

# predict the destination
def predict_des():
    global point_a, point_b
    if point_a[1] > hi_bricks and point_a[1] < point_b[1]:
        m = (point_b[1] - point_a[1]) / (point_b[0] - point_a[0])
        b = point_a[1] - m * point_a[0]
        return (400 - b) / m
    else:
        return None

# reflect
def reflect_adjust(des):
    if des is None:
        return None
    while des < 0 or des > 200:
        if des < 0:
            des = -des
        else:
            des = 400 - des

    return des

def mistake_adjust(des):
    des_new = predict_des()
    des_new = reflect_adjust(des_new)
    return (des + des_new) / 2

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
            command = "SERVE_TO_LEFT"

        # Your code here!
        else:
            global hi_bricks, destination
            global point_a, point_b

            # find the hi_bricks and never change it
            for i in range(len(scene_info["bricks"])):
                if scene_info['bricks'][i][1] > hi_bricks:
                    hi_bricks = scene_info["bricks"][i][1]

            if destination is None:
                command = 'NONE'
                if point_a[0] < 0:
                    point_a[0] = scene_info['ball'][0]
                    point_a[1] = scene_info['ball'][1]

                # predict the destination
                elif point_b[0] < 0:
                    point_b[0] = scene_info['ball'][0]
                    point_b[1] = scene_info['ball'][1]
                    destination = predict_des()
                    # adjust the destination until it is in the correct range
                    destination = reflect_adjust(destination)

                else:
                    # point_a and point_b exist && destination doesn't exist
                    # clear point_a and point_b
                    point_a = [-1, -1]
                    point_b = [-1, -1]

            # destination has already been
            else:
                # generate the command according to the destination
                if scene_info['platform'][0] >= destination - 15 and scene_info['platform'][0] <= destination - 5:
                    command = 'NONE'
                elif scene_info['platform'][0] > destination - 5:
                    command = 'MOVE_LEFT'
                else:
                    command = 'MOVE_RIGHT'

                # mistake adjust
                point_a[0] = point_b[0]
                point_a[1] = point_b[1]
                point_b[0] = scene_info['ball'][0]
                point_b[1] = scene_info['ball'][1]
                destination = mistake_adjust(destination)

                # clear the data (hit the ball)
                if scene_info['ball'][1] >= 393:
                    clear_data()
        return command
    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
