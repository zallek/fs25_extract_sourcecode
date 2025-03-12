import os
import subprocess
import sys
import logging
from pathlib import Path

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def decompile_lua_file(input_file: Path, output_file: Path, medal_path: Path):
    try:
        # Create output directory if it doesn't exist
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Store current working directory
        original_cwd = os.getcwd()
        
        try:
            # Change to medal-main directory
            os.chdir(medal_path)
            
            # Convert input file path to be relative to medal-main directory if possible
            try:
                relative_input = input_file.relative_to(medal_path)
            except ValueError:
                relative_input = input_file.absolute()
            
            logging.info(f'Attempting to decompile file: {relative_input}')
            
            # Run luau-lifter on the input file with -e flag for key 203
            result = subprocess.run(
                ['cargo', '+nightly', 'run', '--bin', 'luau-lifter', str(relative_input)],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Write the decompiled content to the output file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            
            logging.info(f'Successfully decompiled: {input_file} -> {output_file}')
            
        finally:
            # Restore original working directory
            os.chdir(original_cwd)
        
    except subprocess.CalledProcessError as e:
        logging.error(f'Failed to decompile {input_file}: {e.stderr}')
        if hasattr(e, 'output'):
            logging.error(f'Command output: {e.output}')
    except Exception as e:
        logging.error(f'Error processing {input_file}: {str(e)}')

def process_directory(input_dir: Path, output_dir: Path, medal_path: Path):
    for item in input_dir.rglob('*.lua'):
        if item.is_file():
            # Calculate relative path to maintain directory structure
            rel_path = item.relative_to(input_dir)
            output_file = output_dir / rel_path
            
            logging.info(f'Found Lua file: {item}')
            decompile_lua_file(item, output_file, medal_path)

def main():
    if len(sys.argv) != 4:
        print("Usage: python decompile_lua.py <input_directory> <output_directory> <medal_path>")
        sys.exit(1)

    medal_path = Path(sys.argv[1]).resolve()
    input_dir = Path(sys.argv[2]).resolve()
    output_dir = Path(sys.argv[3]).resolve()

    if not input_dir.exists():
        print(f"Input directory '{input_dir}' does not exist!")
        sys.exit(1)
    
    if not medal_path.exists():
        print(f"Medal-main directory '{medal_path}' does not exist!")
        sys.exit(1)

    setup_logging()
    logging.info(f'Starting decompilation process...')
    logging.info(f'Input directory: {input_dir}')
    logging.info(f'Output directory: {output_dir}')
    logging.info(f'Medal-main directory: {medal_path}')

    process_directory(input_dir, output_dir, medal_path)
    logging.info('Decompilation process completed!')

if __name__ == '__main__':
    main() 