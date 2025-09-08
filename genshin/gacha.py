import sys
from random import random
import matplotlib.pyplot as plt
import datetime

def giveFinalday(day, month, year):
    '''
    Returns a date in a datetime format
    '''

    final_day = datetime.datetime.strptime(str(day)+str(month)+str(year),"%d%m%Y")

    return final_day

def datesMatrix(final_day,Currently_primos,Battle_Pass=True,Battle_Pass_Premium=False,events=True,Bendition=True):
    '''
    Returns the number of final primogems you will have in a certain final date.

    final_day: the final day in datetime format
    Currently_primos: integer
    Battle_Pass: Bool
    Battle_Pass_Premium: Bool
    events: Bool
    Bendition: Bool
    '''

    if final_day.date() < datetime.date.today():
        raise ValueError("You tried a past date")

    primogems_promotional = 0
    primogems_permanent = 0
    if Bendition:
        diary = 150
    else:
        diary = 60
    if events:
        diary = diary + 71
    abyss = 800
    theater = 1000
    paimons_bargains = 800
    bili = 300
    actualization = 600
    bannerreset = 40
    wish = 160
    main_event = 1100
    secondary_event = 450

    dates_of_new_versions = []
    dates_of_banner_reset = []

    end_date = final_day.date()
    delta = datetime.timedelta(days=1)
    day = datetime.date.today()+delta

    days_battlePass = Battle_pass_important_dates(final_day)

    while day <= end_date:
        primogems_promotional = primogems_promotional + diary

        if str(day).split("-")[-1] == "16" :
            primogems_promotional += abyss
        elif str(day).split("-")[-1] == "01":
            primogems_promotional += theater
        if str(day).split("-")[-1] == "01":
            primogems_promotional += paimons_bargains
            primogems_permanent += paimons_bargains
        if day in important_dates('bilibili',final_day):
            primogems_promotional += bili
        if day in important_dates('new_version',final_day):
            primogems_promotional += actualization
        if day in important_dates('banner_reset',final_day):
            primogems_promotional += bannerreset
        if day in important_dates('main_event', final_day):
            primogems_promotional += main_event
        if day in important_dates('secondary_event', final_day):
            primogems_promotional += secondary_event

        if Battle_Pass == True:
            if day in days_battlePass:
                primogems_permanent += wish

            if Battle_Pass_Premium == True:

                if day in days_battlePass:

                    if days_battlePass[day] == 'wish':
                        reward = wish
                    elif days_battlePass[day] == 'protos':
                        reward = 680

                    primogems_promotional += reward

        day += delta

    primogems_promotional += Currently_primos

    return [primogems_promotional, primogems_permanent]

def Battle_pass_important_dates(final_day):
    '''
    Returns a list with the important dates for the Battle Pass
    '''

    start_date = datetime.datetime.strptime('12032024',"%d%m%Y")
    end_date = final_day.date()
    delta = datetime.timedelta(days=1)
    list_of_important_dates = {}
    week_count = 0
    Actualization_week = 0

    num_weeks = 1
    week_day = 5
    Wishes = 5

    while start_date.date() <= end_date:
        if start_date.weekday() == 2:
            Actualization_week += 1
            if Actualization_week == 6:
                Wishes = 5
                Actualization_week = 0

        if Wishes > 0:
            if start_date.weekday() == week_day:
                week_count += 1
                if week_count == num_weeks: #1
                    week_count = 0
                    important_date = start_date
                    if Wishes > 1:
                        reward = 'wish'
                    elif Wishes == 1:
                        reward = 'protos'
                    Wishes = Wishes - 1

            if start_date.date() > datetime.date.today() and important_date != 0:
                list_of_important_dates[important_date.date()] = reward

            important_date = 0

        start_date += delta

    #print(list_of_important_dates)

    return list_of_important_dates

