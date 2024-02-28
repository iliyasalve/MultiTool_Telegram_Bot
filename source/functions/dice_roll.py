import random

def dice_roll(dice_number: int) -> int:
    '''
    Return the result of rolled dice
    '''

    result = 0

    for i in range(dice_number):
        dice_result = random.randint(1, 6)
        result += dice_result
    
    return result
