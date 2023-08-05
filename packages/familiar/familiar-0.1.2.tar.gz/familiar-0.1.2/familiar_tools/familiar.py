from familiar_tools.settings import api_settings


def dice_roll(number_of_dice, dice_sides, mod):
    import random
    total = 0
    for i in range(1, number_of_dice + 1):
        total += random.randint(1, dice_sides)
    return total + mod


def get_modifier(stat):
    mod = stat - 10
    mod = mod / 2
    return round(mod)


def get_game_version():
    return api_settings.VERSION
