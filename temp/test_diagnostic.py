#!/usr/bin/env python3
"""
Test script to demonstrate diagnostic features
"""

# Wire pairs (output, input)
WIRE_PAIRS = [
    (17, 27),  # Pair 1
    (22, 10),  # Pair 2
    (9, 11),    # Pair 3
    (5, 6)     # Pair 4
]

def get_diagnostic_message(pair_status, cross_connections, in_to_in_connections, out_to_out_connections):
    """Generate diagnostic message based on current status"""
    
    messages = []
    
    # Check for open pairs
    open_pairs = []
    for i, (output_pin, input_pin) in enumerate(WIRE_PAIRS):
        if not pair_status[i]:
            open_pairs.append(f"Pair {i+1}: GPIO{output_pin} ↔ GPIO{input_pin}")
    
    if open_pairs:
        messages.append("OPEN PAIRS:")
        messages.extend(open_pairs)
    
    # Check for cross connections
    if cross_connections:
        messages.append("\nCROSS CONNECTIONS:")
        for pair1, pair2 in cross_connections:
            out1, in1 = WIRE_PAIRS[pair1]
            out2, in2 = WIRE_PAIRS[pair2]
            messages.append(f"GPIO{out1} → GPIO{in2} (wrong connection)")
    
    # Check for IN-to-IN connections
    if in_to_in_connections:
        messages.append("\nIN-TO-IN CONNECTIONS:")
        for pair1, pair2 in in_to_in_connections:
            _, in1 = WIRE_PAIRS[pair1]
            _, in2 = WIRE_PAIRS[pair2]
            messages.append(f"GPIO{in1} ↔ GPIO{in2} (should not be connected)")
    
    # Check for OUT-to-OUT connections
    if out_to_out_connections:
        messages.append("\nOUT-TO-OUT CONNECTIONS:")
        for pair1, pair2 in out_to_out_connections:
            out1, _ = WIRE_PAIRS[pair1]
            out2, _ = WIRE_PAIRS[pair2]
            messages.append(f"GPIO{out1} ↔ GPIO{out2} (should not be connected)")
    
    if not messages:
        return "All connections are correct!"
    
    return "\n".join(messages)

def get_status_summary(pair_status, cross_connections, in_to_in_connections, out_to_out_connections):
    """Get a summary of the current status"""
    
    total_issues = len([p for p in pair_status if not p]) + len(cross_connections) + len(in_to_in_connections) + len(out_to_out_connections)
    
    if total_issues == 0:
        return "All pairs connected correctly"
    elif any(not p for p in pair_status):
        open_count = len([p for p in pair_status if not p])
        return f"{open_count} pair(s) not connected"
    else:
        return f"{total_issues} connection issue(s) detected"

def main():
    print("Wire Checker Diagnostic Test")
    print("============================")
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "All Good",
            "pair_status": [True, True, True, True],
            "cross": [],
            "in_in": [],
            "out_out": []
        },
        {
            "name": "Pair 1 Open",
            "pair_status": [False, True, True, True],
            "cross": [],
            "in_in": [],
            "out_out": []
        },
        {
            "name": "Cross Connection",
            "pair_status": [True, True, True, True],
            "cross": [(0, 1)],
            "in_in": [],
            "out_out": []
        },
        {
            "name": "Multiple Issues",
            "pair_status": [False, True, False, True],
            "cross": [(1, 3)],
            "in_in": [(0, 2)],
            "out_out": []
        },
        {
            "name": "All Pairs Open",
            "pair_status": [False, False, False, False],
            "cross": [],
            "in_in": [],
            "out_out": []
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n--- Test Scenario {i}: {scenario['name']} ---")
        
        summary = get_status_summary(
            scenario['pair_status'], 
            scenario['cross'], 
            scenario['in_in'], 
            scenario['out_out']
        )
        print(f"Summary: {summary}")
        
        diagnostic = get_diagnostic_message(
            scenario['pair_status'], 
            scenario['cross'], 
            scenario['in_in'], 
            scenario['out_out']
        )
        print(f"Diagnostic:\n{diagnostic}")
        print("-" * 50)

if __name__ == '__main__':
    main() 