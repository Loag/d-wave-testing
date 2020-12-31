from src.task import Task

def run():

    # this is an and gate
    objective = {(0,0): -0.0, (1,1): -0.0, (2,2): 6.0}
    constraints = {(0, 1): 2.0, (0, 2): -4.0, (1,2): -4.0}

    # create a new task
    t = Task()

    # set the data for the task
    t.set_data_with_dicts(objective, constraints)

    # run the task on a quantum computer
    t.run_data()

    # save result as json 
    t.save_as_json()
    
if __name__ == "__main__":
    run()