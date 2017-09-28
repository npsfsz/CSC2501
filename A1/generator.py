#! /usr/bin/env python3.5
'''Look for a specific bird over a bunch of days

This script simulates a bird watcher looking for a specific bird and
the God-like "birder" who determines what birds the watcher gets to see
that day. The arguments 'BIRDER' and 'WATCHER' determine whether
the birder and watcher store values in lists. 'DAYS' is the number of
days we watch for.

This script shows off how to read and write from generators. Generators
avoid unnecessary memory bloat of lists by calculating and returning
iterator elements one at a time, but this only 
'''

import random

from time import process_time

from argparse import ArgumentParser

__author__ = "Sean Robertson"
__email__ = "t6robert@cs.toronto.edu"

# a fraction of birds from wordnet
_BIRDS = [
    'Catharacta_skua', 'Tringa_flavipes', 'peewee', 'gallinaceous_bird',
    'yellowthroat', 'dunlin', 'notornis', 'Ardea_occidentalis',
    'English_sparrow', 'titlark', 'ring_blackbird', 'American_woodcock',
    'takahe', 'ern', 'lyrebird', 'coastal_diving_bird',
    'Vireo_solitarius', 'red-shouldered_hawk', 'Polynesian_tattler',
    'cuckoo', 'tit', 'tree_martin', 'bird_of_Juno', 'skua', 'cacique',
    'tufted_puffin', 'Buteo_buteo', 'Fulmarus_glacialis',
    'resplendent_quetzel', 'oilbird', 'lesser_whitethroat', 'antbird',
    'Haliatus_albicilla', 'wood-creeper', 'ocellated_turkey',
    'downy_woodpecker', 'Corvus_monedula', 'Oriolus_oriolus',
    'grey_catbird', 'songbird', 'grossbeak', 'ringdove', 'wren-tit',
    'longlegs', 'Chen_caerulescens', 'roller', 'darter',
    'Alcedo_atthis', 'Psophia_crepitans', 'ratite',
    'Phalaenoptilus_nuttallii', 'pine_grosbeak', 'pine_finch',
    'butterball', 'Parus_carolinensis', 'Circus_Aeruginosus',
    'great_auk', 'European_nightjar', 'rhea', 'ortolan', 'duck',
    'Mimus_polyglotktos', 'whidah', 'bushtit', 'nightjar',
    'Syrrhaptes_paradoxus', 'Bubo_virginianus', 'aepyornis', 'puffin',
    'Carpodacus_purpureus', 'Haliaeetus_leucocephalus', 'curlew',
    'ratite_bird', 'blue_tit', 'Eurasian_kingfisher',
    'European_nuthatch', 'kaki', "Mother_Carey's_chicken",
    'Dolichonyx_oryzivorus', 'carinate_bird', 'Padda_oryzivora',
    'true_sparrow', 'bush_tit', 'tufted_titmouse', 'tomtit',
    'lesser_scaup_duck', 'Garullus_garullus', 'whooper', 'piping_crow',
    'guan', 'red-legged_partridge', 'mockingbird', 'bantam',
    'gyrfalcon', 'Cygnus_columbianus', 'cochin', 'titmouse', 'scaup',
    'Milvus_migrans', 'smew', 'grey_kingbird', 'oyster_catcher', 'cock',
    "chuck-will's-widow", 'fulmar_petrel', 'Actitis_macularia',
    'petrel', 'chunga', 'Collocalia_inexpectata', 'cliff_swallow',
    'moorbird', 'Actitis_hypoleucos'
]

def make_birds_for_day():
    '''Make a single day's worth of birds

    A day is represented by a space-delimited string of a random and
    i.i.d. choice of birds.
    '''
    return ' '.join(
        random.choice(_BIRDS) for _ in range(random.randint(100, 1000)))

def find_bird_in_day(bird, day):
    '''Return the instances of a day's target bird'''
    return [x for x in day.split(' ') if x == bird]

def birder_generator(days):
    '''Generate the days' birds using generator syntax

    'day_generator' is an iterator that returns elements to the
    caller one at a time using 'yield'. Its stack persists until a
    caller asks for the next element of the iterator. The stack
    disappears when 'return' is called (implicitly or explicitly).
    '''
    for _ in range(days):
        yield make_birds_for_day()

def birder_list(days):
    '''Generate the days' birds using lists

    This is a dumb way to do it, since we only look at the day's birds
    once (we don't have need to store/index the days).
    '''
    return [make_birds_for_day() for _ in range(days)]

def watcher_daily(bird, day_iterator):
    '''Count the number of times the bird shows up by summing daily counts

    Since we throw away the day's list after we're done counting it,
    this code is efficient (especially with 'birder_generator')
    '''
    count = 0
    for day in day_iterator:
        count += len(find_bird_in_day(bird, day))
    return count

def watcher_global(bird, day_iterator):
    '''Count the number of times the bird shows up globally

    This is terribly inefficient because we store all daily values in
    a list when we don't need to. This would be more memory-intensive if
    we stored large chunks of data, like text corpora.
    '''
    birds = []
    for day in day_iterator:
        birds.extend(find_bird_in_day(bird, day))
    return len(birds)

def main(args=None):
    '''The main method'''
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('BIRDER', choices=['list', 'generator'])
    parser.add_argument('WATCHER', choices=['globally', 'daily'])
    parser.add_argument('DAYS', type=int)
    namespace = parser.parse_args(args)
    bird = random.choice(_BIRDS)
    print(
        'BIRDER - "Hullo! I am the birder! I will use a {}.'
        ' I will generator for {} days!"'.format(
            namespace.BIRDER, namespace.DAYS))
    print(
        'WATCHER - "Hail! I am the watcher! I will count {}.'
        ' I am looking for {}."'.format(namespace.WATCHER, bird))
    if namespace.BIRDER == 'list':
        day_iterator = birder_list(namespace.DAYS)
    else:
        day_iterator = birder_generator(namespace.DAYS)
    if namespace.WATCHER == 'globally':
        count = watcher_global(bird, day_iterator)
    else:
        count = watcher_daily(bird, day_iterator)
    print('WATCHER - "Behold! {} birds!"'.format(count))
    print('BIRDER - "That took {:.2f} seconds!'.format(process_time()))

if __name__ == '__main__':
    random.seed(420)
    exit(main())
