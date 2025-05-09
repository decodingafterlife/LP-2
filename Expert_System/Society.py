class ExpertSystem:
    def __init__(self):
        # Mapping of scenarios to their unique explanations
        self.scenarios = {
            1: {
                "name": "Circuit breaker tripped",
                "explanation": "The circuit breaker for the common passage was tripped and not reset."
            },
            2: {
                "name": "All bulbs burned out",
                "explanation": "All bulbs in the common passage were burned out and replacement was delayed."
            },
            3: {
                "name": "Power outage",
                "explanation": "There was a general power outage affecting the building."
            }
        }
    
    def get_explanation(self, scenario_id):
        """Get the explanation for a specific scenario."""
        if scenario_id in self.scenarios:
            return self.scenarios[scenario_id]["explanation"]
        return "Unknown scenario."

def user_interface():
    """User interface for the three specified scenarios with unique explanations."""
    expert_system = ExpertSystem()
    
    while True:
        print("\n===== Society Maintenance Expert System =====")
        print("\nPlease select a scenario:")
        print("1. Circuit breaker tripped")
        print("2. All bulbs burned out")
        print("3. Power outage")
        print("4. Exit")
        
        user_input = input("\nEnter your choice (1-4): ")
        
        if user_input == '4':
            print("Thank you for using the Society Maintenance Expert System.")
            break
        
        try:
            scenario_id = int(user_input)
            if 1 <= scenario_id <= 3:
                explanation = expert_system.get_explanation(scenario_id)
                scenario_name = expert_system.scenarios[scenario_id]["name"]
                
                print(f"\nScenario: {scenario_name}")
                print(f"{explanation}")
                
                input("\nPress Enter to continue...")
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    user_interface()