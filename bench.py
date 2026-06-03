import time
import generate_dataset

def run_bench():
    start = time.time()
    for _ in range(5):
        generate_dataset.generate_examples(3000)
    end = time.time()
    return end - start

if __name__ == '__main__':
    print(run_bench())
