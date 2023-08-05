# MIT License

# PointCNN
# Copyright (c) 2018 Shandong University
# Copyright (c) 2018 Yangyan Li, Rui Bu, Mingchao Sun, Baoquan Chen

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from torch.utils.data import DataLoader, Dataset, SubsetRandomSampler
import torch.nn.functional as F
import torch
import numpy as np
from fastai.data_block import DataBunch
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path
import json
import types
import random
import arcgis
import os
import math
from fastai.data_block import ItemList
try:
    from fastprogress import master_bar, progress_bar
except ImportError:
    from fastprogress.fastprogress import master_bar, progress_bar
import glob
import importlib
import random
import sys
import warnings

def try_imports(list_of_modules):
    ## Not a generic function.
    try:
        for module in list_of_modules:
            importlib.import_module(module)
    except Exception as e:
        raise Exception(f"This function requires {' '.join(list_of_modules)}. Install plotly and h5py using 'conda install -c plotly plotly=4.5.0 plotly-orca psutil h5py=2.10.0'. Install laspy using 'pip install laspy==1.6.0'")

def try_import(module):
    try:
        importlib.import_module(module)
    except ModuleNotFoundError:
        if module == 'plotly':
            raise Exception("This function requires plotly. Install it using 'conda install -c plotly plotly=4.5.0 plotly-orca psutil'")
        elif module == 'laspy':
            raise Exception("This function requires laspy. Install it using 'pip install laspy==1.6.0'")
        elif module == 'h5py':
            raise Exception(f"This function requires h5py. Install it using 'conda install h5py=2.10.0'")
        else:
            raise Exception(f"This function requires {module}. Please install it in your environment.")

def pad_tensor(cur_tensor, max_points, to_float=True):
    cur_points = cur_tensor.shape[0]
    if cur_points < max_points:
        remaining_points = max_points - cur_points
        if len(cur_tensor.shape) < 2:
            remaining_tensor = torch.zeros(remaining_points)
        else:
            remaining_tensor = torch.zeros(remaining_points, cur_tensor.shape[1])
        if to_float:
            remaining_tensor = remaining_tensor.float()
        else:
            remaining_tensor = remaining_tensor.long()
        cur_tensor = torch.cat((cur_tensor, remaining_tensor), dim=0)
    else:
        cur_tensor = cur_tensor[:max_points]
        cur_points = max_points 
    return cur_tensor, cur_points

def concatenate_tensors(read_file, input_keys, tile, max_points):
    cat_tensor = []
    
    cur_tensor = torch.tensor(read_file['xyz'][tile[1]:tile[1]+tile[2]].astype(np.float32))
    if len(cur_tensor.shape) < 2:
        cur_tensor = cur_tensor[:, None]

    cur_tensor, cur_points = pad_tensor(cur_tensor, max_points)
    cat_tensor.append(cur_tensor)
    
    for key, min_max in input_keys.items():
        if key not in ['xyz']:
            cur_tensor = torch.tensor(read_file[key][tile[1]:tile[1]+tile[2]].astype(np.float32))
            if len(cur_tensor.shape) < 2:
                cur_tensor = cur_tensor[:, None]

            cur_tensor = cur_tensor = cur_tensor / min_max['max']  ## Test with actual minmax scale and one_hot
            cur_tensor, cur_points = pad_tensor(cur_tensor, max_points)
            cat_tensor.append(cur_tensor)
    
    return torch.cat(cat_tensor, dim=1), cur_points

class PointCloudDataset(Dataset):
    def __init__(self, path, max_point, extra_dim, class_mapping, **kwargs):
        try_import("h5py")
        import h5py
        self.init_kwargs = kwargs
        self.path = Path(path)
        self.max_point = max_point  ## maximum number of points
        
        with open(self.path / 'Statistics.json', 'r') as f:
            self.statistics = json.load(f)        
        
        self.input_keys = self.statistics['features']  ## Keys to include in training
        self.classification_key = 'classification'     ## Key which contain labels
        self.extra_dim = extra_dim
        self.total_dim = 3 + extra_dim
        
        if class_mapping is None:
            self.class_mapping =  {value['classCode']:idx for idx,value in enumerate(self.statistics['classification']['table'])}
        else:
            self.class_mapping = class_mapping
        ## Helper attributes for remapping
        self.c = len(self.class_mapping)
        self.color_mapping = kwargs.get('color_mapping', np.array([np.random.randint(0, 255, 3) for i in range(self.c)])/255)
        self.remap = False
        for k,v in self.class_mapping.items():
            if k!=v:
                self.remap = True
                break
        
        self.classes = list(self.class_mapping.values())

        with h5py.File(self.path / 'ListTable.h5', 'r') as f:
            files = f['Files'][:]
            self.tiles = f['Tiles'][:]
        
        self.filenames = [self.path / file.decode() for file in files]
        self.h5files = [(h5py.File(filename, 'r')) for filename in self.filenames]
    
    def __len__(self):
        return len(self.tiles)
    
    def __getitem__(self, i):
        
        tile = self.tiles[i]        
        read_file = self.h5files[tile[0]]
        classification, _ = pad_tensor(torch.tensor(read_file[self.classification_key][tile[1]:tile[1]+tile[2]].astype(int)),
                                       self.max_point,
                                       to_float=False
                                      )
     
        if not self.remap:
            return concatenate_tensors(read_file, self.input_keys, tile, self.max_point), classification
        else:
            raise NotImplementedError
        
    def close(self):
        [file.close() for file in self.h5files]

def minmax_scale(pc):
    min_val = np.amin(pc, axis=0)
    max_val = np.amax(pc, axis=0)
    return (pc - min_val[None])/max(max_val - min_val)

