import matplotlib.pyplot as plt
import pandas as pd
import re


#### Load data from characters
def loaddata(character_name):
    '''
    It returns a pandas dataframe with the basic stats of a selected character.
    '''

    df = pd.read_csv("/home/rubenm/repos/genshin/genshin/Characters.csv")
    df1 = df.loc[df["Name"] == character_name]
    return df1

def adddatatodf(source,df1,hp=0,atk=0,deff=0,hpp=0,atkp=0,defp=0,edmg=0,fdmg=0,em=0,cr=0,cdmg=0,er=0,hp_=0,atk_=0,def_=0,hb=0):
    '''
    It returns the same data frame with an extra row refering to an artifact or weapon, for example.
    '''

    dictionary_of_stats = {"Name":source,"hp":hp,"atk":atk,"def":deff,"hpp":hpp,"atkp":atkp,"defp":defp,
                            "edmg":edmg,"fdmg":fdmg,"em":em,"cr":cr,"cdmg":cdmg,"er":er,"hp%":hp_,"atk%":atk_,"def%":def_,"hb":hb}

    df2 = df1.append(dictionary_of_stats,ignore_index=True)

    return df2

def getsumofstats(df2):
    '''
    It returns the same dataframe with an extra row with the sum of all the values in all columns called final_stats.
    '''

    suma = df2.sum()
    suma["Name"] = "final_stats"
    df3 = df2.append(suma,ignore_index=True)

    return df3

def final_stats(dataframe,Name_of_the_character):
    '''
    It return a dictionary with all the final stats that your character have.
    '''

    Final_stats = {}
    Final_stats1 = dataframe.iloc[[-1]].to_dict(orient="records")
    Final_stats["NAME"] = Name_of_the_character
    Final_stats["HP"] = Final_stats1[0]["hpp"]+Final_stats1[0]["hp"]*(1+Final_stats1[0]["hp%"]/100)
    Final_stats["ATK"] = Final_stats1[0]["atkp"]+Final_stats1[0]["atk"]*(1+Final_stats1[0]["atk%"]/100)
    Final_stats["DEF"] = Final_stats1[0]["defp"]+Final_stats1[0]["def"]*(1+Final_stats1[0]["def%"]/100)
    Final_stats["EM"] = Final_stats1[0]["em"]
    Final_stats["ER"] = Final_stats1[0]["er"]+100
    Final_stats["CR"] = Final_stats1[0]["cr"]
    Final_stats["CDMG"] = Final_stats1[0]["cdmg"]
    Final_stats["EDMG"] = Final_stats1[0]["edmg"]
    Final_stats["FDMG"] = Final_stats1[0]["fdmg"]

    return Final_stats

def singleattack(dict_stats,hability_dmg,basis='ATK',Elemental=True,Fisical=False,lvl=90,enemy_lvl=93,Enemy_RES=10,Reaction=False,Res=False):
    '''
    It returns the dmg a single attack would do.

    dict_stats: a dictiorany with all the stats (see loaddata())
    hability_dmg: integer. The damage multiplier.
    basis: string. The escaling of the hability damage. By default is attack.
    Elemental: bool. Set to True if your damage is elemental.
    Fisical: bool. Set to True if your damage is fisical.
    lvl: integer. Your level.
    enemy_lvl: integer.
    Enemy_RES: integer.
    Reaction: string. Only amplifying reactions: Melt_fire, Melt_ice, Vape_water, Vape_fire
    '''

    Enemy_DEF = (lvl+100)/(lvl+enemy_lvl+200)
    if Fisical == True:
        type_of_dmg = 'FDMG'
        Elemental = False
    elif Elemental == True:
        type_of_dmg = 'EDMG'
        Fisical=False

    if Res == False:
        Rfactor = 0
    elif Res != False and isinstance(Res, int):
        Rfactor = Res

    Enemy_RES = Enemy_RES - Rfactor
    if Enemy_RES < 0:
            Enemy_RES = Enemy_RES/2

    if Reaction == 'Vape_water'or Reaction == 'Melt_fire':
        reaction = 2
    elif Reaction == 'Vape_fire' or Reaction == 'Melt_ice':
        reaction = 1.5
    else:
        reaction = 1

    DMG_of_an_attack = dict_stats[basis]*hability_dmg/100*(1+dict_stats[type_of_dmg]/100)*Enemy_DEF*(100-Enemy_RES)/100*(1+dict_stats['CDMG']/100)*reaction

    return DMG_of_an_attack

