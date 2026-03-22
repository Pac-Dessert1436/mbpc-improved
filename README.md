# `mbpc-improved`: Enhanced "Much Better Python Classes"

## Description

`mbpc-improved` is an enhanced version of [MBPC](https://github.com/MintLF/MBPC/) ("Much Better Python Classes"), a powerful library that introduces advanced object-oriented programming capabilities to Python. It provides utilities for defining interfaces, classes, and structs in a more structured, type-safe manner, bringing some of the best features of statically-typed languages to Python's dynamic environment.

### Key Improvements Over Original MBPC
- **Snake_case Consistency**: All identifiers converted from camelCase to Python's standard snake_case.
- **Improved Readability**: Lambda expressions replaced with explicit `def-return` statements.
- **Struct Support**: Added `structdef` for creating data-focused structures with interface support.
- **Simplified Initialization**: Renamed `initialize` method to `init` for brevity and consistency.
- **Object Cloning**: Added `clone` method for deep copying objects.
- **Enhanced Iterability**: Eliminated need for manual list conversion when iterating over interfaces.

_Note: For built-in iterability, simply use Python's `reversed(...)` function._

## Installation

### Prerequisites
- Python 3.7 or higher

### Via `pip`
Install the package directly from PyPI:

```bash
pip install mbpc-improved
```

### From Source
1. Clone the repository:

```bash
git clone https://github.com/Pac-Dessert1436/mbpc-improved.git
cd mbpc-improved
```

2. Install in development mode:

```bash
pip install -e .
```

> **Note**: Avoid running scripts directly within the `mbpc` directory, as this may cause import errors. Always run from the project root or install the package first.

## Core Components

`mbpc-improved` provides three primary decorators for defining structured components:

| Component | Description |
|-----------|-------------|
| `interfacedef` | Define interfaces with required methods that must be implemented by classes or structs. |
| `classdef` | Create classes with inheritance and interface implementation capabilities. |
| `structdef` | Define data-focused structures (similar to C structs) with interface support. |

## Usage Examples

### 1. Defining Interfaces

Interfaces define contracts that classes or structs must implement. Use `interfacedef` to create interfaces with required methods:

```python
from mbpc.interfacedef import interfacedef

@interfacedef()
def Hashable(self):
    """Interface for objects that can be hashed."""
    @self.method
    def hashcode() -> int: ...  # Must return an integer hash value

@interfacedef()
def Equatable(self):
    """Interface for objects that can be compared for equality."""
    @self.method
    def equals(other) -> bool: ...  # Must return a boolean

# NOTE: Common interfaces like Hashable and Equatable are already available in `mbpc.interfaces`
```

### 2. Creating Structs

Structs are lightweight, data-focused structures that can implement interfaces. They're ideal for simple data containers:

```python
from mbpc.structdef import structdef
from mbpc.interfaces import Hashable, Equatable

@structdef(Hashable, Equatable)
def Point(self, x: int, y: int):
    """A 2D point struct with x and y coordinates."""
    # Initialize instance variables
    self.x = x
    self.y = y

    # Implement Hashable interface
    @self.method
    def hashcode(self) -> int:
        """Generate a hash value for the point."""
        return hash((self.x, self.y))

    # Implement Equatable interface
    @self.method
    def equals(self, other) -> bool:
        """Compare two points for equality."""
        if not hasattr(other, 'x') or not hasattr(other, 'y'):
            return False
        return self.x == other.x and self.y == other.y

# Example Usage:
p1 = Point(2, 3)
p2 = Point(2, 3)
p3 = Point(5, 7)

print(p1.x, p1.y)         # Output: 2 3
print(p1.hashcode())      # Output: (hash value of (2, 3))
print(p1.equals(p2))      # Output: True
print(p1.equals(p3))      # Output: False
print(p1.to_string())     # Output: {'x': 2, 'y': 3} (built-in method)
print(p1.clone())         # Output: Point(x=2, y=3) (deep copy)
```

### 3. Defining Classes

Classes support full object-oriented features including inheritance and interface implementation, but the parent constructor are always called first:

```python
from mbpc.classdef import classdef
from mbpc.interfaces import Equatable

@classdef()
def Person(self, name: str, age: int):
    """A person class with name and age attributes."""
    # Call parent constructor (required for all classes)
    self.super.init()
    
    # Initialize instance variables
    self.name = name
    self.age = age

    # Define instance methods
    @self.method
    def greet(self) -> str:
        """Return a greeting message."""
        return f"Hello, my name is {self.name}"

    # Implement Equatable interface
    @self.method
    def equals(self, other) -> bool:
        """Compare two Person objects for equality."""
        if not isinstance(other, Person):
            return False
        return self.name == other.name and self.age == other.age

    # Define to_string method (built-in method override)
    @self.method
    def to_string(self) -> str:
        """Return a string representation of the person."""
        return f"Person(name='{self.name}', age={self.age})"

# Example Usage:
person1 = Person("Alice", 30)
person2 = Person("Alice", 30)
person3 = Person("Bob", 25)

print(person1.greet())      # Output: Hello, my name is Alice
print(person1.equals(person2))  # Output: True
print(person1.equals(person3))  # Output: False
print(person1.to_string())  # Output: Person(name='Alice', age=30)
```

### 4. Class Inheritance

Classes can inherit from other classes, overriding methods as needed:

```python
from mbpc.classdef import classdef

# Inherit from the Person class defined in the previous example
@classdef(Person)  # Specify the parent class
def Student(self, name: str, age: int, major: str, student_id: str):
    """A Student class inheriting from Person."""
    # Call parent constructor with required parameters
    self.super.init(name, age)
    
    # Add new instance variables
    self.major = major
    self.student_id = student_id

    # Override the greet method from Person
    @self.method
    def greet(self) -> str:
        """Return a student-specific greeting."""
        return f"Hello, I'm {self.name}, studying {self.major} (ID: {self.student_id})"

    # Override to_string to include student-specific information
    @self.method
    def to_string(self) -> str:
        """Return a string representation of the student."""
        return f"Student(name='{self.name}', age={self.age}, major='{self.major}', id='{self.student_id}')"

# Example Usage:
student = Student("Bob", 20, "Computer Science", "CS12345")
print(student.greet())  # Output: Hello, I'm Bob, studying Computer Science (ID: CS12345)
print(student.to_string())  # Output: Student(name='Bob', age=20, major='Computer Science', id='CS12345')

# Access inherited attributes
print(student.name)  # Output: Bob
print(student.age)   # Output: 20
```

## Interface Enforcement

`mbpc-improved` enforces strict interface implementation at runtime, ensuring that classes and structs adhere to the contracts defined by interfaces:

### Validation Checks
- **Missing Methods**: Raises `InterfaceError` if any required interface method is not implemented.
- **Incorrect Signatures**: Validates method parameters and return type hints.
- **Method Types**: Supports both instance methods and static methods.

### Example of Enforcement

```python
from mbpc.interfacedef import interfacedef
from mbpc.classdef import classdef
from mbpc.interfaces import InterfaceError

@interfacedef()
def Countable(self):
    @self.method
    def count() -> int: ...  # Must return an integer

# This will raise an error because count() is not implemented
@classdef(Countable)
def BrokenCounter(self):
    self.value = 0
    
    # Missing count() method implementation
    
# This will also raise an error because count() returns wrong type
@classdef(Countable)
def WrongReturnType(self):
    self.value = 0
    
    @self.method
    def count(self) -> str:  # Should return int, not str
        return "5"
```

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests on the [GitHub repository](https://github.com/Pac-Dessert1436/mbpc-improved).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Authors

- Original MBPC by [MintLF](https://github.com/MintLF)
- Enhanced version by [Pac-Dessert1436](https://github.com/Pac-Dessert1436)

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/Pac-Dessert1436/mbpc-improved/issues) on GitHub.