def show_point_cloud_batch(self, rows=2, figsize=(6,12), color_mapping=None):
    rows = min(rows, self.batch_size)
    fig = plt.figure(figsize=figsize)
    color_mapping = self.color_mapping if color_mapping is None else np.array(color_mapping) / 255
    
    h5_files = self.h5files.copy()
    random.shuffle(h5_files)  

    idx = 0
    file_idx = 0
    while (idx < rows):
        file = h5_files[file_idx]
        pc = file['xyz'][:]
        labels = file['classification'][:] 
        sample_idxs = labels!=0
        sampled_pc = pc[sample_idxs]
        if sampled_pc.shape[0] == 0:
            file_idx += 1
            continue
        x, y, z = minmax_scale(sampled_pc).transpose(1,0)  ## convert to 3,N so that upacking works
        color_list =  color_mapping[labels[sample_idxs]].tolist()
        ax = fig.add_subplot(rows, 1, idx+1, projection='3d')
        ax.scatter3D(x, y, z, zdir='z', c=color_list)
        idx += 1
        file_idx += 1

def filter_pc(pc):
    mean = pc.mean(0)
    std = pc.std(0)
    mask = (pc[:, 0] < (mean[0] + 2*std[0])) & (pc[:, 1] < (mean[1] + 2*std[1])) & (pc[:, 2] < (mean[2] + 2*std[2]))
    return mask

def recenter(pc):
    min_val = np.amin(pc, axis=0)
    max_val = np.amax(pc, axis=0)
    return (pc - min_val[None])

def show_point_cloud_batch_TF(self, rows=2, color_mapping=None, **kwargs):

    """
    It will plot 3d point cloud data you exported in the notebook.

    =====================   ===========================================
    **Argument**            **Description**
    ---------------------   -------------------------------------------
    rows                    Optional rows. Number of rows to show. Deafults
                            value is 2.
    ---------------------   -------------------------------------------
    color_mapping           Optional dictionary. Mapping from class value
                            to RGB values. Default value
                            Example: {0:[220,220,220],
                                        1:[255,0,0],
                                        2:[0,255,0],
                                        3:[0,0,255]}                                                         
    =====================   ===========================================

    **kwargs**

    =====================   ===========================================
    **Argument**            **Description**
    ---------------------   -------------------------------------------
    mask_class              Optinal array of integers. Array containing
                            class values to mask. Default value is [0].    
    ---------------------   -------------------------------------------
    width                   Optional integer. Width of the plot. Default 
                            value is 750.
    ---------------------   -------------------------------------------
    height                  Optional integer. Height of the plot. Default
                            value is 512
    =====================   ===========================================
    """

    filter_outliers = False
    try_import("h5py")
    import h5py
    try_import('plotly')
    import plotly.graph_objects as go
    mask_class = kwargs.get('mask_class', [0])
    rows = min(rows, self.batch_size)
    color_mapping = np.array(list(self.color_mapping.values()) if color_mapping is None else list(self.color_mapping.values())) / 255

    idx = 0
    import random
    keys = list(self.meta['files'].keys()).copy()
    random.shuffle(keys)
    
    for fn in keys:
        num_files = self.meta['files'][fn]['idxs']
        block_center = self.meta['files'][fn]['block_center']
        block_center = np.array(block_center)
        block_center[0][2], block_center[0][1] = block_center[0][1], block_center[0][2]
        if num_files == []:
            continue
        idxs = [h5py.File(fn[:-3] + f'_{i}.h5', 'r') for i in num_files]
        pc = []
        labels = []
        for i in idxs:
            current_block = i['unnormalized_data'][:, :3]
            data_num = i['data_num'][()]   
            pc.append(current_block[:data_num])
            labels.append(i['label_seg'][:data_num])  
            
        if pc == []:
            continue         
       
        pc = np.concatenate(pc, axis=0)
        labels = np.concatenate(labels, axis=0)          
        sample_idxs = np.concatenate([(labels[None]!=mask) for mask in mask_class])
        sample_idxs = sample_idxs.all(axis=0)
        sampled_pc = pc[sample_idxs]
        if sampled_pc.shape[0] == 0:
            continue
        x, y, z = recenter(sampled_pc).transpose(1,0)       
        if filter_outliers:
            ## Filter on the basis of std.
            mask = filter_pc(pc)
        else:
            ## all points
            mask = x > -9999999
            
        color_list =  color_mapping[labels[sample_idxs]][mask].tolist()
        
        scene=dict(aspectmode='data')
        layout = go.Layout(
            width=kwargs.get('width', 750),
            height=kwargs.get('height', 512),
            scene = scene)

        figww = go.Figure(data=[go.Scatter3d(x=x[mask], y=z[mask], z=y[mask], 
                                        mode='markers', marker=dict(size=1, color=color_list))], layout=layout)
        figww.show()

        if idx == rows-1:
            break
        idx += 1

def get_device():
    if getattr(arcgis.env, "_processorType", "") == "GPU" and torch.cuda.is_available():
        device = torch.device("cuda")
    elif getattr(arcgis.env, "_processorType", "") == "CPU":
        device = torch.device("cpu")
    else:
        device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    return device    

def read_xyzinumr_label_from_las(filename_las, extra_features):
    try_import('laspy')
    import laspy
    file = laspy.file.File(filename_las, mode='r')    
    h = file.header
    xyzirgb_num = h.point_records_count
    labels = file.Classification
    
    xyz = np.concatenate([file.x[:, None], file.y[:, None], file.z[:, None]] + [(np.clip(getattr(file, f[0]), None, f[1])[:, None] - f[2])/ (f[1] - f[2]) for f in extra_features],
                         axis=1)
    
    xyzirgb_num = len(xyz)
    return xyz, labels, xyzirgb_num

