import pandas as pd
import time
import concurrent.futures
import asyncio
import aiofiles

csv_file = '/app/data/test.csv'
output_path = '/app/output/benchmark_single_file_results.txt'

# Stub processing function
def process_chunk(df_chunk):
    # Simulate some processing that takes 0.1 seconds
    time.sleep(0.1)
    return len(df_chunk)

# measure time for synchronous functions
def measure_time_sync(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return end_time - start_time, result

# measure time for asynchronous functions
async def measure_time_async(func, *args):
    start_time = time.time()
    result = await func(*args)
    end_time = time.time()
    return end_time - start_time, result

# Benchmark single-threaded CSV reading and independent processing
def benchmark_single_thread():
    df = pd.read_csv(csv_file)
    return process_chunk(df)  # Process the entire CSV

# Multi-threaded approach (process each chunk independently)
def read_and_process_chunk_thread(start, chunk_size):
    df_chunk = pd.read_csv(csv_file, skiprows=range(1, start + 1), nrows=chunk_size, header=None)
    return process_chunk(df_chunk)

def benchmark_multi_thread(n_threads, chunk_size):
    total_rows = sum(1 for row in open(csv_file)) - 1
    starts = list(range(0, total_rows, chunk_size))

    with concurrent.futures.ThreadPoolExecutor(max_workers=n_threads) as executor:
        futures = [executor.submit(read_and_process_chunk_thread, start, chunk_size) for start in starts]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]  # Processed results
    
    return results  # Return independent results from each thread

# Multi-processing approach (process each chunk independently)
def read_and_process_chunk_process(start, chunk_size):
    df_chunk = pd.read_csv(csv_file, skiprows=range(1, start + 1), nrows=chunk_size, header=None)
    return process_chunk(df_chunk)

def benchmark_multi_process(n_processes, chunk_size):
    total_rows = sum(1 for row in open(csv_file)) - 1
    starts = list(range(0, total_rows, chunk_size))

    with concurrent.futures.ProcessPoolExecutor(max_workers=n_processes) as executor:
        futures = [executor.submit(read_and_process_chunk_process, start, chunk_size) for start in starts]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]  # Processed results
    
    return results  # Return independent results from each process

# Asynchronous approach with aiofiles (stubbed as just reading for now)
async def read_and_process_chunk_async():
    async with aiofiles.open(csv_file, mode='r') as f:
        content = await f.read()
    # Simulate processing on the content
    return len(content.splitlines())  # Example: count the lines (processing step)

async def benchmark_async_io():
    return await read_and_process_chunk_async()

# Main benchmarking script
if __name__ == "__main__":
    results = []

    # Single-threaded
    single_thread_time, _ = measure_time_sync(benchmark_single_thread)
    results.append(f"Single-threaded: {single_thread_time:.4f} seconds")

    # Multi-threaded
    n_threads = 4
    chunk_size = 10000
    multi_thread_time, _ = measure_time_sync(benchmark_multi_thread, n_threads, chunk_size)
    results.append(f"Multi-threaded ({n_threads} threads): {multi_thread_time:.4f} seconds")

    # Multi-processing
    n_processes = 4
    multi_process_time, _ = measure_time_sync(benchmark_multi_process, n_processes, chunk_size)
    results.append(f"Multi-processing ({n_processes} processes): {multi_process_time:.4f} seconds")

    # Asynchronous I/O
    async def run_async_benchmark():
        async_io_time, _ = await measure_time_async(benchmark_async_io)
        results.append(f"Asynchronous I/O: {async_io_time:.4f} seconds")

    asyncio.run(run_async_benchmark())

    # Save results to a text file
    with open(output_path, 'w') as f:
        for result in results:
            f.write(result + '\n')
    
    print("Benchmark results saved to", output_path)
    for result in results:
        print(result)