def stats_optimizer(Final_stats, damage_formula='(1.36*{EM}+{ATK})*1.78*(1+{EDMG}/100)*(1+{CDMG}/100)', DEF=0.5,
                    RES=0.9, ignore=[], max_var_stat=4, max_var_total=10, print_output=True, print_values=False,
                    set_jumps={}, verbose=False, min_values=None):

    Final_stats['DEFx'] = DEF
    Final_stats['RES'] = RES
    ignore.append('DEFx')
    ignore.append('RES')

    # Generate formula
    if isinstance(damage_formula, str):
        def formula_calculator(damage_formula, values_dict, DEF=DEF, RES=RES):
            result = eval(damage_formula.format(**values_dict))
            variable_names = re.findall(r"\{(\w+)\}", damage_formula)
            return [result, variable_names]

    elif isinstance(damage_formula, dict):
        def formula_calculator(damage_formula, values_dict, DEF=DEF, RES=RES):
            results = {}
            variables = []
            for i in damage_formula.keys():
                value = eval(i.format(**values_dict))
                results[value] = damage_formula[i]
                variable_names = re.findall(r"\{(\w+)\}", i)
                for i in variable_names:
                    if i not in variables:
                        variables.append(i)
            weighted_sum = 0
            for key in results.keys():
                weighted_sum += key * results[key]
            result = weighted_sum
            return [result, variables]

    raw_value = formula_calculator(damage_formula, Final_stats)[0]

    participating_stats = formula_calculator(damage_formula, Final_stats)[1]
    for i in ignore:
        participating_stats.remove(i)

    # Optimize stats
    jumps = {'HP':300, 'ATK':56, 'DEF':60, 'EM':23, 'CR':3.9, 'CDMG':7.8, 'EDMG':7, 'FDMG':7, 'ER':6.5}
    if len(set_jumps.keys()) > 0:
        for i in set_jumps:
            jumps[i] = set_jumps[i]
    if min_values == None:
        min_values = {'HP':12000, 'ATK':1100, 'DEF':500, 'EM':0, 'CR':5, 'CDMG':50, 'EDMG':0, 'FDMG':0, 'ER':100}
    else:
        values = {'HP':12000, 'ATK':1100, 'DEF':500, 'EM':0, 'CR':5, 'CDMG':50, 'EDMG':0, 'FDMG':0, 'ER':100}
        for i in min_values:
            values[i] = min_values[i]
        min_values = values

    # Set count of stats
    counter = {}
    for i in participating_stats:
        counter[i] = 0
    total_counter = 0
    best_prev = 0

    # Run improvement
    improvement_stats_history = {'Improved':[],'Decreased':[],'Value':[]}
    improved_stats = Final_stats.copy()

    for i in range(max_var_total):

        # Run one iteration per stat
        for i in participating_stats:
            if counter[i] >= max_var_stat:
                participating_stats.remove(i)
        current_stats = improved_stats.copy()

        if len(participating_stats) < 2:
            break
        best_damage = {}
        for i in participating_stats:
            best_damage[i] = {}

        old_value = formula_calculator(damage_formula, improved_stats)[0]
        for stat1 in participating_stats:

            for stat2 in participating_stats:
                current_stats = improved_stats.copy()
                if stat1 != stat2: # and current_stats['CR'] < 100 and current_stats['ATK'] > min_atk and current_stats['HP'] > min_hp:
                    current_stats[stat1] = current_stats[stat1] + jumps[stat1]
                    current_stats[stat2] = current_stats[stat2] - jumps[stat2]
                    new_value = formula_calculator(damage_formula, current_stats)[0]
                    best_damage[stat1][stat2] = new_value
                    if new_value > old_value:
                        best_stats_to_be_changed = [stat1, stat2]
                        best_value = new_value
                        old_value = new_value

                    if current_stats[stat1] <= min_values[stat1]:
                        try:
                            participating_stats.remove(stat1)
                        except:
                            nothing=True
                    if current_stats[stat2] <= min_values[stat2]:
                        try:
                            participating_stats.remove(stat2)
                        except:
                            nothing=True
                    if current_stats['CR'] >= 100:
                        try:
                            participating_stats.remove('CR')
                        except:
                            nothing=True


        # Annotate best stat, actualise damage and stats
        best = 0
        #print(best_damage)
        for i in participating_stats:
             for j in participating_stats:
                    if i != j:
                        try:
                            if best_damage[i][j] > best:
                                up = i
                                down = j
                                best = best_damage[i][j]
                        except:
                            continue
        if best < best_prev:
            continue
        improvement_stats_history['Improved'].append(up)
        improvement_stats_history['Decreased'].append(down)
        improvement_stats_history['Value'].append(best)
        improved_stats[up] = improved_stats[up] + jumps[up]
        improved_stats[down] = improved_stats[down] - jumps[down]
        counter[up] = counter[up] + 1
        best_prev = best

    proportion = (improvement_stats_history['Value'][-1]/raw_value-1)*100
    # print('You would gain a '+str(proportion)[:5]+'% of increased damage')
    increase_stats = []
    for string in improvement_stats_history['Improved']:
        if string not in increase_stats:
            increase_stats.append(string)
    decrease_stats = []
    for string in improvement_stats_history['Decreased']:
        if string not in decrease_stats:
            decrease_stats.append(string)

    if print_output:
        print('You would gain a '+str(proportion)[:5]+'% of increased damage')
        print('Best stats to increase -> '+','.join(increase_stats))
        print('Less worst stats to decrease -> '+','.join(decrease_stats))
    if print_values:
        print('Prevoius damage: '+str(raw_value))
        print('Final damage: '+str(improvement_stats_history['Value'][-1]))
    if verbose:
        print('Improvement stats history')
        print(improvement_stats_history)
        print('Improved stats')
        print(improved_stats)

    return raw_value, improvement_stats_history['Value'][-1]

