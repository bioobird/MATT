import spaceship

def get_enemy_size(enemy_type):
    match enemy_type:
        case 'enemy1': 
            return 25
        case 'enemy2':
            return 45
        case 'boss3':
            return spaceship.WIDTH * 4 // 2
        case 'boss4':
            return spaceship.WIDTH * 5 // 2
        case 'boss5':
            return spaceship.WIDTH * 6 // 4