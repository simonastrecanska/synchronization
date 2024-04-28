# Synchronization
Program that synchronizes two folders: source and replica. The program would maintain a full, identical copy of source folder at replica folder. Synchronization is scheduled to occur at regular intervals. All file creation, copying, and removal operations are logged both to a file and to the console output. Folder paths, synchronization interval, and log file path are specified as command-line arguments when running the program.

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/simonastrecanska/synchronization.git
   ```

2. Navigate to the project directory:

   ```bash
   cd synchronization
   ```

3. Install dependencies:

   ```bash
   python3 -m venv venv
   ```

4. Run the program:

   ```bash
   ./synchronize <source_directory> <target_directory> <log_file> [--interval INTERVAL]
   ```

   - `<source_directory>`: Path to the source directory.
   - `<target_directory>`: Path to the target directory.
   - `<log_file>`: Path to the log file.
   - `--interval INTERVAL`: Synchronization interval in seconds (default: 100).

## Example


```bash
./synchronize tests/source tests/target logs/logfile.log 5

```
