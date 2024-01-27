"""
code by qitang
last update: 01/27/2024

vectorize_v0 ==> brutal way
vectorize ==> normalize each sensor (recommend to try)
ecllipse_filter ==> post filter tuning

"""
import numpy as np 

foot_center_parameter = (158, 366) #parameter

scaling_factor_default = np.ones(16) #current scale is based on the relative x, y position of each sensor
pad_position_list = [(237, 217), (241, 104), (183, 641), (177, 534), (187, 394), (182, 236), (198, 90), (114, 645), (108, 538), (139, 399), (134, 240), (162, 95), (94, 432), (83, 324), (83, 225), (118, 121)]

def vectorize_v0(weight_subsequent, weight_initial, scaling_factor, foot_center_parameter = foot_center_parameter):
    pad_vector_list = [(x - foot_center_parameter[0], y - foot_center_parameter[1]) for x, y in pad_position_list]
    weight_delta = np.array(weight_subsequent) - np.array(weight_initial)
    weight_delta = weight_delta * scaling_factor
    vector_x, vector_y, vector_z = 0, 0, 0 # vector_z is relative to gravity
    for i, (x, y) in enumerate(pad_vector_list):
        vector_x += weight_delta[i]*x
        vector_y += weight_delta[i]*y
    vector_z = -(sum(weight_subsequent) - sum(weight_initial)) #more pressure --> more towards the ground
    print(vector_x, vector_y, vector_z)
    return vector_x, vector_y, vector_z

def vectorize(weight_subsequent, weight_initial, scaling_factor, foot_center_parameter = foot_center_parameter):
    pad_vector_list = [(x - foot_center_parameter[0], y - foot_center_parameter[1]) for x, y in pad_position_list]
    weight_initial = np.array(weight_initial)
    weight_subsequent = np.array(weight_subsequent)

    weight_delta = weight_subsequent - weight_initial
    weight_initial = weight_initial + 1E-6

    weight_delta = weight_delta / weight_initial
    weight_delta = weight_delta * scaling_factor
    vector_x, vector_y, vector_z = 0, 0, 0 # vector_z is relative to gravity
    for i, (x, y) in enumerate(pad_vector_list):
        vector_x += weight_delta[i]*x
        vector_y += weight_delta[i]*y
    vector_z = -(sum(weight_subsequent) - sum(weight_initial)) #more pressure --> more towards the ground
    print(vector_x, vector_y, vector_z)
    return vector_x, vector_y, vector_z

def ecllipse_filter(vector_x, vector_y, vector_z):
    pass

if __name__ == "__main__":
    weight_subsequent = [1.5] + [1]*15
    weight_initial = [1]*16
    vectorize(weight_subsequent, weight_initial, scaling_factor=scaling_factor_default)