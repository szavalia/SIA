from crossbreeding import crossbreeding_chooser
from selection import selection_chooser
from models import Metrics, Properties, Selection, Crossbreeding, Mutation
from selection import selection_chooser
from mutation import mutation_chooser
import json

def generate_output(metrics:Metrics,properties:Properties):
    print("Population's size: {0}".format(properties.population_size))
    print("Generations: {0}".format(properties.generations))
    print("Crossbreeding: {0}".format(properties.crossbreeding.method))
    print("Mutation: {0} p :{1}".format(properties.mutation.method, properties.mutation.probability))
    print("Selection: {0}".format(properties.selection.method))

    print("W: {0}\nw: {1}\nw0: {2}".format(metrics.individual.chromosome[0:3],[metrics.individual.chromosome[3:6], metrics.individual.chromosome[6:9]],metrics.individual.chromosome[9:11] ))
    print("Func val: [E1 : {0}, E2: {1}, E3: {2}]".format(metrics.ideal_func[0], metrics.ideal_func[1], metrics.ideal_func[2]))
    print("Error val: {0}".format(metrics.individual.fitness))
    
# Receive parameters from config.json and encapsulate them into properties object
def parse_properties():

    file = open('config.json')
    json_values = json.load(file)
    file.close()    
    
    initial_values = json_values.get("initial_values")
    initial_results = json_values.get("initial_results")
    population_size = json_values.get("population_size")
    if population_size == None or population_size <= 0:
        print("Specify a positive population size")
        exit(-1)

    generations = json_values.get("generations")
    if generations == None or generations <= 0:
        print("Specify a positive generation cap")
        exit(-1)

    selection = selection_chooser(json_values.get("selection"))
    mutation = mutation_chooser(json_values.get("mutation"))
    crossbreeding = crossbreeding_chooser(json_values.get("crossbreeding"))

    if(selection == None or mutation == None or crossbreeding == None):
        return None

    return Properties(initial_values,initial_results,population_size, generations, crossbreeding, mutation, selection)

