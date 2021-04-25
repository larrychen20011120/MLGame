"""
The template of the script for the machine learning process in game pingpong
"""

class MLPlay:
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False
        self.side = side
        self.pre_block_x = 0
        self.destination_2p = 0

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] != "GAME_ALIVE":
            print(self.destination_2p)
            print(scene_info['ball'][0])
            print(scene_info['platform_2P'][0])
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            return "SERVE_TO_LEFT"
        else:
            speed = scene_info['ball_speed']
            ball = scene_info['ball']
            if scene_info['blocker'][0] - self.pre_block_x > 0:
                block_speed = 5
            else:
                block_speed = -5
            def hit_block_side():
                # for 1p : 往上打磚塊側邊
                if ball[1] > 250:
                    time = (250 - ball[1]) / speed[1]
                    ball_hit = speed[0] * time + ball[0]
                    block_hit = block_speed * time + scene_info['blocker'][0]
                    if ball_hit > 195:
                        velocity = [-speed[0], speed[1]]
                        ball_hit = 390 - ball_hit
                    elif ball_hit < 0:
                        velocity = [-speed[0], speed[1]]
                        ball_hit = -ball_hit
                    else:
                        velocity = [speed[0], speed[1]]
                    if block_hit > 170:
                        block_hit = 340 - block_hit
                    elif block_hit < 0:
                        block_hit = -block_hit

                    if block_hit < ball_hit < block_hit + 30:
                        if velocity[0] > 0:
                            # 向右碰撞左側
                            return [ball_hit, 250], [-velocity[0], velocity[1]]
                        else:
                            # 向左碰撞右側
                            return [ball_hit, 250], [-velocity[0], velocity[1]]
                    else:
                        return None
            def hit_block_bottom():
                # for 2p : 往下打磚塊側邊 or 往下打磚塊底部
                if ball[1] < 235:
                    time = (235 - ball[1]) / speed[1]
                    ball_hit = speed[0] * time + ball[0]
                    block_hit = block_speed * time + scene_info['blocker'][0]
                    if ball_hit > 195:
                        velocity = [-speed[0], speed[1]]
                        ball_hit = 390 - ball_hit
                    elif ball_hit < 0:
                        velocity = [-speed[0], speed[1]]
                        ball_hit = -ball_hit
                    else:
                        velocity = [speed[0], speed[1]]

                    if block_hit > 170:
                        block_hit = 340 - block_hit
                    elif block_hit < 0:
                        block_hit = -block_hit

                    if block_hit - 5 < ball_hit < block_hit + 30:
                        return [ball_hit, 240], [velocity[0], -velocity[1]]
                    else:
                        return None
            def reflect(point, velocity):
                m = velocity[1] / velocity[0]
                b = point[1] - m * point[0]
                des = (80 - b) / m
                while True:
                    if des > 195:
                        des = 390 - des
                    elif des < 0:
                        des = - des
                    else:
                        break
                return des

            if speed[1] < 0:
                # go up : 1.撞邊 2.僅撞牆
                if hit_block_side() is not None:
                    point, velocity = hit_block_side()
                    self.destination_2p = reflect(point, velocity)
                    if scene_info['platform_2P'][0] + 18 <= self.destination_2p <= scene_info['platform_2P'][0] + 22:
                        command = 'NONE'
                    elif scene_info['platform_2P'][0] + 18 > self.destination_2p:
                        command = 'MOVE_LEFT'
                    else:
                        command = 'MOVE_RIGHT'
                else:
                    self.destination_2p = reflect(ball, speed)
                    if scene_info['platform_2P'][0] + 18 <= self.destination_2p <= scene_info['platform_2P'][0] + 22:
                        command = 'NONE'
                    elif scene_info['platform_2P'][0] + 18 > self.destination_2p:
                        command = 'MOVE_LEFT'
                    else:
                        command = 'MOVE_RIGHT'

            else:
                # go down : 1.撞底 2.置中
                if hit_block_bottom() is not None:
                    point, velocity = hit_block_bottom()
                    self.destination_2p = reflect(point, velocity)
                    if scene_info['platform_2P'][0] + 18 <= self.destination_2p <= scene_info['platform_2P'][0] + 22:
                        command = 'NONE'
                    elif scene_info['platform_2P'][0] + 18 > self.destination_2p:
                        command = 'MOVE_LEFT'
                    else:
                        command = 'MOVE_RIGHT'
                else:
                    if scene_info['platform_2P'][0] + 20 > 100:
                        command = 'MOVE_LEFT'
                    elif scene_info['platform_2P'][0] + 20 < 100:
                        command = 'MOVE_RIGHT'
                    else:
                        command = 'NONE'


            self.pre_block_x = scene_info['blocker'][0]

        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