def important_dates(what,final_day):
    '''
    Returns a list with the important dates for the many things
    '''

    start_date = datetime.datetime.strptime('30072025',"%d%m%Y")
    end_date = final_day.date()
    delta = datetime.timedelta(days=1)
    list_of_important_dates = []
    week_count = 0

    if what == 'new_version':
        num_weeks = 6
        week_day = 2
    elif what == 'banner_reset':
        num_weeks = 3
        week_day = 2
    elif what == 'Battle_Pass':
        num_weeks = 1
        week_day = 5
    elif what == 'bilibili':
        num_weeks = 6
        week_day = 4
        start_date = start_date - datetime.timedelta(days=12)
    elif what == 'main_event':
        num_weeks = 6
        week_day = 6
        start_date = start_date + datetime.timedelta(days=7)
    elif what == 'secondary_event':
        num_weeks = 2
        week_day = 4
        start_date = start_date + datetime.timedelta(days=7)

    while start_date.date() <= end_date:
        important_date = 0
        if start_date.weekday() == week_day:
            week_count = week_count + 1
            if week_count == num_weeks: #2
                week_count = 0
                important_date = start_date

        if start_date.date() > datetime.date.today() and important_date != 0:
            list_of_important_dates.append(important_date.date())

        start_date += delta

    return list_of_important_dates

def gold_num_prob(wishes, total_tries, currently_pitty, fifty_origin, Number_of_5stars):
    '''
    It returns a list with the probabilities of achieving different quantities of
    5 star characters and a promotional 5 stars character.

    wishes: integer
    total_tries: integer
    currently_pitty: integer
    fifty_origin: Bool
    Number_of_5stars: integer
    '''

    #Final vecttrd
    if wishes < 500:
        number = 25
    else:
        number = 40
    dens_prob = [0 for zero in range(0, number)]
    dens_prob_Promotional_character = [0 for zero in range(0, Number_of_5stars+1)]
    # [quehacerconelvalor for valorquedevuelve in iterable]

    #Parameters
    prob_nonpitty = 0.006
    nonpitty_duration = 76
    prob_pitty = 0.06
    pitty_duration = 90
    prob_90 = 1

    #All tries 5 stars
    for n in range(total_tries):
        first_try = True
        tries = wishes
        GOLD_total = 0
        Promotional_character = 0
        fifty = fifty_origin

        while tries > 0:

            GOLD = False
            start_point = 1

            if first_try == True:
                start_point = currently_pitty
                first_try = False

            #Nonpitty
            for tirada in range(start_point,nonpitty_duration):
                luck = random()
                tries = tries - 1

                if luck <= prob_nonpitty:
                    GOLD_total = GOLD_total + 1
                    GOLD = True
                    break

                elif tries <= 0:
                    break

                else:
                    continue

            #SubPitty
            if not GOLD == True and tries > 0:
                i = 0

                for tirada in range(nonpitty_duration,pitty_duration):
                    luck = random()
                    tries = tries - 1
                    i = i + 1

                    if luck <= prob_pitty*i:
                        GOLD_total = GOLD_total + 1
                        GOLD = True
                        break

                    elif tries <= 0:
                        break

                    else:
                        continue

            #Wish 90
            if GOLD == False and tries > 0:
                GOLD_total = GOLD_total + 1
                tries = tries - 1
                GOLD = True

            #50/50
            if GOLD == True:
                if fifty == True:
                    luck_50 = random()

                    if luck_50 < 0.50000:
                        fifty = True
                        Promotional_character = Promotional_character + 1
                    elif luck_50 >= 0.50000:
                        luck_capture = random()
                        if luck_capture <= 0.10000:
                            fifty = True
                            Promotional_character = Promotional_character + 1
                        else:
                            fifty = False

                elif fifty == False:
                    Promotional_character = Promotional_character + 1
                    fifty = True

            elif GOLD == False and tries > 0:
                print('Parece ser que no has conseguido dorada en 90 tiradas, revisa el código')

            #No more wishes
            if tries <= 0:
                break

        #Write down the results
        dens_prob[GOLD_total] = dens_prob[GOLD_total] + 1
        if Promotional_character >= Number_of_5stars:
            dens_prob_Promotional_character[Number_of_5stars] = dens_prob_Promotional_character[Number_of_5stars] + 1
        else:
            dens_prob_Promotional_character[Promotional_character] = dens_prob_Promotional_character[Promotional_character] + 1



    return [dens_prob, dens_prob_Promotional_character]

