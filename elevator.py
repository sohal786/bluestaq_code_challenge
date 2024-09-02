import matplotlib.pyplot as plt
import heapq
import logging

# Assumptions: 
# 1. Single elevator is simulated.
# 2. No real-time request processing (i.e., all requests are queued and then processed).
# 3. No consideration for weight or the number of people in the elevator.

# Set the font family to 'DejaVu Sans' to ensure consistent font usage across all plots,
# and to prevent matplotlib from performing font matching, which can produce multiple logs.
plt.rcParams['font.family'] = 'DejaVu Sans'

class Elevator:
    """
    A class to simulate the behavior of an elevator.
    
    Attributes:
    - current_floor: The current floor where the elevator is located.
    - total_floors: The total number of floors in the building.
    - up_requests: A priority queue for requests where the destination is above the current floor.
    - down_requests: A priority queue for requests where the destination is below the current floor.
    - direction: Indicates the current direction of the elevator (1 for up, -1 for down, 0 for idle).
    - fig, ax: Used to create a visual representation of the elevator's movement using matplotlib.
    - x, y: Coordinates for drawing the elevator in the plot.
    """
    
    def __init__(self, floors=10):
        """
        Initialize the Elevator with a given number of floors.

        Args:
        - floors (int): Total number of floors in the building (default is 10).
        """
        self.current_floor = 0  # Elevator starts at ground floor (floor 0).
        self.total_floors = floors  # Total number of floors in the building.
        self.up_requests = []  # Priority queue for up requests.
        self.down_requests = []  # Priority queue for down requests.
        self.direction = 0  # Elevator starts in an idle state.
        
        # Setup for matplotlib to visualize the elevator's movement.
        self.fig, self.ax = plt.subplots()
        self.x = [0, 10, 10, 0, 0]
        self.y = [0, 0, 20, 20, 0]

    def call_elevator(self, user_floor, destination_floor):
        """
        Add a request to move the elevator to the appropriate queue (up or down) and handle the movement.

        Args:
        - user_floor (int): The floor where the user is currently located.
        - destination_floor (int): The floor the user wants to go to.
        """
        # Check for valid floor numbers.
        if user_floor < 0 or user_floor >= self.total_floors:
            print(f"Invalid user floor: {user_floor}. It must be between 0 and {self.total_floors - 1}.")
            return
        if destination_floor < 0 or destination_floor >= self.total_floors:
            print(f"Invalid destination floor: {destination_floor}. It must be between 0 and {self.total_floors - 1}.")
            return
        if user_floor == destination_floor:
            print(f"You are already on floor {user_floor}. No need to move.")
            return
        
        # Determine the direction of the request.
        direction = 1 if destination_floor > user_floor else -1
        
        # We use two queues (up_requests and down_requests) to process requests based on direction.
        # This ensures that the elevator handles requests in a logical order, minimizing unnecessary movements.
        if direction == 1:  # If the request is upwards.
            heapq.heappush(self.up_requests, (user_floor, destination_floor))
        else:  # If the request is downwards.
            # We store negative values to maintain a max-heap behavior for downward requests.
            heapq.heappush(self.down_requests, (-user_floor, -destination_floor))

        logging.debug(f"Request added: Moving from floor {user_floor} to floor {destination_floor}. Up queue: {self.up_requests}, Down queue: {self.down_requests}")

    def process_requests(self):
        """
        Process all the requests in the up and down queues in order.
        The elevator will handle all up requests before switching to down requests.
        This is done to avoid going up and down when there are multiple requests
        """
        while self.up_requests or self.down_requests:
            if self.direction in [0, 1]:  # Handle upward requests first.
                while self.up_requests:
                    user_floor, destination_floor = heapq.heappop(self.up_requests)
                    self.move_to_floor(user_floor)  # Move to the user's floor.
                    self.move_to_floor(destination_floor)  # Move to the destination floor.
                self.direction = -1  # Switch direction to down after completing up requests.

            if self.direction == -1:  # Handle downward requests next.
                while self.down_requests:
                    user_floor, destination_floor = heapq.heappop(self.down_requests)
                    self.move_to_floor(-user_floor)  # Convert back to positive.
                    self.move_to_floor(-destination_floor)  # Convert back to positive.
                self.direction = 0  # Set to idle after completing all requests.

        # Update the plot to reflect that all requests have been processed.
        self.ax.set_title("All requests processed. Ready for new commands.")
        plt.draw()

    def move_to_floor(self, target_floor):
        """
        Move the elevator to a specified floor.

        Args:
        - target_floor (int): The floor the elevator needs to move to.
        """
        if target_floor == self.current_floor:
            print(f"Already at floor {target_floor}.")
            return

        # Determine direction and print movement status.
        if target_floor > self.current_floor:
            self.direction = 1
            print(f"Moving up to floor {target_floor}...")
        elif target_floor < self.current_floor:
            self.direction = -1
            print(f"Moving down to floor {target_floor}...")

        # Animate the elevator movement to the target floor.
        self._animate_elevator(target_floor)
        self.current_floor = target_floor  # Update the current floor after moving.
        self.direction = 0  # Set to idle once movement is complete.

    def _animate_elevator(self, target_floor):
        """
        Animate the movement of the elevator using matplotlib.
        The plot should be visible when "Proecess Requests" is called on command line
        Args:
        - target_floor (int): The floor the elevator is moving to.
        """
        # Calculate the step size based on the direction.
        floor_diff = target_floor - self.current_floor
        step = 1 if floor_diff > 0 else -1

        # Update the elevator's position on the plot as it moves.
        for i in range(self.current_floor * 10, target_floor * 10, step):
            self.ax.clear()
            self.ax.set_xlim(min(self.x) - 1, max(self.x) + 1)
            self.ax.set_ylim(min(self.y) - 1, max(self.y) + self.total_floors * 10 + 1)
            y_movement = [y_val + i for y_val in self.y]
            self.ax.plot(self.x, y_movement)
            self.ax.set_title(f"Floor: {int(i / 10)}")
            plt.pause(0.01)  # Reduced pause for faster animation.

        # Ensure the final position is displayed accurately.
        self.ax.clear()
        y_movement = [y_val + target_floor * 10 for y_val in self.y]
        self.ax.plot(self.x, y_movement)
        self.ax.set_xlim(min(self.x) - 1, max(self.x) + 1)
        self.ax.set_ylim(min(self.y) - 1, max(self.y) + self.total_floors * 10 + 1)
        self.ax.set_title(f"Floor: {target_floor}")
        plt.draw()

    def display_current_floor(self):
        """
        Display the current floor of the elevator.
        """
        print(f"The elevator is currently at floor {self.current_floor}")

def main():
    """
    Main function to run the elevator simulation.
    Provides a simple menu to add requests, process them, and exit the simulation.
    """
    elevator = Elevator(floors=10)  # Create an elevator with 10 floors.

    while True:
        # Display the menu options.
        print("\nElevator Control Menu (This is an Elevator Simulation):")
        print("1. Add Elevator Request (Call the elevator)")
        print("2. Process Requests (Call this to make the elevator move)")
        print("3. Exit")

        # Get user input and handle their choice.
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            try:
                user_floor = int(input("Enter your current floor: "))
                destination_floor = int(input("Enter your destination floor: "))
                
                # Queue the request based on user input.
                elevator.call_elevator(user_floor, destination_floor)

            except ValueError:
                # Handle invalid input gracefully.
                print("Please enter a valid integer for the floor number.")
        elif choice == '2':
            # Process all queued elevator requests.
            elevator.process_requests()

        elif choice == '3':
            # Exit the simulation.
            print("Exiting...")
            break
        else:
            # Handle invalid menu options.
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