def prepare_las_data(root,
                       block_size,
                       max_point_num,
                       output_path,
                       extra_features=[('intensity', 5000, 0), ('num_returns', 5, 0)],
                       grid_size=1.0,
                       blocks_per_file=2048,
                       folder_names=['train', 'val'],
                       segregate=True,
                       **kwargs
                       ):
    try_import("h5py")
    import h5py
    block_size_ = block_size
    batch_size= blocks_per_file
    data = np.zeros((batch_size, max_point_num, 3 + len(extra_features))) #XYZ, Intensity, NumReturns
    unnormalized_data = np.zeros((batch_size, max_point_num, 3 + len(extra_features)))
    data_num = np.zeros((batch_size), dtype=np.int32)
    label = np.zeros((batch_size), dtype=np.int32)
    label_seg = np.zeros((batch_size, max_point_num), dtype=np.int32)
    indices_split_to_full = np.zeros((batch_size, max_point_num), dtype=np.int32)
    LOAD_FROM_EXT = '.las'
    os.makedirs(output_path, exist_ok=True)

    if (Path(output_path) / 'meta.json').exists() or (Path(output_path) / 'Statistics.json').exists():
        raise Exception(f"The given output path({output_path}) already contains exported data. Either delete those files or pass in a new output path.")

    folders = [os.path.join(root, folder) for folder in folder_names]  ## Folders are named train and val
    mb = master_bar(range(len(folders)))
    for itn in mb:
        folder = folders[itn]
        os.makedirs(os.path.join(output_path, Path(folder).stem), exist_ok=True)
        datasets = [filename[:-4] for filename in os.listdir(folder) if filename.endswith(LOAD_FROM_EXT)]
        # mb.write(f'{itn + 1}. Exporting {Path(folder).stem} folder')
        for dataset_idx, dataset in enumerate(progress_bar(datasets, parent=mb)):
            filename_ext = os.path.join(folder, dataset + LOAD_FROM_EXT)
            if LOAD_FROM_EXT == '.las':
                xyzinumr, labels, xyz_num = read_xyzinumr_label_from_las(filename_ext, extra_features)
                xyz, other_features = np.split(xyzinumr, (3,), axis=-1)
                if len(other_features.shape) < 2:
                    other_features = other_features[:, None]
            else:
                xyz, labels, xyz_num = read_xyz_label_from_txt(filename_ext)
            
            offsets = [('zero', 0.0), ('half', block_size_ / 2)]

            for offset_name, offset in offsets:
                idx_h5 = 0
                idx = 0

                xyz_min = np.amin(xyz, axis=0, keepdims=True) - offset
                xyz_max = np.amax(xyz, axis=0, keepdims=True)
                block_size = (block_size_, block_size_, 2 * (xyz_max[0, -1] - xyz_min[0, -1]))  
                xyz_blocks = np.floor((xyz - xyz_min) / block_size).astype(np.int)

                blocks, point_block_indices, block_point_counts = np.unique(xyz_blocks, return_inverse=True,
                                                                            return_counts=True, axis=0)
                block_point_indices = np.split(np.argsort(point_block_indices), np.cumsum(block_point_counts[:-1]))

                block_to_block_idx_map = dict()
                for block_idx in range(blocks.shape[0]):
                    block = (blocks[block_idx][0], blocks[block_idx][1])
                    block_to_block_idx_map[(block[0], block[1])] = block_idx

                # merge small blocks into one of their big neighbors
                block_point_count_threshold = max_point_num / 10
                nbr_block_offsets = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (1, 1), (1, -1), (-1, -1)]
                block_merge_count = 0
                for block_idx in range(blocks.shape[0]):
                    if block_point_counts[block_idx] >= block_point_count_threshold:
                        continue

                    block = (blocks[block_idx][0], blocks[block_idx][1])
                    for x, y in nbr_block_offsets:
                        nbr_block = (block[0] + x, block[1] + y)
                        if nbr_block not in block_to_block_idx_map:
                            continue

                        nbr_block_idx = block_to_block_idx_map[nbr_block]
                        if block_point_counts[nbr_block_idx] < block_point_count_threshold:
                            continue

                        block_point_indices[nbr_block_idx] = np.concatenate(
                            [block_point_indices[nbr_block_idx], block_point_indices[block_idx]], axis=-1)
                        block_point_indices[block_idx] = np.array([], dtype=np.int)
                        block_merge_count = block_merge_count + 1
                        break

                idx_last_non_empty_block = 0
                for block_idx in reversed(range(blocks.shape[0])):
                    if block_point_indices[block_idx].shape[0] != 0:
                        idx_last_non_empty_block = block_idx
                        break

                # uniformly sample each block
                for block_idx in range(idx_last_non_empty_block + 1):
                    point_indices = block_point_indices[block_idx]
                    if point_indices.shape[0] == 0:
                        continue
                    block_points = xyz[point_indices]
                    block_min = np.amin(block_points, axis=0, keepdims=True)
                    xyz_grids = np.floor((block_points - block_min) / grid_size).astype(np.int)
                    grids, point_grid_indices, grid_point_counts = np.unique(xyz_grids, return_inverse=True,
                                                                            return_counts=True, axis=0)
                    grid_point_indices = np.split(np.argsort(point_grid_indices), np.cumsum(grid_point_counts[:-1]))
                    grid_point_count_avg = int(np.average(grid_point_counts))
                    point_indices_repeated = []
                    for grid_idx in range(grids.shape[0]):
                        point_indices_in_block = grid_point_indices[grid_idx]
                        repeat_num = math.ceil(grid_point_count_avg / point_indices_in_block.shape[0])
                        if repeat_num > 1:
                            point_indices_in_block = np.repeat(point_indices_in_block, repeat_num)
                            np.random.shuffle(point_indices_in_block)
                            point_indices_in_block = point_indices_in_block[:grid_point_count_avg]
                        point_indices_repeated.extend(list(point_indices[point_indices_in_block]))
                    block_point_indices[block_idx] = np.array(point_indices_repeated)
                    block_point_counts[block_idx] = len(point_indices_repeated)
                for block_idx in range(idx_last_non_empty_block + 1):
                    point_indices = block_point_indices[block_idx]
                    if point_indices.shape[0] == 0:
                        continue

                    block_point_num = point_indices.shape[0]
                    block_split_num = int(math.ceil(block_point_num * 1.0 / max_point_num))
                    point_num_avg = int(math.ceil(block_point_num * 1.0 / block_split_num))
                    point_nums = [point_num_avg] * block_split_num
                    point_nums[-1] = block_point_num - (point_num_avg * (block_split_num - 1))
                    starts = [0] + list(np.cumsum(point_nums))

                    np.random.shuffle(point_indices)
                    block_points = xyz[point_indices]
                    block_min = np.amin(block_points, axis=0, keepdims=True)
                    block_max = np.amax(block_points, axis=0, keepdims=True)
                    block_center = (block_min + block_max) / 2
                    block_center[0][-1] = block_min[0][-1]
                    unnormalized_block_points = block_points.copy()
                    block_points = block_points - block_center  # align to block bottom center
                    x, y, z = np.split(block_points, (1, 2), axis=-1)
        
                    block_xzyrgbi = np.concatenate([x, z, y] + [i[point_indices][:, None] for i in other_features.transpose(1,0)], axis=-1) #XYZ, Intensity, NumReturns, RGB
                    block_labels = labels[point_indices]

                    ## unormalized points
                    x_u, y_u, z_u = np.split(unnormalized_block_points, (1, 2), axis=-1)
                    unnormalized_block_xzyrgbi = np.concatenate([x_u, z_u, y_u] + [i[point_indices][:, None] for i in other_features.transpose(1,0)], axis=-1)


                    for block_split_idx in range(block_split_num):
                        start = starts[block_split_idx]
                        point_num = point_nums[block_split_idx]
                        end = start + point_num
                        idx_in_batch = idx % batch_size
                        data[idx_in_batch, 0:point_num, ...] = block_xzyrgbi[start:end, :]
                        unnormalized_data[idx_in_batch, 0:point_num, ...] = unnormalized_block_xzyrgbi[start:end, :]
                        data_num[idx_in_batch] = point_num
                        label[idx_in_batch] = dataset_idx  # won't be used...
                        label_seg[idx_in_batch, 0:point_num] = block_labels[start:end]
                        indices_split_to_full[idx_in_batch, 0:point_num] = point_indices[start:end]

                        if ((idx + 1) % batch_size == 0) or \
                                (block_idx == idx_last_non_empty_block and block_split_idx == block_split_num - 1):
                            item_num = idx_in_batch + 1
                            filename_h5 = os.path.join(output_path, Path(folder).stem, Path(dataset).stem + '_%s_%d.h5' % (offset_name, idx_h5))

                            file = h5py.File(filename_h5, 'w')
                            file.create_dataset('unnormalized_data', data=unnormalized_data[0:item_num, ...])
                            file.create_dataset('data', data=data[0:item_num, ...])
                            file.create_dataset('data_num', data=data_num[0:item_num, ...])
                            file.create_dataset('label', data=label[0:item_num, ...])
                            file.create_dataset('label_seg', data=label_seg[0:item_num, ...])
                            file.create_dataset('indices_split_to_full', data=indices_split_to_full[0:item_num, ...])
                            file.create_dataset('block_center', data=block_center)
                            file.close()
                            idx_h5 = idx_h5 + 1
                        idx = idx + 1
    if segregate:
        ## Segregate data
        output_path = Path(output_path)
        path_convert = output_path
        
        GROUND_CLASS = 0
        mb = master_bar(range(len(folders)))
        meta_file = {}
        meta_file['files'] = {}
        all_classes = set()
        for itn in mb:
            folder = folders[itn]
            path = output_path / Path(folder).stem
            total = 0
            # mb.write(f'{itn + 1}. Segregating {Path(folder).stem} folder')
            all_files = list(path.glob('*.h5'))
            file_id = 0
            for idx, fn in enumerate(progress_bar(all_files, parent=mb)):
                file = h5py.File(fn, 'r')
                data = file['data']
                total += data.shape[0]
                label_seg = file['label_seg']
                data_num = file['data_num']
                unnormalized_data = file['unnormalized_data']
                block_center = file['block_center'][:]
                file_idxs = []
                for i in range(file['data_num'][:].shape[0]):
                    if not ((label_seg[i] != GROUND_CLASS).sum().tolist() == 0):
                        save_file = path_convert / Path(folder).stem /  (fn.stem + f'_{i}' + '.h5')
                        new_file = h5py.File(save_file, mode='w')
                        new_file.create_dataset('unnormalized_data', data=unnormalized_data[i])
                        new_file.create_dataset('data', data=data[i])
                        new_file.create_dataset('label_seg', data=label_seg[i])
                        new_file.create_dataset('data_num', data=data_num[i])
                        new_file.close()
                        all_classes = all_classes.union(np.unique(label_seg[i]).tolist())
                        file_idxs.append(i)
                meta_file['files'][str(fn)] = {'idxs':file_idxs,
                                                'block_center':block_center.tolist()}
                file.close()
                os.remove(fn)
        meta_file['num_classes'] = len(all_classes)
        meta_file['classes'] = list(all_classes)
        meta_file['max_point'] = max_point_num
        meta_file['num_extra_dim'] = len(extra_features)
        meta_file['extra_features'] = extra_features
        meta_file['block_size'] = block_size
        with open(output_path / 'meta.json', 'w') as f:
            json.dump(meta_file, f)

    if kwargs.get('print_it', True):
        print('Export finished.')

    return output_path

