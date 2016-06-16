import pandas as pd
from collections import Counter
from dictionnaire_sport import sport_dict

def apply_sport(row):
    """ ajout des libellés de chaque FF"""
    try:
        return sport_dict[row]
    except KeyError:
        return row


def split_pop(s):
    return list(filter(None, s.split("pop")[1].split("_")))


def split_l(s):
    return list(filter(None, s.replace('2012', '2010').split("l")[1].split("_")))


def import_clean_licences_2012(path):
    # import
    t_licences = pd.read_csv(path, sep=";", quotechar="'", low_memory=False)
    t_licences.rename(columns={"l_30_44__2012": "l_30_44_2012"}, inplace=True)
    # get libellés des FF
    t_licences["fed_2012_libelles"] = t_licences['fed_2012'].apply(apply_sport)
    t_licences['poph_75_99_2010'] = [x.replace('"', '') for x in t_licences["poph_75_99_2010\""]]
    # fix invalid string
    t_licences["\"cog2"] = [x.replace('"', '') for x in t_licences["\"cog2"]]
    del t_licences['poph_75_99_2010\"']
    del t_licences["\"cog2"]
    # dtypes for pop indicators
    starts_with_pop = [x for x in t_licences.columns if x.startswith('pop')]
    t_licences.loc[:, t_licences.columns.isin(starts_with_pop)] =\
        t_licences.loc[:, t_licences.columns.isin(starts_with_pop)].convert_objects(convert_numeric=True)
    # calculate ratio
    l_labels = [x for x in t_licences.columns if x.startswith('l_')][:-3]
    pop_labels = [x for x in t_licences.columns if x.startswith('pop')]
    for l_lab in l_labels:
        for pop_lab in pop_labels:
            if (Counter(split_pop(pop_lab)) == Counter(split_l(l_lab))):
                t_licences[l_lab + "_ratio"] = t_licences[l_lab] / t_licences[pop_lab]
            else:
                pass

    return t_licences
