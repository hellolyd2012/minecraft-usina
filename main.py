from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
import sys
from random import *
from os import *

word_big = 50
game_time = 0
SEED = randint(1,9999999999999999999999)


class Hand(Entity):
    def __init__(self):
        hand_texture = load_texture('assets/arm_texture.png')
        super().__init__(
            parent=camera.ui,     # 手的特殊设置, 表示显示方式
            model='assets/arm',   # 使用自己制作的模型
            texture=hand_texture,
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.6),
            double_sided=True  # 表示球体的两面都显示sky_texture
        )

    # 手动的时候，简单地移动， 实现动画效果
    def active(self):
        self.position = Vec2(0.3, -0.5)

    # 手不动的时候，回到初始位置
    def passive(self):
        self.position = Vec2(0.4, -0.6)

class sky(Entity):
    def __init__(self, texture_sky=None):
        super().__init__(
            model='sphere',
            texture=texture_sky,
            scale= randrange(200,300),
            double_sided=True
        )


app = Ursina()


window.fps_counter.enabled = False  # 隐藏屏幕右上角的帧数
window.exit_button.visible = False  # 沉浸式感觉

block_pick = 1



block_pick_global = 1
grass_texture = None
stone_texture = None
brick_texture = None
dirt_texture = None
punch_sound = None
# texture_block_pick = None


# 更新创建方式
def update_block_pick(block_pick):
    global block_pick_global
    block_pick_global = block_pick


# 加载对应的texture
def load_block_texture():
    global grass_texture, stone_texture, brick_texture, dirt_texture
    global punch_sound
    grass_texture = load_texture('assets/grass_block.png')
    stone_texture = load_texture('assets/stone_block.png')
    brick_texture = load_texture('assets/brick_block.png')
    dirt_texture = load_texture('assets/dirt_block.png')
    punch_sound = Audio('assets/punch_sound.wav', loop=False, autoplay=False)


# 默认创建草坪方块

scene.fog_color = color.white
scene.fog_density = 0.05
class Block(Button):
    def __init__(self, position=(0, 0, 0),texture_block=load_texture('assets/grass_block.png')):
        global grass_texture
        self.texture_block = grass_texture
        # self.texture_block = texture_block
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',             # 模型使用立方体
            origin_y=0.5,
            texture=texture_block,   # 显示内容
            color=color.color(0, 0, uniform(0.9, 1)),  # 利用RGB生成不同颜色的方块
            highlight_color=color.white,  # 触碰到立方体为白色
            scale=0.5
        )

    def input(self, key):
        global grass_texture, stone_texture, brick_texture, dirt_texture
        global block_pick_global
        if key == "escape":
            sys.exit()
        if self.hovered:
            # 右键，朝鼠标指向方向创建方块
            if key == 'right mouse down':
                punch_sound.play()
                # if held_keys['1']: block = Block(position=self.position + mouse.normal, texture_block=grass_texture)
                # if held_keys['2']: block = Block(position=self.position + mouse.normal, texture_block=stone_texture)
                # if held_keys['3']: block = Block(position=self.position + mouse.normal, texture_block=brick_texture)
                # if held_keys['4']: block = Block(position=self.position + mouse.normal, texture_block=dirt_texture)
                if block_pick_global == 1: block = Block(position=self.position + mouse.normal, texture_block=grass_texture)
                if block_pick_global == 2: block = Block(position=self.position + mouse.normal, texture_block=stone_texture)
                if block_pick_global == 3: block = Block(position=self.position + mouse.normal, texture_block=brick_texture)
                if block_pick_global == 4: block = Block(position=self.position + mouse.normal, texture_block=dirt_texture)

                # block = Block(position=self.position + mouse.normal, texture_block=self.texture_block)
            # 左键， 摧毁方块
            if key == 'left mouse down':
                punch_sound.play()
                destroy(self)
            #退出游戏
            if held_keys["Esc"]:
                sys.exit()
            if held_keys['F1']:
                sys.exit()



sky_texture = load_texture('assets/skybox.png')

# 将加载到的texture放在block文件
# 注意加载过程必须在app = Ursina()后面
load_block_texture()






# held_keys
# 该函数会被自动调用， ursina的机制
# 页面每次刷新，调用该函数
def update():
    # 生成方块类型选择
    global block_pick
    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4
    update_block_pick(block_pick)
    # 手的动画实现
    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()
   


noise = PerlinNoise(octaves= 2,seed = SEED)
scale = 24
# 生成指定数量和位置的模块
for z in range(word_big):
    for x in range(word_big):
        block = Block(position= (x,-1 ,z))
for z in range(word_big):
    for x in range(word_big):
        block = Block(position= (x,0,z))
        block.y = floor(noise([x/scale,z/scale])*8)
        

player = FirstPersonController()

hand = Hand()
sky = Sky(texture_sky=sky_texture)


app.run()
