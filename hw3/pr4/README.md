
# Benchmark CSV Processing Project

This project benchmarks various approaches to reading and processing CSV files using Python. The project contains two benchmark scripts:

1. **Benchmark for a single large CSV file** (`benchmark.py`)
2. **Benchmark for processing 1000 small CSV files** (`benchmark_1000_files.py`)

## Files:

### 1. **benchmark.py**
   - **Description**: This script benchmarks different methods of reading and processing a single large CSV file (`test.csv`) using:
     - Single-threaded processing
     - Multi-threaded processing
     - Multi-processing
     - Asynchronous I/O
   - **Path**: `/app/benchmark.py`

### 2. **benchmark_1000_files.py**
   - **Description**: This script benchmarks reading and processing 1000 small CSV files (`test-1.csv`, `test-2.csv`, ..., `test-1000.csv`). It uses:
     - Single-threaded processing
     - Multi-threaded processing
     - Multi-processing
   - **Path**: `/app/benchmark_1000_files.py`

### 3. **duplicate_test_csv.py**
   - **Description**: This script creates 1000 copies of `test.csv` with filenames `test-1.csv`, `test-2.csv`, ..., `test-1000.csv`. This is a prerequisite for running `benchmark_1000_files.py`.
   - **Path**: `/app/data/duplicate_test_csv.py`

### 4. **test.csv**
   - **Description**: This is the source CSV file used in both benchmarks. It is copied to create the 1000 files for the second benchmark.
   - **Path**: `/app/data/test.csv`

### 5. **Dockerfiles**
   - **docker-compose-single-file.yml**: Docker Compose configuration for running the benchmark for a single large CSV file.
   - **docker-compose-1000-files.yml**: Docker Compose configuration for running the benchmark for 1000 small CSV files.

### 6. **Requirements**
   - **requirements.txt**: Lists the required Python dependencies:
     - `pandas==2.2.2`
     - `aiofiles==24.1.0`

---

## Attention:
- **Before running `benchmark_1000_files.py`**, you need to generate 1000 CSV files using `duplicate_test_csv.py`. Running this script will create 1000 copies of `test.csv` as `test-1.csv`, `test-2.csv`, ..., `test-1000.csv`.

---

## Results:

### Results for Single CSV File (500 MB):
**benchmark_single_file_results.txt**:

```
Single-threaded: 3.6335 seconds
Multi-threaded (4 threads): 121.8137 seconds
Multi-processing (4 processes): 47.4908 seconds
Asynchronous I/O: 4.7532 seconds
```

### Results for 1000 CSV Files:
**benchmark_1000_files_results.txt**:

```
Single-threaded (1000 files): 111.1569 seconds
Multi-threaded (1000 files, 4 threads): 28.7620 seconds
Multi-processing (1000 files, 4 processes): 29.0377 seconds
```

---

## Commands to Run the Benchmarks:

### For a Single Large CSV File:
```bash
docker compose -f docker-compose-single-file.yml up --build
```

### For 1000 CSV Files:
First, generate the 1000 CSV files:
```bash
python <pr4_folder>/data/duplicate_test_csv.py
```

Then run the benchmark:
```bash
docker compose -f docker-compose-1000-files.yml up --build
```