## Segregated data ItemList

def open_h5py_tensor(fn, keys=['data']):
    try_import("h5py")
    import h5py
    data_label = []
    file = h5py.File(fn, 'r')
    for key in keys:
        tensor = torch.tensor(file[key][...]).float()
        data_label.append(tensor)

    file.close()    
    return data_label ## While getting a specific index from the file
    
## It also stores the label so that we don't have to open the file twice.
class DataStore():
    pass
    
class PointCloudItemList(ItemList):
    def __init__(self, items, **kwargs):
        super().__init__(items, **kwargs)
        
        self.keys = ['data', 'label_seg', 'data_num']
        
    def get(self, i):
        data = self.open(self.items[i])
        DataStore.i = i
        DataStore.data = data
        return (data[0], data[2])
        
    def open(self, fn):
        return open_h5py_tensor(fn, keys=self.keys)
    
class PointCloudLabelList(ItemList):
    def __init__(self, items, **kwargs):
        super().__init__(items, **kwargs)
        self.key = 'label_seg'
        
    def get(self, i):
        return DataStore.data[1].long()
    
    
    def analyze_pred(self, pred):
        return pred.argmax(dim=1)
        
PointCloudItemList._label_cls = PointCloudLabelList


## Prepare data called in _data.py

def pointcloud_prepare_data(path, class_mapping, batch_size, val_split_pct, dataset_type='PointCloud', **kwargs):
    try_imports(['h5py', 'plotly', 'laspy'])
    databunch_kwargs = {'num_workers':0} if sys.platform == 'win32' else {}
    if (path / 'Statistics.json').exists():
        dataset_type = "PointCloud"
    else:
        dataset_type = "PointCloud_TF"

    if dataset_type == 'PointCloud':
        with open(path / 'Statistics.json') as f:
            json_file = json.load(f)

        max_points = json_file['parameters']['numberOfPointsInEachTile']
        ## It is assumed that the pointcloud will have only X,Y & Z.
        extra_dim = sum([len(v['max']) if isinstance(v['max'], list) else 1 for k,v in json_file['features'].items()]) - 3
        pointcloud_dataset = PointCloudDataset(path, max_points, extra_dim, class_mapping, **kwargs)

        # Reconsider shuffling method
        # val_num_files = int(val_pct * len(data.h5files))
        # all_indices = list(range(len(data.h5files)))
        # np.random.shuffle(all_indices)
        # valid_file_indices = all_indices[:val_num_files]
        # train_file_indices = all_indices[val_num_files:]
        # valid_indices = [*point_dataset.tiles[point_dataset.tiles == i] for i in valid_file_indices]
        # train_indices = [*point_dataset.tiles[point_dataset.tiles == i] for i in train_file_indices]

        ## Better than random shuffling because this will cause less spill of data in training and testing.
        train_indices = torch.arange(int(len(pointcloud_dataset) * (1-val_split_pct)))
        val_indices = torch.arange(train_indices[-1], len(pointcloud_dataset))
        train_sampler = SubsetRandomSampler(train_indices)
        val_sampler = SubsetRandomSampler(val_indices)

        train_dl = DataLoader(pointcloud_dataset, batch_size=batch_size, sampler=train_sampler, **databunch_kwargs)
        valid_dl = DataLoader(pointcloud_dataset, batch_size=batch_size, sampler=val_sampler, **databunch_kwargs)
        device = get_device()
        data = DataBunch(train_dl, valid_dl, device=device)
        data.show_batch = types.MethodType(show_point_cloud_batch, data)
        data.path = data.train_ds.path

    elif dataset_type == 'PointCloud_TF':
        src = PointCloudItemList.from_folder(path, ['.h5'])
        train_idxs = [i for i,p in enumerate(src.items) if p.parent.name == 'train']
        val_idxs = [i for i,p in enumerate(src.items) if p.parent.name == 'val']
        src = src.split_by_idxs(train_idxs, val_idxs)\
            .label_from_func(lambda x: x)
        data = src.databunch(bs=batch_size, **databunch_kwargs)
        with open(Path(path) / 'meta.json', 'r') as f:
            data.meta = json.load(f)
        data.c = data.meta['num_classes']
        data.show_batch = types.MethodType(show_point_cloud_batch_TF, data)
        data.classes =  data.meta['classes']
        data.color_mapping = kwargs.get('color_mapping', {i:[random.choice(range(256)) for _ in range(3)]  for i in range(data.c)})
        data.color_mapping = {int(k):v for k, v in data.color_mapping.items()}
        data.class_mapping = class_mapping if class_mapping is not None else {v:k for k,v in enumerate(data.classes)}
        data.max_point = data.meta['max_point']
        data.extra_dim = data.meta['num_extra_dim']
        data.extra_features = data.meta['extra_features']
        data.block_size = data.meta['block_size']
        ## To accomodate save function to save in correct directory
        data.path = data.path / 'train' 
    else:
        raise Exception("Could not infer dataset type.")

    data.path = data.train_ds.path
    ## Below are the lines to make save function work
    data.chip_size = None
    data._image_space_used = None
    data.dataset_type = dataset_type
    return data