def goldweapon_num_prob(wishes, total_tries, currently_pitty, fifty_origin, Number_of_5stars):
    '''
    It returns a list with the probabilities of achieving different quantities of
    5 star weapons and promotional 5 stars weapons, distinguished.

    wishes: integer
    total_tries: integer
    currently_pitty: integer
    fifty_origin: Bool
    Number_of_5stars: integer
    '''

    #Final vecttrd
    if wishes < 500:
        number = 25
    else:
        number = 40
    dens_prob = [0 for zero in range(0, number)]
    dens_prob_Promotional_weapon1 = [0 for zero in range(0, Number_of_5stars+1)]
    dens_prob_Promotional_weapon2 = [0 for zero in range(0, Number_of_5stars+1)]
    dens_prob_Permanent_weapon = [0 for zero in range(0, Number_of_5stars*5)]


    #Parameters
    prob_nonpitty = 0.007
    nonpitty_duration = 66
    prob_pitty = 0.3
    pitty_duration = 80
    prob_80 = 1

    #All tries 5 stars
    for n in range(total_tries+1):
        first_try = True
        tries = wishes
        GOLD_total = 0
        Promotional_weapon1 = 0
        Promotional_weapon2 = 0
        Permanent_weapon = 0
        fifty = fifty_origin
        count_epitomized_path = 0

        while tries > 0:

            GOLD = 0
            start_point = 1

            if first_try == True:
                start_point = currently_pitty
                first_try = False

            #Nonpitty
            for tirada in range(start_point,nonpitty_duration):
                luck = random()
                tries = tries - 1
                #print('tirada_nonpitty')

                if luck <= prob_nonpitty:
                    GOLD_total = GOLD_total + 1
                    GOLD = True
                    break

                elif tries <= 0:
                    break

                else:
                    continue

            #Pitty
            if not GOLD == True and tries > 0:

                for tirada in range(nonpitty_duration,pitty_duration):
                    luck = random()
                    tries = tries - 1

                    if luck <= prob_pitty:
                        GOLD_total = GOLD_total + 1
                        GOLD = True
                        break

                    elif tries <= 0:
                        break

                    else:
                        continue

            #Wish 80
            if not GOLD == True and tries > 0:
                GOLD_total = GOLD_total + 1
                tries = tries - 1
                GOLD = True

            #75/25 & 50/50
            if GOLD == True:
                if fifty == True:
                    luck_75 = random()

                    if luck_75 < 0.75000 or count_epitomized_path == 1:
                        fifty = True
                        luck_50 = random()

                        if luck_50 < 0.5000 or count_epitomized_path == 1:
                            Promotional_weapon1 = Promotional_weapon1 + 1
                            count_epitomized_path = 0
                        elif luck_50 >= 0.5000:
                            Promotional_weapon2 = Promotional_weapon2 + 1
                            count_epitomized_path = count_epitomized_path + 1
                    elif luck_75 >= 0.75000:
                        Permanent_weapon = Permanent_weapon + 1
                        count_epitomized_path = count_epitomized_path + 1
                        fifty = False

                elif fifty == False:
                    luck_50 = random()
                    if luck_50 < 0.5000 or count_epitomized_path == 1:
                        Promotional_weapon1 = Promotional_weapon1 + 1
                        count_epitomized_path1 = 0
                    elif luck_50 >= 0.5000:
                        Promotional_weapon2 = Promotional_weapon2 + 1
                        count_epitomized_path = count_epitomized_path + 1
                    fifty = True

            #No more wishes
            if tries <= 0:
                break

        #Write down the results
        dens_prob[GOLD_total] = dens_prob[GOLD_total] + 1
        if Promotional_weapon1 >= Number_of_5stars:
            dens_prob_Promotional_weapon1[Number_of_5stars] = dens_prob_Promotional_weapon1[Number_of_5stars] + 1
        else:
            dens_prob_Promotional_weapon1[Promotional_weapon1] = dens_prob_Promotional_weapon1[Promotional_weapon1] + 1

        if Promotional_weapon2 >= Number_of_5stars:
            dens_prob_Promotional_weapon2[Number_of_5stars] = dens_prob_Promotional_weapon2[Number_of_5stars] + 1
        else:
            dens_prob_Promotional_weapon2[Promotional_weapon2] = dens_prob_Promotional_weapon2[Promotional_weapon2] + 1

        dens_prob_Permanent_weapon[Permanent_weapon] = dens_prob_Permanent_weapon[Permanent_weapon] + 1

    return [dens_prob, dens_prob_Promotional_weapon1, dens_prob_Promotional_weapon2, dens_prob_Permanent_weapon]

