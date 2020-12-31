from dwave.system.samplers import DWaveSampler           
from dwave.system.composites import EmbeddingComposite   
import dwave.inspector
import json
from pathlib import Path

'''
  Small class to make running some examples a little easier and less of an ugly script
'''
class Task:
    def __init__(self, quantum=True):
        self.sampler = DWaveSampler(solver={"qpu":quantum})
        self.input_data = None
        self.result = None

    '''
      dictionaries with tuples as keys as input
    '''
    def set_data_with_dicts(self, objective, constraints):

        # first make sure all data keys are tuples
        def check_tuples(data):
            for i in data.keys():
                if type(i) != tuple:
                    raise Exception(f"All keys for input data must be tuples") 
        
        # It feels wrong to do this like this but it works
        check_tuples(objective)
        check_tuples(constraints)

        self.input_data = {**objective, **constraints}

    def run_data(self, chain_strength=5, num_reads=100):
        if self.input_data == None:
            raise Exception("You must include a dataset, use set_data") 
        
        print(f"Using Chain Strength: {chain_strength}")
        print(f"Number of reads: {num_reads}")

        self.result = EmbeddingComposite(self.sampler).sample_qubo(self.input_data, chain_strength=chain_strength, num_reads=num_reads)

    '''
      save response as json, must name file
    '''
    def save_as_json(self, name=None, p=None):

        # if no path specified use working dir
        if p == None:
            p = Path.cwd()


        identifier = self.result.info["problem_id"]

        if name == None:
            name = str(identifier) # pretty sure this is a string but just to make sure.

        try:            
            with open(f"{name}.json", "w") as t_r:

                print(f'Writing response with id: {identifier} to file {name}.json in path: {p}')

                json.dump(self.result.to_serializable(), t_r) 

                t_r.close()

        except Exception as e:
            raise Exception(f"An unexpected error occured: {e} while trying to save result with id: {identifier} to path: {p} as json") 