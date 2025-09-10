import math

def factorial(n):
    result = 1
    for i in range(1, n+1):
        result *= i
    return result

def main():
    total_keys = factorial(25)
    log2_total_keys = math.log2(total_keys)
    print(f"Total possible keys (25!): {total_keys}")
    print(f"Approximate as 2^{log2_total_keys:.0f}")
    print(f"Effectively unique keys (approximate): 2^61")

if __name__ == "__main__":
    main()
