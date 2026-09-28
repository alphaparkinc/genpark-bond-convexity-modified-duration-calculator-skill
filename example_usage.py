from client import BondDurationConvexity

def run_example():
    print("=== GenPark Bond Duration & Convexity Example ===")
    calc = BondDurationConvexity()
    print("Bond Analytics:", calc.benchmark_bond_analytics())

if __name__ == "__main__":
    run_example()