def stats_comparer(Final_stats1, Final_stats2, damage_formula='(1.36*{EM}+{ATK})*1.78*(1+{EDMG}/100)*(1+{CDMG}/100)', DEF=0.5,
                    RES=0.9, print_values=False, verbose=False):

    Final_stats1['DEFx'] = DEF
    Final_stats1['RES'] = RES
    Final_stats2['DEFx'] = DEF
    Final_stats2['RES'] = RES

    # Generate formula
    if isinstance(damage_formula, str):
        dictionary = {}
        dictionary[damage_formula] = 1
        damage_formula = dictionary

    if isinstance(damage_formula, dict):
        def formula_calculator(damage_formula, values_dict, DEF=DEF, RES=RES):
            results = {}
            variables = []
            for i in damage_formula.keys():
                value = eval(i.format(**values_dict))
                results[value] = damage_formula[i]
                variable_names = re.findall(r"\{(\w+)\}", i)
                for i in variable_names:
                    if i not in variables:
                        variables.append(i)
            weighted_sum = 0
            for key in results.keys():
                weighted_sum += key * results[key]
            result = weighted_sum
            return [result, variables]

    value1 = formula_calculator(damage_formula, Final_stats1)[0]
    value2 = formula_calculator(damage_formula, Final_stats2)[0]

    proportion = (value1/value2-1)*100
    print('You would gain a '+str(proportion)[:5]+'% of damage if you use '+Final_stats1['NAME']+' instead of '+Final_stats2['NAME'])
    if print_values:
        print(value1, value2)

def equipment_comparer(Final_stats1, Final_stats2, damage_formula1='(1.36*{EM}+{ATK})*1.78*(1+{EDMG}/100)*(1+{CDMG}/100)',
                       damage_formula2='{ATK}*1.78*(1+{EDMG}/100)*(1+{CDMG}/100)',DEF=0.5, RES=0.9, print_values=False, verbose=False):

    Final_stats1['DEFx'] = DEF
    Final_stats1['RES'] = RES
    Final_stats2['DEFx'] = DEF
    Final_stats2['RES'] = RES

    # Generate formula
    if isinstance(damage_formula1, str):
        dictionary = {}
        dictionary[damage_formula] = 1
        damage_formula = dictionary

    if isinstance(damage_formula2, str):
        dictionary = {}
        dictionary[damage_formula] = 1
        damage_formula = dictionary

    def formula_calculator(damage_formula, values_dict, DEF=DEF, RES=RES):
        results = {}
        variables = []
        for i in damage_formula.keys():
            value = eval(i.format(**values_dict))
            results[value] = damage_formula[i]
            variable_names = re.findall(r"\{(\w+)\}", i)
            for i in variable_names:
                if i not in variables:
                    variables.append(i)
        weighted_sum = 0
        for key in results.keys():
            weighted_sum += key * results[key]
        result = weighted_sum
        return [result, variables]

    value1 = formula_calculator(damage_formula1, Final_stats1)[0]
    value2 = formula_calculator(damage_formula2, Final_stats2)[0]

    proportion = (value1/value2-1)*100
    print('You would gain a '+str(proportion)[:5]+'% of damage if you use '+Final_stats1['NAME']+' instead of '+Final_stats2['NAME'])
    if print_values:
        print(value1, value2)