def read_xyz_label_from_las(filename_las):
    try_import('laspy')
    import laspy
    msg = 'Loading {}...'.format(filename_las)
    f = laspy.file.File(filename_las, mode='r')    
    h = f.header
    xyzirgb_num = h.point_records_count
    xyz_offset = h.offset
    encoding = h.encoding
    xyz = np.ndarray((xyzirgb_num, 3))
    labels = np.ndarray(xyzirgb_num, np.int16)
    i = 0
    for p in f:
        xyz[i] = [p.x, p.y, p.z]
        labels[i] = p.classification
        i += 1
    return xyz, labels, xyzirgb_num, xyz_offset, encoding

def save_xyz_label_to_las(filename_las, xyz, xyz_offset, encoding, labels):  
    try_import('laspy')
    import laspy
    msg = 'Saving {}...'.format(filename_las)
    h = laspy.header.Header()
    h.dataformat_id = 1
    h.major = 1
    h.minor = 2
    h.min = np.min(xyz, axis=0)
    h.max = np.max(xyz, axis=0)
    h.scale = [1e-3, 1e-3, 1e-3]
    h.offset = xyz_offset
    h.encoding = encoding
    
    f = laspy.file.File(filename_las, mode='w', header=h)    
    for i in range(xyz.shape[0]):
        p = laspy.point.Point()
        p.x = xyz[i,0] / h.scale[0]
        p.y = xyz[i,1] / h.scale[1]
        p.z = xyz[i,2] / h.scale[2]
        p.classification = labels[i]
        p.color = laspy.color.Color()
        p.intensity = 100
        p.return_number = 1
        p.number_of_returns = 1
        p.scan_direction = 1
        p.scan_angle = 0
        f.write(p)
        
    f.close()


