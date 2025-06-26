import time

class ThisClass:
    def __init__(self, name="DefaultThisClass"):
        self.name = name
        self._is_active = False # Internal state flag for this class
        print(f"[{self.name}] ThisClass instance initialized.")

    class _ProcessContextManager:
        """
        Context manager to manage the internal processing of ThisClass.
        Usually intended to be accessed only from ThisClass methods.
        """
        def __init__(self, parent_instance):
            self.parent = parent_instance
            print(f"[{self.parent.name}] _ProcessContextManager initialized.")

        def __enter__(self):
            """
            Called when entering the 'with' block.
            Sets the parent instance to an active state.
            """
            print(f"[{self.parent.name}] __enter__() called. Starting process.")
            if self.parent._is_active:
                raise RuntimeError(f"[{self.parent.name}] A process is already active.")
            self.parent._is_active = True
            print(f"[{self.parent.name}] _is_active: {self.parent._is_active}")
            return self.parent # Return the parent instance for 'with ... as'

        def __exit__(self, exc_type, exc_value, traceback):
            """
            Called when exiting the 'with' block.
            Sets the parent instance to an inactive state and performs cleanup.
            """
            print(f"[{self.parent.name}] __exit__() called. Ending process.")
            self.parent._is_active = False
            print(f"[{self.parent.name}] _is_active: {self.parent._is_active}")

            if exc_type is not None:
                print(f"[{self.parent.name}] An exception occurred: {exc_type.__name__}: {exc_value}")
                # Re-raise the exception
                return False
            return False

    def Process(self):
        """
        Returns an instance of the context manager to be used with the 'with' statement.
        Calling this method prepares for 'with ... as'.
        """
        print(f"[{self.name}] Process() method called.")
        return self._ProcessContextManager(self)

    # Other methods of ThisClass
    def perform_task(self):
        """Method to perform other tasks of ThisClass (checks processing flag)."""
        if self._is_active:
            print(f"[{self.name}] Performing task during an active process.")
            time.sleep(0.05)
        else:
            print(f"[{self.name}] (Warning) Attempted to perform task when no process is active.")


# --- Usage Examples ---

print("--- Scenario 1: Normal processing ---")
my_instance = ThisClass("MainProcess")
print(f"Initial state: _is_active = {my_instance._is_active}")

with my_instance.Process() as main_process:
    # Inside the 'with' block, 'main_process' refers to the same object as 'my_instance'
    print(f"Inside 'with' block (start): _is_active = {main_process._is_active}")
    main_process.perform_task() # Call a method of the parent instance
    print(f"[{main_process.name}] Executing some main processing...")
    time.sleep(0.1)
    main_process.perform_task()
    # If needed, the object received via 'with ... as' can also be used
    print(f"Just before exiting 'with' block: _is_active = {my_instance._is_active}")

print(f"After 'with' block: _is_active = {my_instance._is_active}")


print("\n--- Scenario 2: Processing with an exception ---")
another_instance = ThisClass("ErrorProcess")
print(f"Initial state: _is_active = {another_instance._is_active}")

try:
    with another_instance.Process() as error_process:
        print(f"Inside 'with' block (start): _is_active = {error_process._is_active}")
        print(f"[{error_process.name}] Executing a process that will cause an error...")
        time.sleep(0.05)
        raise ValueError("Intentional error") # Raise an exception
except ValueError as e:
    print(f"Caught exception outside: {e}")

print(f"After 'with' block (exception): _is_active = {another_instance._is_active}")


print("\n--- Scenario 3: Attempting nested processing (invalid use) ---")
# Designed to raise an error if attempting to nest multiple processes on the same instance
third_instance = ThisClass("MultiProcess")
print(f"Initial state: _is_active = {third_instance._is_active}")

try:
    with third_instance.Process():
        print(f"[{third_instance.name}] Outer process active: {third_instance._is_active}")
        time.sleep(0.05)
        with third_instance.Process(): # This should cause an error
            print(f"[{third_instance.name}] Inner process active: {third_instance._is_active}")
except RuntimeError as e:
    print(f"Caught error outside: {e}")

print(f"After 'with' block (error occurred): _is_active = {third_instance._is_active}")