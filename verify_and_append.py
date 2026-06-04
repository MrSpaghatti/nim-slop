import sys
import json
import subprocess
import os

def main():
    if len(sys.argv) != 2:
        print("Usage: python verify_and_append.py <chunk.json>")
        sys.exit(1)

    chunk_file = sys.argv[1]

    with open(chunk_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for i, item in enumerate(data):
        nim_code = item['nim_code']
        temp_path = f"nimcheck_test_{i}.nim"
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(nim_code)

        try:
            result = subprocess.run(['nim', 'check', temp_path], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error in example {i+1}:")
                print(result.stdout)
                print(result.stderr)
                os.remove(temp_path)
                sys.exit(1)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    print(f"All {len(data)} examples passed compilation check.")

    with open('nim_stdlib_heavy.jsonl', 'a', encoding='utf-8') as out_f:
        for item in data:
            out_f.write(json.dumps(item) + '\n')

    print(f"Appended {len(data)} examples to nim_stdlib_heavy.jsonl")

if __name__ == '__main__':
    main()
