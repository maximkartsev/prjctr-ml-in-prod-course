import pandas as pd
import time
import concurrent.futures
import os

# File path format for the 1000 CSV files
file_pattern = '/app/data/test-{i}.csv'
output_path = '/app/output/benchmark_1000_files_results.txt'

# List of CSV file names
csv_files = [file_pattern.format(i=i) for i in range(1, 1001)]

def process_file(df):
    # Simulate some processing that takes 0.1 seconds
    time.sleep(0.1)
    return len(df)

# measure time for synchronous functions
def measure_time_sync(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return end_time - start_time, result

# Single-threaded reading and processing of 1000 CSV files
def benchmark_single_thread_1000_files():
    results = []
    for csv_file in csv_files:
        if os.path.exists(csv_file):  # Ensure the file exists
            df = pd.read_csv(csv_file)
            result = process_file(df)  # Process the file
            results.append(result)
    return results

# Multi-threaded reading and processing of 1000 CSV files
def read_and_process_file_thread(csv_file):
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        return process_file(df)
    return None  # In case the file doesn't exist

def benchmark_multi_thread_1000_files(n_threads):
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_threads) as executor:
        futures = [executor.submit(read_and_process_file_thread, csv_file) for csv_file in csv_files]
        results = [f.result() for f in concurrent.futures.as_completed(futures) if f.result() is not None]
    return results

# Multi-processing reading and processing of 1000 CSV files
def read_and_process_file_process(csv_file):
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        return process_file(df)
    return None  # In case the file doesn't exist

def benchmark_multi_process_1000_files(n_processes):
    with concurrent.futures.ProcessPoolExecutor(max_workers=n_processes) as executor:
        futures = [executor.submit(read_and_process_file_process, csv_file) for csv_file in csv_files]
        results = [f.result() for f in concurrent.futures.as_completed(futures) if f.result() is not None]
    return results

# Main benchmarking script
if __name__ == "__main__":
    results = []

    # Single-threaded benchmark for 1000 files
    single_thread_time, _ = measure_time_sync(benchmark_single_thread_1000_files)
    results.append(f"Single-threaded (1000 files): {single_thread_time:.4f} seconds")

    # Multi-threaded benchmark for 1000 files
    n_threads = 4
    multi_thread_time, _ = measure_time_sync(benchmark_multi_thread_1000_files, n_threads)
    results.append(f"Multi-threaded (1000 files, {n_threads} threads): {multi_thread_time:.4f} seconds")

    # Multi-processing benchmark for 1000 files
    n_processes = 4
    multi_process_time, _ = measure_time_sync(benchmark_multi_process_1000_files, n_processes)
    results.append(f"Multi-processing (1000 files, {n_processes} processes): {multi_process_time:.4f} seconds")

    # Save results to a text file
    with open(output_path, 'w') as f:
        for result in results:
            f.write(result + '\n')
    
    print("Benchmark results saved to", output_path)
    for result in results:
        print(result)
