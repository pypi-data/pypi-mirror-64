import numpy as np
from PIL import Image
import torch
import torch.utils.data as data
import torchvision.transforms as transforms
import os




def produce_adjacent_matrix_2_neighbors(flag_bits, stroke_len):
    assert flag_bits.shape == (100, 1)
    adja_matr = np.zeros([100, 100], int)
  
    adja_matr[ : ][ : ] = -1e10

    adja_matr[0][0] = 0
    
    if (flag_bits[0] == 100):
        adja_matr[0][1] = 0


    for idx in range(1, stroke_len):
        
        adja_matr[idx][idx] = 0

        if (flag_bits[idx - 1] == 100):
            adja_matr[idx][idx - 1] = 0

        if idx == stroke_len - 1:
            break

        if (flag_bits[idx] == 100):
            adja_matr[idx][idx + 1] = 0

    return adja_matr


def produce_adjacent_matrix_4_neighbors(flag_bits, stroke_len):
    assert flag_bits.shape == (100, 1)
    adja_matr = np.zeros([100, 100], int)
    adja_matr[ : ][ : ] = -1e10

    adja_matr[0][0] = 0
    
    if (flag_bits[0] == 100):
        adja_matr[0][1] = 0
        
        if (flag_bits[1] == 100):
            adja_matr[0][2] = 0


    for idx in range(1, stroke_len):
        
        adja_matr[idx][idx] = 0

        if (flag_bits[idx - 1] == 100):
            adja_matr[idx][idx - 1] = 0
            
            if (idx >= 2) and (flag_bits[idx - 2] == 100):
                adja_matr[idx][idx - 2] = 0

        if idx == stroke_len - 1:
            break

        
        if (idx <= (stroke_len - 2)) and (flag_bits[idx] == 100):
            adja_matr[idx][idx + 1] = 0
            
            if (idx <= (stroke_len - 3)) and (flag_bits[idx + 1] == 100):
                adja_matr[idx][idx + 2] = 0

    return adja_matr


def produce_adjacent_matrix_joint_neighbors(flag_bits, stroke_len):
    assert flag_bits.shape == (100, 1)
    adja_matr = np.zeros([100, 100], int)
    adja_matr[ : ][ : ] = -1e10
    
    adja_matr[0][0] = 0
    adja_matr[0][stroke_len - 1] = 0
    adja_matr[stroke_len - 1][stroke_len - 1] = 0
    adja_matr[stroke_len - 1][0] = 0

    assert flag_bits[0] == 100 or flag_bits[0] == 101

    if (flag_bits[0] == 101) and stroke_len >= 2:
        adja_matr[0][1] = 0


    for idx in range(1, stroke_len):

        assert flag_bits[idx] == 100 or flag_bits[idx] == 101

        adja_matr[idx][idx] = 0

        if (flag_bits[idx - 1] == 101):
            adja_matr[idx][idx - 1] = 0

        if (idx == stroke_len - 1):
            break

        
        if (idx <= (stroke_len - 2)) and (flag_bits[idx] == 101):
            adja_matr[idx][idx + 1] = 0


    return adja_matr




def generate_padding_mask(stroke_length):
    padding_mask = np.ones([100, 1], int)
    padding_mask[stroke_length: , : ] = 0
    return padding_mask



class Quickdraw414k4MultigraphTransformer(data.Dataset):

    def __init__(self, coordinate_path_root, sketch_list, data_dict):
        with open(sketch_list) as sketch_url_file:
            sketch_url_list = sketch_url_file.readlines()
            
        self.coordinate_urls = [os.path.join(coordinate_path_root, (sketch_url.strip(
        ).split(' ')[0]).replace('png', 'npy')) for sketch_url in sketch_url_list]
        
        self.labels = [int(sketch_url.strip().split(' ')[-1])
                       for sketch_url in sketch_url_list]

        self.data_dict = data_dict
        

    def __len__(self):
        return len(self.coordinate_urls)

    def __getitem__(self, item):
        
        
        coordinate_url = self.coordinate_urls[item]
        label = self.labels[item]
        
        
        coordinate, flag_bits, stroke_len = self.data_dict[coordinate_url]
        
        attention_mask_2_neighbors = produce_adjacent_matrix_2_neighbors(flag_bits, stroke_len)

        attention_mask_4_neighbors = produce_adjacent_matrix_4_neighbors(flag_bits, stroke_len)

        attention_mask_joint_neighbors = produce_adjacent_matrix_joint_neighbors(flag_bits, stroke_len)

        padding_mask = generate_padding_mask(stroke_len)

        position_encoding = np.arange(100)
        position_encoding.resize([100, 1])

        if coordinate.dtype == 'object':
            coordinate = coordinate[0]
        
        assert coordinate.shape == (100, 2)
        
        coordinate = coordinate.astype('float32') 
        
        return (coordinate, label, flag_bits.astype('int'), stroke_len, attention_mask_2_neighbors, attention_mask_4_neighbors, attention_mask_joint_neighbors, padding_mask, position_encoding)

    
