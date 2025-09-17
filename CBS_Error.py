def analyze_cbc_error_propagation():
    print("CBC Error Propagation Analysis\n")
    
    print("CBC Mode Error Propagation:")
    print("P1 = D(C1) \u2295 IV")  # ⊕ XOR
    print("P2 = D(C2) \u2295 C1")
    print("P3 = D(C3) \u2295 C2")
    print("...\n")
    
    print("If there's an error in transmitted C1:")
    print("- P1 will be corrupted (directly affected)")
    print("- P2 will be corrupted (because P2 = D(C2) ⊕ C1)")
    print("- P3, P4, ... will NOT be affected\n")
    
    print("Answers:")
    print("a. Are any blocks beyond P2 affected? NO")
    print(" Only P1 and P2 are affected by an error in C1.\n")
    
    print("b. If there's a bit error in source P1:")
    print(" - This error propagates through ALL subsequent ciphertext blocks")
    print(" - C1 = E(P1 ⊕ IV) - error in P1 affects C1")
    print(" - C2 = E(P2 ⊕ C1) - error propagates to C2")
    print(" - C3 = E(P3 ⊕ C2) - error continues to propagate")
    print(" - Effect: ALL ciphertext blocks after the error are affected")
    print(" - At receiver: ALL plaintext blocks will be corrupted\n")

if __name__ == "__main__":
    analyze_cbc_error_propagation()
