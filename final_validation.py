import sys
import json
import re

def main():
    if len(sys.argv) != 2:
        print("Usage: python final_validation.py <jsonl_file>")
        sys.exit(1)

    jsonl_file = sys.argv[1]

    with open(jsonl_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"Total lines: {len(lines)}")
    if len(lines) != 200:
        print(f"Error: Expected 200 lines, got {len(lines)}")
        sys.exit(1)

    prompts = set()
    thinkings = set()
    total_chars = 0

    for i, line in enumerate(lines):
        try:
            data = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"Error: Line {i+1} is not valid JSON. {e}")
            sys.exit(1)

        if set(data.keys()) != {'prompt', 'thinking', 'nim_code'}:
            print(f"Error: Line {i+1} does not have exact keys 'prompt', 'thinking', 'nim_code'.")
            sys.exit(1)

        prompt = data['prompt']
        thinking = data['thinking']
        nim_code = data['nim_code']

        prompts.add(prompt)
        thinkings.add(thinking)
        total_chars += len(nim_code)

        if len(nim_code.splitlines()) < 15:
            print(f"Error: Line {i+1} code is less than 15 lines.")
            sys.exit(1)

        import_match = re.search(r'import\s+(.*?)(?:\n|$)', nim_code)
        if not import_match:
            print(f"Error: Line {i+1} missing imports.")
            sys.exit(1)

        imports = [m.strip() for m in import_match.group(1).split(',')]
        if len(imports) < 3:
            print(f"Error: Line {i+1} has fewer than 3 imports: {imports}")
            sys.exit(1)

        if 'when isMainModule:' not in nim_code:
            print(f"Error: Line {i+1} missing 'when isMainModule:' block.")
            sys.exit(1)

    if len(thinkings) < 200:
        print(f"Error: Duplicate thinkings found. Unique thinkings: {len(thinkings)}")
        sys.exit(1)

    if len(prompts) < 180:
        print(f"Error: Not enough unique prompts. Unique prompts: {len(prompts)}/200")
        sys.exit(1)

    avg_chars = total_chars / len(lines)
    if avg_chars < 500:
        print(f"Error: Average chars too low: {avg_chars}. Expected >= 500")
        sys.exit(1)

    print(f"Success: All validations passed.")
    print(f"- Total lines: {len(lines)}")
    print(f"- Unique prompts: {len(prompts)}")
    print(f"- Unique thinkings: {len(thinkings)}")
    print(f"- Average code length: {avg_chars:.2f} chars")

if __name__ == '__main__':
    main()