def write_resulting_las(in_las_filename, out_las_filename, labels, num_classes):
    try_import('laspy')
    import laspy
    false_positives = [0] * num_classes
    true_positives = [0] * num_classes
    false_negatives = [0] * num_classes
    f = laspy.file.File(in_las_filename, mode='r')    
    h = f.header
    f_out = laspy.file.File(out_las_filename, mode='w', header=h)
    i = 0
    x = []
    y = []
    z = []
    classification = []
    for p in f:
        p = f[i]
        try:
            false_positives[labels[i]] += int(p.classification != labels[i])
            true_positives[labels[i]] += int(p.classification == labels[i])
            false_negatives[p.classification] += int(p.classification != labels[i])
        except:
            pass

        x.append(p.X)
        y.append(p.Y)
        z.append(p.Z)
        classification.append(labels[i])
        i += 1
    f.close()
    f_out.X = x
    f_out.Y = y
    f_out.Z = z
    f_out.classification = classification
    f_out.close()
    
    return false_positives, true_positives, false_negatives

def calculate_metrics(false_positives, true_positives, false_negatives):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        precision = np.divide(true_positives, np.add(true_positives, false_positives))
        recall = np.divide(true_positives, np.add(true_positives, false_negatives))
        f_1 = np.multiply(2.0, np.divide(np.multiply(precision, recall), np.add(precision, recall)))
    return precision, recall, f_1

def get_pred_prefixes(datafolder):
    fs = os.listdir(datafolder)
    preds = []
    for f in fs:
        if f[-8:] == '_pred.h5':
            preds += [f]
    pred_pfx = []
    for p in preds:
        to_check = "_half" #"_zero"
        if to_check in p: 
            pred_pfx += [p.split(to_check)[0]]
    return np.unique(pred_pfx)

def get_predictions(pointcnn_model, data, batch_idx, points_batch, sample_num, batch_size, point_num):
    ## Getting sampling indices
    tile_num = math.ceil((sample_num * batch_size) / point_num)
    indices_shuffle = np.tile(np.arange(point_num), tile_num)[0:sample_num * batch_size]
    np.random.shuffle(indices_shuffle)
    indices_batch_shuffle = np.reshape(indices_shuffle, (batch_size, sample_num, 1))

    model_input = np.concatenate([points_batch[i, s[:, 0]][None] for i, s in enumerate(indices_batch_shuffle)], axis=0)
    
    ## Putting model in evaluation mode and inferencing.
    pointcnn_model.learn.model.eval()
    with torch.no_grad():
        probs = pointcnn_model.learn.model(torch.tensor(model_input).to(pointcnn_model._device).float()).softmax(dim=-1).cpu()
        
    seg_probs = probs.numpy()
    
    probs_2d = np.reshape(seg_probs, (sample_num * batch_size, -1))  ## Complete probs
    predictions = [(-1, 0.0)] * point_num  ## predictions
    
    ## Assigning the confidences and labels to the appropriate index.
    for idx in range(sample_num * batch_size):
        point_idx = indices_shuffle[idx]
        probs = probs_2d[idx, :]
        confidence = np.amax(probs)
        label = np.argmax(probs)
        if confidence > predictions[point_idx][1]:
            predictions[point_idx] = [label, confidence]
        
    return predictions

