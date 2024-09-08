import shutil

# Path to the source file
source_file = 'test.csv'

# Copy the source file to 1000 new files with different names
for i in range(1, 1001):
    # Create target file name
    target_file = f'test-{i}.csv'
    
    # Copy the file
    try:
        shutil.copy(source_file, target_file)
        print(f"Copied to: {target_file}")
    except FileNotFoundError:
        print(f"Source file {source_file} not found.")
        break
    except IOError as e:
        print(f"Failed to copy to {target_file}: {e}")
