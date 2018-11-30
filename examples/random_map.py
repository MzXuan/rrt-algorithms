import random
import numpy as np

def random_2d_map(x_dim,y_dim):
    obs_list = []
    obs_nums = random.randint(5,10)
    for i in range(obs_nums):
        x1 = random.randint(0,x_dim-1)
        y1 = random.randint(0,y_dim-1)

        obs_list.append(np.array([x1,y1,
                        random.randint(x1+1,x_dim),random.randint(y1+1,y_dim)]))

    return obs_list


def random_3d_map(x_dim,y_dim,z_dim):
    obs_list = []
    obs_nums = random.randint(5,10)
    for i in range(obs_nums):
        x1 = random.randint(0,x_dim - 1)
        y1 = random.randint(0,y_dim - 1)
        z1 = random.randint(0, z_dim - 1)

        obs_list.append(np.array([x1,y1,z1,
                        random.randint(x1+1,x_dim),random.randint(y1+1,y_dim), random.randint(z1+1,z_dim)]))

    return obs_list