def inference_las(path, pointcnn_model, out_path=None, print_metrics=False):
    try_import("h5py")
    import h5py    
    ## Export data
    path = Path(path)

    if len(list(path.glob('*.las'))) == 0:
        raise Exception(f"The given path({path}) contains no las files.")

    if out_path is None:
        out_path = path / 'results'
    else:    
        out_path = Path(out_path)
        
    prepare_las_data(path.parent,
                     block_size=pointcnn_model._data.block_size[0],
                     max_point_num=pointcnn_model._data.max_point,
                     output_path=path.parent,
                     extra_features=pointcnn_model._data.extra_features,
                     folder_names=[path.stem],
                     segregate=False,
                     print_it=False
    )
    ## Predict and postprocess
    max_point_num = pointcnn_model._data.max_point
    sample_num = pointcnn_model.sample_point_num
    batch_size = 1 * math.ceil(max_point_num / sample_num) 
    filenames = list(glob.glob(str(path/ "*.h5")))

    mb = master_bar(range(len(filenames)))
    for itn in mb:  
        filename = filenames[itn]
        data_h5 = h5py.File(filename, 'r')
        data = data_h5['data'][...].astype(np.float32)  
        data_num =  data_h5['data_num'][...].astype(np.int32)
        batch_num = data.shape[0]
        labels_pred = np.full((batch_num, max_point_num), -1, dtype=np.int32)
        confidences_pred = np.zeros((batch_num, max_point_num), dtype=np.float32)


        for batch_idx in progress_bar(range(batch_num), parent=mb): 
            points_batch = data[[batch_idx] * batch_size, ...]
            point_num = data_num[batch_idx]
            predictions = get_predictions(pointcnn_model, data, batch_idx, points_batch, sample_num, batch_size, point_num)      
            labels_pred[batch_idx, 0:point_num] = np.array([label for label, _ in predictions])
            confidences_pred[batch_idx, 0:point_num] = np.array([confidence for _, confidence in predictions])

        ## Saving h5 predictions file
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        filename_pred = os.path.join(out_path , Path(filename).stem + '_pred.h5')
        file = h5py.File(filename_pred, 'w')
        file.create_dataset('data_num', data=data_num)
        file.create_dataset('label_seg', data=labels_pred)
        file.create_dataset('confidence', data=confidences_pred)
        has_indices = 'indices_split_to_full' in data_h5
        if has_indices:
            file.create_dataset('indices_split_to_full', data=data_h5['indices_split_to_full'][...])
        file.close()
        data_h5.close()


    ## Merge H5 files and write las files
    SAVE_TO_EXT = '.las'
    LOAD_FROM_EXT = '.las'


    categories_list = get_pred_prefixes(out_path)

    global_false_positives = [0] * pointcnn_model._data.c
    global_true_positives = [0] * pointcnn_model._data.c
    global_false_negatives = [0] * pointcnn_model._data.c

    for category in categories_list:
        output_path = os.path.join(out_path ,category + "_pred" + SAVE_TO_EXT)
        if not os.path.exists(os.path.join(out_path)):
            os.makedirs(os.path.join(out_path))
        pred_list = [pred for pred in os.listdir(out_path)
                    if category in pred and pred.split(".")[0].split("_")[-1] == 'pred' and pred[-3:] != 'las']

        merged_label = None
        merged_confidence = None

        for pred_file in pred_list:
            data = h5py.File(os.path.join(out_path, pred_file), mode='r')
            labels_seg = data['label_seg'][...].astype(np.int64)
            indices = data['indices_split_to_full'][...].astype(np.int64)
            confidence = data['confidence'][...].astype(np.float32)
            data_num = data['data_num'][...].astype(np.int64)

            if merged_label is None:
                # calculating how many labels need to be there in the output
                label_length = 0
                for i in range(indices.shape[0]):
                    label_length = np.max([label_length, np.max(indices[i][:data_num[i]])])
                label_length += 1
                merged_label = np.zeros((label_length), dtype=int)
                merged_confidence = np.zeros((label_length), dtype=float)
            else:
                label_length2 = 0
                for i in range(indices.shape[0]):
                    label_length2 = np.max([label_length2, np.max(indices[i][:data_num[i]])])
                label_length2 += 1
                if label_length < label_length2:
                    # expanding labels and confidence arrays, as the new file appears having mode of them
                    for i in range(label_length2 - label_length):
                        merged_label = np.append(merged_label, 0)
                        merged_confidence = np.append(merged_confidence, 0.0)
                    label_length = label_length2
            
            for i in range(labels_seg.shape[0]):
                temp_label = np.zeros((data_num[i]),dtype=int)
                pred_confidence = confidence[i][:data_num[i]]
                temp_confidence = merged_confidence[indices[i][:data_num[i]]]

                temp_label[temp_confidence >= pred_confidence] = merged_label[indices[i][:data_num[i]]][temp_confidence >= pred_confidence]
                temp_label[pred_confidence > temp_confidence] = labels_seg[i][:data_num[i]][pred_confidence > temp_confidence]

                merged_confidence[indices[i][:data_num[i]][pred_confidence > temp_confidence]] = pred_confidence[pred_confidence > temp_confidence]
                merged_label[indices[i][:data_num[i]]] = temp_label

            data.close()

        if len(pred_list) > 0:
            # concatenating source points with the final labels and writing out resulting file
            points_path = os.path.join(path, category + LOAD_FROM_EXT)
            
            false_positives, true_positives, false_negatives = write_resulting_las(points_path,
                                                                                   output_path,
                                                                                   merged_label,
                                                                                   pointcnn_model._data.c)
            global_false_positives = np.add(global_false_positives, false_positives)
            global_true_positives = np.add(global_true_positives, true_positives)
            global_false_negatives = np.add(global_false_negatives, false_negatives)
    if print_metrics: 
        print('Overal per-class-metrics: \nPrecision:{}, \nRecall:   {}, \nF1 score: {}'.format(
        *calculate_metrics(global_false_positives, global_true_positives, global_false_negatives)))


    for fn in glob.glob(str(path / '*.h5'), recursive=True): ## Remove h5 files in val directory.
        os.remove(fn) 

    for fn in glob.glob(str(out_path / '*.h5'), recursive=True):  ## Remove h5 files in results directory.
        os.remove(fn)        

    return out_path

