# Mock GPIO module for Windows testing
import time
import random

class MockGPIO:
    BCM = "BCM"
    OUT = "OUT"
    IN = "IN"
    HIGH = True
    LOW = False
    PUD_DOWN = "PUD_DOWN"
    
    _pin_states = {}
    _pin_modes = {}
    
    @classmethod
    def setmode(cls, mode):
        pass
    
    @classmethod
    def setwarnings(cls, state):
        pass
    
    @classmethod
    def setup(cls, pin, mode, pull_up_down=None):
        cls._pin_modes[pin] = mode
        if mode == cls.OUT:
            cls._pin_states[pin] = cls.LOW
    
    @classmethod
    def output(cls, pin, state):
        cls._pin_states[pin] = state
    
    @classmethod
    def input(cls, pin):
        # Simulate random input for testing
        return random.choice([True, False])
    
    @classmethod
    def cleanup(cls):
        cls._pin_states.clear()
        cls._pin_modes.clear()

# Create mock GPIO instance
GPIO = MockGPIO()