def purple_num_prob(wishes, total_tries, four_star_garanteed = True, pitty_4star = 0):
    '''
    It returns a list with the probabilities of achieving different quantities of
    4 star weapons and promotional 4 stars weapons, distinguishing between promotional or not.

    wishes: integer
    total_tries: integer
    four_star_garanteed: Bool. Weather the next 4 star is from the banner or 50/50
    pitty_4star: integer
    '''

    prob_4star = 0.06
    dens_prob_4star_temporal_character = []
    dens_prob_4star_permanent_character = []

    #All tries 4 stars
    for n in range(total_tries):
        tries = wishes
        gotcha4star = False
        four_stars = 0
        temporal_4star = 0
        other_4star = 0

        while tries > 0:

            tries = tries - 1

            if pitty_4star < 10:
                if random() <= prob_4star:
                    pitty_4star = 0
                    gotcha4star = True
                else:
                    pitty_4star = pitty_4star + 1
                    gotcha4star = False

            elif pitty_4star == 10:
                four_stars = four_stars + 1
                gotcha4star = True
                pitty_4star = 0

            else:
                print('error in number of 4 star pitty')

            if gotcha4star == True:
                if random() <= 0.5 or four_star_garanteed == True:
                    temporal_4star = temporal_4star + 1
                    four_star_garanteed = False
                else:
                    other_4star = other_4star + 1
                    four_star_garanteed = True

            #No more wishes
            if tries <= 0:
                break

        #Write down the results
        dens_prob_4star_temporal_character.append(temporal_4star)
        dens_prob_4star_permanent_character.append(other_4star)

    average_4star_temporal = sum(dens_prob_4star_temporal_character)/len(dens_prob_4star_temporal_character)
    average_4star_permanent = sum(dens_prob_4star_permanent_character)/len(dens_prob_4star_permanent_character)

    return [average_4star_temporal, average_4star_permanent]

def purpleweapon_num_prob(wishes, total_tries, four_star_garanteed = True, pitty_4star = 0):
    '''
    It returns a list with the probabilities of achieving different quantities of
    4 star weapons and promotional 4 stars weapons, distinguishing between promotional or not.

    wishes: integer
    total_tries: integer
    four_star_garanteed: Bool. Weather the next 4 star is from the banner or 50/50
    pitty_4star: integer
    '''

    prob_4star = 0.06
    dens_prob_4star_temporal_weapon = []
    dens_prob_4star_permanent = []

    #All tries 4 stars
    for n in range(total_tries):
        tries = wishes
        gotcha4star = False
        four_stars = 0
        temporal_4star = 0
        other_4star = 0

        while tries > 0:

            tries = tries - 1

            if pitty_4star < 10:
                if random() <= prob_4star:
                    pitty_4star = 0
                    gotcha4star = True
                else:
                    pitty_4star = pitty_4star + 1
                    gotcha4star = False

            elif pitty_4star == 10:
                four_stars = four_stars + 1
                gotcha4star = True
                pitty_4star = 0

            else:
                print('error in number of 4 star pitty')

            if gotcha4star == True:
                if random() <= 0.75 or four_star_garanteed == True:
                    temporal_4star = temporal_4star + 1
                    four_star_garanteed = False
                else:
                    other_4star = other_4star + 1
                    four_star_garanteed = True

            #No more wishes
            if tries <= 0:
                break

        #Write down the results
        dens_prob_4star_temporal_weapon.append(temporal_4star)
        dens_prob_4star_permanent.append(other_4star)

    average_4star_temporal = sum(dens_prob_4star_temporal_weapon)/len(dens_prob_4star_temporal_weapon)
    average_4star_permanent = sum(dens_prob_4star_permanent)/len(dens_prob_4star_permanent)

    return [average_4star_temporal, average_4star_permanent]

def needeprimos(threshold, banner, desired_5star, pitty, fifty_fifty, step=50):
    '''
    Returns the number of wishes you need to achieve a certain probability
    to get a 5 star character or weapon.

    threshold: integer. Between 0 and 1. Probability with which you want to achieve something
    banner: string. Choose between these: ['character', 'weapon']
    desired_5star: integer. Number of 5 stars you want
    pitty: intger
    fifty_fifty: Bool
    '''

    prob_is_near_threshold = False
    step = step
    wishes = 100
    num_iterations = 1
    tries = 10000
    error = 0.009
    toomuch = False
    tooless = False
    prob_old = 0

    if threshold >= 1:
        threshold = 0.98
        print('setting threshold to 100% of probabilities')

    while prob_is_near_threshold == False:

        if banner == 'character':
            prob = gold_num_prob(wishes, tries, pitty, fifty_fifty, desired_5star)[1][-1]/tries
        elif banner == 'weapon':
            prob = goldweapon_num_prob(wishes, tries, pitty, fifty_fifty, desired_5star)[1][-1]/tries

        if prob > threshold-error and prob < threshold+error:
            prob_is_near_threshold = True
            break
        elif prob > threshold-error:
            if tooless == True:
                num_iterations = num_iterations + 1
            wishes = wishes - step/num_iterations
            toomuch = True
            tooless = False
        elif prob < threshold+error:
            if toomuch == True:
                num_iterations = num_iterations + 1
            wishes = wishes + step/num_iterations
            toomuch = False
            tooless = True
        else:
            print('error')
        prob_old = prob

    return wishes