def show_results(self, rows, color_mapping=None, **kwargs):

    """
    It will plot results from your trained model with ground truth on the
    left and predictions on the right.

    =====================   ===========================================
    **Argument**            **Description**
    ---------------------   -------------------------------------------
    rows                    Optional rows. Number of rows to show. Deafults
                            value is 2.
    ---------------------   -------------------------------------------
    color_mapping           Optional dictionary. Mapping from class value
                            to RGB values. Default value
                            Example: {0:[220,220,220],
                                        1:[255,0,0],
                                        2:[0,255,0],
                                        3:[0,0,255]}                                                         
    =====================   ===========================================

    **kwargs**

    =====================   ===========================================
    **Argument**            **Description**
    ---------------------   -------------------------------------------
    mask_class              Optinal array of integers. Array containing
                            class values to mask. Default value is [0].    
    ---------------------   -------------------------------------------
    width                   Optional integer. Width of the plot. Default 
                            value is 750.
    ---------------------   -------------------------------------------
    height                  Optional integer. Height of the plot. Default
                            value is 512
    =====================   ===========================================
    """
    
    filter_outliers = False
    try_import("h5py")
    try_import('plotly')
    import h5py    
    import plotly
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots    
    import random
    mask_class = kwargs.get('mask_class', [0])    
    save_html = kwargs.get('save_html', False)
    save_path = kwargs.get('save_path', False)

    rows = min(rows, self._data.batch_size)
    color_mapping = np.array(list(self._data.color_mapping.values()) if color_mapping is None else list(self._data.color_mapping.values())) / 255

    idx = 0
    keys = list(self._data.meta['files'].keys()).copy()
    keys = [f for f in keys if Path(f).parent.stem == 'val']
    random.shuffle(keys)

    for fn in keys:        
        fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'scene'}, {'type': 'scene'}]])        

        num_files = self._data.meta['files'][fn]['idxs']
        block_center = self._data.meta['files'][fn]['block_center']
        block_center = np.array(block_center)
        block_center[0][2], block_center[0][1] = block_center[0][1], block_center[0][2]
        if num_files == []:
            continue
        idxs = [h5py.File(fn[:-3] + f'_{i}.h5', 'r') for i in num_files]
        pc = []
        labels = []
        pred_class = []
        pred_confidence = []
        for i in idxs:
            # print(f'Running Show Results: Processing {nn+1} of {len(idxs)} blocks.', end='\r')
            current_block = i['unnormalized_data'][:, :3]
            data_num = i['data_num'][()] 
            data = i['data'][:] 
            pc.append(current_block[:data_num])
            labels.append(i['label_seg'][:data_num])

            max_point_num = self._data.max_point
            sample_num = self.sample_point_num
            batch_size = 1 * math.ceil(max_point_num / sample_num) 
            data = data[None]
            batch_idx = 0
            points_batch = data[[batch_idx] * batch_size, ...]
            point_num = data_num
            predictions = np.array(get_predictions(self, data, batch_idx, points_batch, sample_num, batch_size, point_num))
            pred_class.append(predictions[:, 0])
            pred_confidence.append(predictions[:, 1])
            
        if pc == []:
            continue         
                
        pc = np.concatenate(pc, axis=0)
        labels = np.concatenate(labels, axis=0)
        pred_class = np.concatenate(pred_class, axis=0).astype(int)
        sample_idxs = np.concatenate([(labels[None]!=mask) for mask in mask_class])
        sample_idxs = sample_idxs.all(axis=0)
        sampled_pc = pc[sample_idxs]
        if sampled_pc.shape[0] == 0:
            continue
        x, y, z = recenter(sampled_pc).transpose(1,0)       
        if filter_outliers:
            ## Filter on the basis of std.
            mask = filter_pc(pc)
        else:
            ## all points
            mask = x > -9999999
        
        color_list_true =  color_mapping[labels[sample_idxs]][mask].tolist()
        color_list_pred = color_mapping[pred_class[sample_idxs]][mask].tolist()
        
        scene=dict(aspectmode='data')


        fig.add_trace(go.Scatter3d(x=x[mask], y=z[mask], z=y[mask], 
                                        mode='markers', marker=dict(size=1, color=color_list_true)), row=1, col=1)

        fig.add_trace(go.Scatter3d(x=x[mask], y=z[mask], z=y[mask], 
                                mode='markers', marker=dict(size=1, color=color_list_pred)), row=1, col=2)


        fig.update_layout(
            scene=scene,
            scene2=scene,
            title_text='Ground Truth / Predictions' if idx==0 else '',
            width=kwargs.get('width', 750),
            height=kwargs.get('width', 512),
            showlegend=False,
            title_x=0.5
        )

        if save_html:
            save_path = Path(save_path)
            plotly.io.write_html(fig, str(save_path / 'show_results.html'))
            fig.write_image(str(save_path / 'show_results.png'))
            return
        else:
            fig.show()

        if idx == rows-1:
            break
        idx += 1

def compute_precision_recall(self):
    from ..models._pointcnn_utils import get_indices
    import pandas as pd 

    valid_dl = self._data.valid_dl
    model = self.learn.model.eval()

    false_positives = [0] * self._data.c
    true_positives = [0] * self._data.c
    false_negatives = [0] * self._data.c

    all_y = []
    all_pred = []
    for x_in, y_in in iter(valid_dl):
        x_in, point_nums = x_in   ## (batch, total_points, num_features), (batch,)
        batch, _, num_features = x_in.shape
        indices = torch.tensor(get_indices(batch, self.sample_point_num, point_nums.long())).to(x_in.device)
        indices = indices.view(-1, 2).long()
        x_in = x_in[indices[:, 0], indices[:, 1]].view(batch, self.sample_point_num, num_features).contiguous()  ## batch, self.sample_point_num, num_features                
        y_in = y_in[indices[:, 0], indices[:, 1]].view(batch, self.sample_point_num).contiguous().cpu().numpy() ## batch, self.sample_point_num        
        with torch.no_grad():
            preds = model(x_in).detach().cpu().numpy()
        predicted_labels = preds.argmax(axis=-1)
        all_y.append(y_in.reshape(-1))
        all_pred.append(predicted_labels.reshape(-1))

    all_y = np.concatenate(all_y)
    all_pred = np.concatenate(all_pred)
    
    for i in range(len(all_y)):        
        false_positives[all_pred[i]] += int(all_y[i] != all_pred[i])
        true_positives[all_pred[i]] += int(all_y[i] == all_pred[i])
        false_negatives[all_y[i]] += int(all_y[i] != all_pred[i])        
    
    
    precision, recall, f_1 = calculate_metrics(false_positives, true_positives, false_negatives)
    data = [precision, recall, f_1]
    index = ['precision', 'recall', 'f_1 score']
    df = pd.DataFrame(data, columns=list(range(self._data.c)), index=index) 
    return df
