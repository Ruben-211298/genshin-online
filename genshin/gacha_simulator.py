import sys
import random

def simulate_weapon_pull(tries, pity_wpn, fifty_wpn, epitomized, bargain_coins):
    """
    Simulate until one promotional WEAPON is obtained.
    Returns updated (tries, pity_wpn, fifty_wpn, epitomized, bargain_coins, success)
    """
    prob_nonpitty = 0.007
    prob_soft = 0.07
    soft_start = 66
    hard_pity = 80
    prob_4star = 0.1
    pity_4star_limit = 10

    gold = False
    pity_counter = pity_wpn
    pity_4star = 0
    got_promotional = False

    while not got_promotional and tries > 0:
        gold = False

        # --- Normal pulls before soft pity ---
        while pity_counter < soft_start and tries > 0 and not gold:
            tries -= 1
            pity_counter += 1
            if random.random() <= prob_nonpitty:
                gold = True
            else:
                if random.random() <= prob_4star or pity_4star == pity_4star_limit:
                    bargain_coins += 2.5
                    pity_4star = 0
                else:
                    pity_4star += 1

                while bargain_coins >= 5.0:
                    bargain_coins -= 5.0
                    tries += 1

        # --- Soft pity section ---
        i = 0
        while soft_start <= pity_counter < hard_pity and tries > 0 and not gold:
            tries -= 1
            pity_counter += 1
            i += 1
            if random.random() <= prob_nonpitty + prob_soft * i:
                gold = True
            else:
                if random.random() <= prob_4star or pity_4star == pity_4star_limit:
                    bargain_coins += 2.5
                    pity_4star = 0
                else:
                    pity_4star += 1

                while bargain_coins >= 5.0:
                    bargain_coins -= 5.0
                    tries += 1

        # --- Hard pity (guaranteed) ---
        if not gold and pity_counter >= hard_pity and tries > 0:
            tries -= 1
            pity_counter = 0
            gold = True

        # --- If we hit a gold, check epitomized + 75/25 split ---
        if gold:
            pity_counter = 0
            if fifty_wpn:  # not guaranteed
                if random.random() < 0.7 or epitomized == 1:
                    fifty_wpn = True
                    if random.random() < 0.5 or epitomized == 1:
                        got_promotional = True
                        epitomized = 0
                    else:
                        epitomized = 1
                else:
                    fifty_wpn = False
                    epitomized = 1
            else:
                fifty_wpn = True
                if random.random() < 0.5 or epitomized == 1:
                    got_promotional = True
                    epitomized = 0
                else:
                    epitomized = 1

    return tries, pity_counter, fifty_wpn, epitomized, bargain_coins, got_promotional

def simulate_character_pull(tries, pity_char, fifty_char, capture_value, bargain_coins):
    """
    Simulate until one promotional CHARACTER is obtained.
    Returns updated (tries, pity_char, fifty_char, capture_value, bargain_coins, success)
    """
    prob_nonpitty = 0.006
    prob_soft = 0.06
    soft_start = 76
    hard_pity = 90
    prob_4star = 0.1
    pity_4star_limit = 10

    pity_counter = pity_char
    pity_4star = 0
    got_promotional = False

    while not got_promotional and tries > 0:
        gold = False

        # --- Normal pulls before soft pity ---
        while pity_counter < soft_start and tries > 0 and not gold:
            tries -= 1
            pity_counter += 1
            if random.random() <= prob_nonpitty:
                gold = True
            else:
                if random.random() <= prob_4star or pity_4star == pity_4star_limit:
                    bargain_coins += 3.5
                    pity_4star = 0
                else:
                    pity_4star += 1

                # Convert coins into pulls
                while bargain_coins >= 5.0:
                    bargain_coins -= 5.0
                    tries += 1

        # --- Soft pity section ---
        i = 0
        while soft_start <= pity_counter < hard_pity and tries > 0 and not gold:
            tries -= 1
            pity_counter += 1
            i += 1
            if random.random() <= prob_nonpitty + prob_soft * i:
                gold = True
            else:
                if random.random() <= prob_4star or pity_4star == pity_4star_limit:
                    bargain_coins += 3.5
                    pity_4star = 0
                else:
                    pity_4star += 1

                while bargain_coins >= 5.0:
                    bargain_coins -= 5.0
                    tries += 1

        # --- Hard pity (guaranteed) ---
        if not gold and pity_counter >= hard_pity and tries > 0:
            tries -= 1
            pity_counter = 0
            gold = True

        # --- If we hit a gold, check 50/50 mechanics ---
        if gold:
            pity_counter = 0
            if fifty_char:  # means not guaranteed, do a coin flip
                luck_50 = random.random()

                # capture mechanic
                if capture_value in [0, 1]:
                    luck_value = -1.0
                elif capture_value == 2:
                    luck_value = 0.1
                elif capture_value == 3:
                    luck_value = 2.0

                if luck_50 < 0.5:
                    got_promotional = True
                    fifty_char = True
                else:
                    if random.random() <= luck_value:
                        got_promotional = True
                        fifty_char = True
                        capture_value = 0
                    else:
                        fifty_char = False  # next 50/50 again
                        capture_value += 1
                        got_promotional = False
            else:
                # already guaranteed
                got_promotional = True
                fifty_char = True

    return tries, pity_counter, fifty_char, capture_value, bargain_coins, got_promotional

def full_5star_wishing(wishes, total_simulations, current_pity, fifty_origin, order, capture=0):
    """
    Simulates pulling characters/weapons in a specific order.
    Returns dens_prob_Promotional_order (list of counts).
    """
    num_chars = order.count("character")
    num_wpns = order.count("weapon")
    dens_prob = [0 for _ in range(num_chars + num_wpns + 1)]

    for _ in range(total_simulations):
        tries = wishes
        pity_char = current_pity[0]
        pity_wpn = current_pity[1]
        fifty_char = not fifty_origin[0]  # careful: original logic had inverted bool
        fifty_wpn = not fifty_origin[1]
        epitomized = 0
        capture_value = capture
        bargain_coins = 0.0

        progress = 0  # how many steps in "order" achieved

        for step, element in enumerate(order):
            if element == "character":
                tries, pity_char, fifty_char, capture_value, bargain_coins, success = simulate_character_pull(
                    tries, pity_char, fifty_char, capture_value, bargain_coins
                )
                if success:
                    progress += 1
                    dens_prob[progress] += 1
                else:
                    break
            elif element == "weapon":
                tries, pity_wpn, fifty_wpn, epitomized, bargain_coins, success = simulate_weapon_pull(
                    tries, pity_wpn, fifty_wpn, epitomized, bargain_coins
                )
                if success:
                    progress += 1
                    dens_prob[progress] += 1
                else:
                    break
            else:
                raise ValueError("Order must contain only 'character' or 'weapon'")

        if progress == 0:
            dens_prob[0] += 1
    
    return dens_prob