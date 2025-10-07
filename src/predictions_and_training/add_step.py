def add_step(pipeline, step_name, step):
    """
    Esta función agrega un paso a un pipeline de scikit-learn.
    """
    flag = 0
    for s in pipeline.steps:	
        if s[0] == step_name:
            pipeline.steps.remove(s)
            pipeline.steps.append((step_name, step))
            flag = 1
    if flag == 0:
        pipeline.steps.append((step_name, step))
    return pipeline