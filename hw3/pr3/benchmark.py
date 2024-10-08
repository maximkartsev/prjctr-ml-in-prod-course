import time
import pandas as pd
import numpy as np
import pyarrow.feather as feather
import pyarrow.parquet as pq
import h5py
import netCDF4 as nc
import networkx as nx
import xarray as xr
from pandas import json_normalize
import json
import igraph as ig

# Sample DataFrame for benchmarking
df = pd.DataFrame(np.random.rand(100000, 10), columns=[f'col_{i}' for i in range(10)])


# Benchmark function
def benchmark_format(save_func, load_func, file_path):
    start_time = time.time()
    save_func(df, file_path)
    save_time = time.time() - start_time

    start_time = time.time()
    loaded_df = load_func(file_path)
    load_time = time.time() - start_time

    return save_time, load_time


# Define save and load functions for each format

def save_csv(df, file_path):
    df.to_csv(file_path, index=False)


def load_csv(file_path):
    return pd.read_csv(file_path)


def save_pickle(df, file_path):
    df.to_pickle(file_path)


def load_pickle(file_path):
    return pd.read_pickle(file_path)


def save_feather(df, file_path):
    feather.write_feather(df, file_path)


def load_feather(file_path):
    return feather.read_feather(file_path)


def save_parquet(df, file_path):
    df.to_parquet(file_path)


def load_parquet(file_path):
    return pd.read_parquet(file_path)


def save_npy(df, file_path):
    np.save(file_path, df.values)


def load_npy(file_path):
    return pd.DataFrame(np.load(file_path), columns=df.columns)


def save_hdf(df, file_path):
    df.to_hdf(file_path, key='df', mode='w')


def load_hdf(file_path):
    return pd.read_hdf(file_path, 'df')


def save_netcdf(df, file_path):
    df.to_xarray().to_netcdf(file_path)


def load_netcdf(file_path):
    return xr.open_dataset(file_path).to_dataframe()


def save_json(df, file_path):
    df.to_json(file_path, orient='records', lines=True)


def load_json(file_path):
    return pd.read_json(file_path, orient='records', lines=True)


def save_excel(df, file_path):
    df.to_excel(file_path, index=False)


def load_excel(file_path):
    return pd.read_excel(file_path)


def save_graph(df, file_path):
    edges = [(int(row['col_0']), int(row['col_1'])) for _, row in df.iterrows()]
    G = ig.Graph(edges=edges)
    G.write_pickle(file_path)

def load_graph(file_path):
    return ig.Graph.Read_Pickle(file_path)


# Benchmark each format
formats = {
    'CSV': ('/app/output/data.csv', save_csv, load_csv),
    'Pickle': ('/app/output/data.pkl', save_pickle, load_pickle),
    'Feather': ('/app/output/data.feather', save_feather, load_feather),
    'Parquet': ('/app/output/data.parquet', save_parquet, load_parquet),
    'npy': ('/app/output/data.npy', save_npy, load_npy),
    'HDF5': ('/app/output/data.h5', save_hdf, load_hdf),
    'NetCDF4': ('/app/output/data.nc', save_netcdf, load_netcdf),
    'JSON': ('/app/output/data.json', save_json, load_json),
    'Excel': ('/app/output/data.xlsx', save_excel, load_excel),
    'Graph': ('/app/output/data_graph.gpickle', save_graph, load_graph),
}

# Run the benchmarks
benchmark_results = {}

for format_name, (file_path, save_func, load_func) in formats.items():
    save_time, load_time = benchmark_format(save_func, load_func, file_path)
    benchmark_results[format_name] = {'Save Time (s)': save_time, 'Load Time (s)': load_time}

# Save benchmark results to file
benchmark_df = pd.DataFrame(benchmark_results).T
benchmark_df.to_csv("/app/output/benchmark_results.csv", index=True, float_format="%.2f")
