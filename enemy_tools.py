import enemy
import utils

def get_enemy_size_from_type(enemy_type):
    return utils.get_enemy_size(enemy_type)
    

# Since the stage is what determines the enemy's type, let's isolate that into a simple function
def get_enemy_type_from_stage(stage):
    match stage:
        case 1:
            return 'enemy1'
        case 2:
            return 'enemy2'
        case 3:
            return 'boss3'
        case 4:
            return 'boss4'
        case 5:
            return 'boss5'
    

# Given the stage, returns the number of enemies to spawn
def get_enemies_for_stage(stage):
    enemies = []
    if stage in [1,2]:
        for _ in range(10):
            enemies.append(enemy.Enemy(get_enemy_type_from_stage(stage), stage >=3, stage))
    if stage > 2:
        for _ in range(1):
            enemies.append(enemy.Enemy(get_enemy_type_from_stage(stage), stage >=3, stage))
    return enemies

    