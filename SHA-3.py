"""
SHA-3 simplified simulation (ignore permutation).

- State: 25 lanes (5x5), each lane = 64 bits.
- Rate = 1024 bits -> 1024/64 = 16 lanes (rate lanes).
- Capacity = 1600-1024 = 576 bits -> 576/64 = 9 lanes (capacity lanes).
- We will XOR message lanes into the 16 rate lanes only.
- We ignore the permutation entirely.
- Show that the 9 capacity lanes remain zero forever.
"""

import random

LANE_BITS = 64
NUM_LANES = 25
RATE_BITS = 1024
RATE_LANES = RATE_BITS // LANE_BITS   # 16
CAPACITY_LANES = NUM_LANES - RATE_LANES  # 9

def make_random_nonzero_lane():
    """Return a 64-bit integer with at least one nonzero bit."""
    # ensure nonzero by sampling from 1..(2^64-1)
    return random.randrange(1, 1 << LANE_BITS)

def lanes_to_binstr(lanes):
    return ' '.join(f"{lane:064b}" for lane in lanes)

def simulate_absorb_without_permutation(iterations = 1000):
    # Initialize state lanes: all zeros
    state = [0] * NUM_LANES

    # Choose which lane indices are rate vs capacity.
    # We'll use the simple convention: lane indices 0..15 are rate, 16..24 are capacity.
    rate_indices  = list(range(RATE_LANES))          # 0..15
    cap_indices   = list(range(RATE_LANES, NUM_LANES))  # 16..24

    # First message block P0: we are told each of the lanes in P0 has at least one nonzero bit.
    # P0 is only RATE_LANES long (16 lanes), so put a nonzero lane into each rate lane.
    P0 = [make_random_nonzero_lane() for _ in range(RATE_LANES)]

    # Absorb P0: XOR into rate lanes
    for i, idx in enumerate(rate_indices):
        state[idx] ^= P0[i]

    # For demonstration we can show that capacity lanes are still zero
    print("After absorbing P0 (without permutation):")
    print("Rate lanes (0..15):")
    print(lanes_to_binstr([state[i] for i in rate_indices]))
    print("\nCapacity lanes (16..24) - SHOULD BE ALL ZEROS:")
    print(lanes_to_binstr([state[i] for i in cap_indices]))

    # Now absorb many more random message blocks (each block supplies RATE_LANES lanes).
    # Since we are ignoring the permutation, absorption always XORs into the *same* rate lanes.
    # Capacity lanes are never XORed, so they remain zero forever.
    for it in range(iterations):
        # next message block (could be random or all-nonzero, doesn't matter)
        block = [make_random_nonzero_lane() for _ in range(RATE_LANES)]
        for i, idx in enumerate(rate_indices):
            state[idx] ^= block[i]
        # optionally, we could check capacity lanes each iteration
        if any(state[idx] != 0 for idx in cap_indices):
            # This should never run when permutation is ignored
            print(f"At iteration {it} capacity lane became nonzero (unexpected).")
            break
    else:
        print(f"\nAfter {iterations} additional absorptions (no permutation), capacity lanes are still all zeros.")
        print("Capacity lanes (16..24):", state[RATE_LANES:])

if __name__ == "__main__":
    simulate_absorb_without_permutation(iterations=100000)