def full_5star_wishing(wishes, total_simulations, current_pitty, fifty_origin, order, capture=0):

    '''
    A function that simulates character and weapon wishes with an specified order, and gives as output
    how far you will be in in your desired wishing campaign.

    wishes: int
    total_simulations: int - tries to build statistics
    currently_pitty: list of two int
    fifty_origin: list of two bool - you depend on luck? then True
    Number_of_5stars: list of two int
    Order: list - list of strings being 'character or 'weapon' in the order you want to pull
    Capture: int - number of 50/50 already lost in a row (between 0 and 3)
    '''

    # Final vector
    Number_of_5stars = [0, 0]
    for i in order:
        if i == 'character':
            Number_of_5stars[0] += 1
        elif i == 'weapon':
            Number_of_5stars[1] += 1

    # if wishes < 500:
    #     number = 25
    # else:
    #     number = 40
    # dens_prob = [0 for zero in range(0, number)]
    dens_prob_Promotional_order = [0 for zero in range(0, Number_of_5stars[0]+Number_of_5stars[1]+1)]

    #Parameters
    prob_char_nonpitty = 0.006
    nonpitty_char_duration = 76
    prob_char_pitty = 0.06
    pitty_char_duration = 90
    prob_char_90 = 1

    prob_wpn_nonpitty = 0.007
    nonpitty_wpn_duration = 66
    prob_wpn_pitty = 0.07
    pitty_wpn_duration = 80
    prob_wpn_80 = 1

    pitty_4star_char = 10
    pitty_4star_weapon = 10

    bargain_coins = 0.0

    if capture not in [0, 1, 2, 3]:
        raise ValueError('Capture value must be between 0 - 3 and without decimals')

    # Start simulation

    for m in range(total_simulations):
        # first_try = True
        tries = wishes
        characters = 0
        promotional_characters = 0
        weapons = 0
        promotional_weapons = 0
        fifty_character = not fifty_origin[0]
        fifty_weapon = not fifty_origin[1]
        epitomized = 0
        pre_promotional_characters = 0
        pre_promotional_weapons = 0
        pitty_character = current_pitty[0]
        pitty_weapon = current_pitty[1]
        char_got = False
        wpn_got = False
        capture_value = capture

        for n,element in enumerate(order):
            if tries > 0:
                if element == 'character':

                    pre_promotional_characters = promotional_characters
                    gold = False

                    while promotional_characters != pre_promotional_characters+1 and tries > 0:

                        starting_pitty = 1
                        if char_got == False:
                            starting_pitty = pitty_character

                        # Nonpitty
                        for t in range(starting_pitty,nonpitty_char_duration+1):
                            luck = random()
                            tries = tries - 1

                            if luck <= prob_char_nonpitty:
                                characters = characters + 1
                                gold = True
                                break
                            elif luck > prob_char_nonpitty:
                                luck_4 = random()
                                if luck_4 <= 0.1 or  pitty_4star_char == 10:
                                    bargain_coins += 3.5
                                    pitty_4star_char = 0
                                else:
                                    pitty_4star_char += 1

                                while bargain_coins >= 5.0:
                                    bargain_coins -= 5.0
                                    tries += 1

                            elif tries <= 0:
                                break
                            else:
                                continue

                        # Subpitty
                        if gold == False and tries > 0:
                            for t in range(nonpitty_char_duration, pitty_char_duration):
                                luck = random()
                                tries = tries - 1

                                if luck <= prob_char_pitty:
                                    characters = characters + 1
                                    gold = True
                                    break
                                elif luck > prob_char_nonpitty:
                                    luck_4 = random()
                                    if luck_4 <= 0.1 or pitty_4star_char == 10:
                                        bargain_coins += 3.5
                                        pitty_4star_char = 0
                                    else:
                                        pitty_4star_char += 1

                                    while bargain_coins >= 5.0:
                                        bargain_coins -= 5.0
                                        tries += 1

                                elif tries <= 0:
                                    break
                                else:
                                    continue

                        # Ensured
                        if gold == False and tries > 0:
                            tries = tries - 1
                            gold = True

                        #50/50
                        if gold == True and tries > -1:
                            char_got = True
                            if fifty_character == True:
                                luck_50 = random()

                                if capture_value in [0, 1]:
                                    luck_value = -1.0
                                elif capture_value == 2:
                                    luck_value = 0.10000
                                elif capture_value == 3:
                                    luck_value = 2.0

                                if luck_50 < 0.50000:
                                    fifty_character = True
                                    promotional_characters = promotional_characters + 1
                                else:
                                    luck_capture = random()
                                    if luck_capture <= luck_value:
                                        fifty_character = True
                                        promotional_characters = promotional_characters + 1
                                        capture_value = 0
                                    else:
                                        fifty_character = False
                                        capture_value += 1

                            elif fifty_character == False:
                                promotional_characters = promotional_characters + 1
                                fifty_character = True

                elif element == 'weapon':

                    pre_promotional_weapons = promotional_weapons
                    gold = False

                    while promotional_weapons != pre_promotional_weapons+1 and tries > 0:

                        starting_pitty = 1
                        if wpn_got == False:
                            starting_pitty = pitty_weapon

                        # Nonpitty
                        for t in range(starting_pitty,nonpitty_wpn_duration+1):
                            luck = random()
                            tries = tries - 1

                            if luck <= prob_wpn_nonpitty:
                                weapons = weapons + 1
                                gold = True
                                break
                            elif luck > prob_char_nonpitty:
                                luck_4 = random()
                                if luck_4 <= 0.1 or  pitty_4star_weapon == 10:
                                    bargain_coins += 2.5
                                    pitty_4star_weapon = 0
                                else:
                                    pitty_4star_weapon += 1

                                while bargain_coins >= 5.0:
                                    bargain_coins -= 5.0
                                    tries += 1

                            elif tries <= 0:
                                break
                            else:
                                continue

                        # Subpitty
                        if gold == False and tries > 0:
                            for t in range(nonpitty_wpn_duration, pitty_wpn_duration):
                                luck = random()
                                tries = tries - 1

                                if luck <= prob_wpn_pitty:
                                    weapons = weapons + 1
                                    gold = True
                                    break
                                elif luck > prob_char_nonpitty:
                                    luck_4 = random()
                                    if luck_4 <= 0.1 or  pitty_4star_weapon == 10:
                                        bargain_coins += 2.5
                                        pitty_4star_weapon = 0
                                    else:
                                        pitty_4star_weapon += 1

                                    while bargain_coins >= 5.0:
                                        bargain_coins -= 5.0
                                        tries += 1

                                elif tries <= 0:
                                    break
                                else:
                                    continue

                        # Ensured
                        if gold == False and tries > 0:
                            tries = tries - 1
                            gold = True

                        #50/50 and Epitomized Path
                        if gold == True:
                            wpn_got = True
                            if fifty_weapon == True:
                                luck_70 = random()

                                if luck_70 < 0.700000 or epitomized == 1:
                                    fifty_weapon = True
                                    luck_epitomized = random()
                                    if luck_epitomized < 0.500000 or epitomized == 1:
                                        promotional_weapons = promotional_weapons + 1
                                    else:
                                        epitomized += 1

                                elif luck_70 >= 0.700000:
                                    fifty_weapon = False
                                    epitomized += 1

                            elif fifty_weapon == False:
                                fifty_weapon = True
                                luck_epitomized = random()
                                if luck_epitomized < 0.500000 or epitomized == 1:
                                    promotional_weapons = promotional_weapons + 1
                                else:
                                    epitomized += 1

                else:
                    raise ValueError('In order list select either character or weapon')

                if promotional_characters == pre_promotional_characters+1 and order[n] == 'character':
                    dens_prob_Promotional_order[n+1] += 1
                elif promotional_weapons == pre_promotional_weapons+1 and order[n] == 'weapon':
                    dens_prob_Promotional_order[n+1] += 1
                elif promotional_characters == 0 and promotional_weapons == 0:
                    dens_prob_Promotional_order[0] += 1

    return dens_prob_Promotional_order
