**Goals for the finished project:**  
Support for creation, running and visualization of cellular automata.  

**Creation**  
- Rules are specified through a python function, operating on a proxy
    object, which will provide all the necessary access plus some
    convenience methods.
- Initial state is provided through a two dimensional buffer filled
  with the appropriate type of objects. Pycella doesn't care what is that 
  type. This is completely handled by the provided function. This provides
  freedom to store complex state, like for example a sound to be played
  every time the rules are applied to a cell.
- The GUI will provide options for loading files with rules definitions
  and for loading/saving files with initial state as well as an easy method
  to create an initial state.  

**Running and visualization. Possible in two modes:**
- By directly using the API of the backend in your own code and doing your own visualization.
- By using the GUI which will provide means to conveniently explore the
  evolution of a cellular automaton like:  
    1. Playing the evolution at a convenient and changeable speed  
    2. Pausing  
    3. Running through the evolution step by step  
    4. Going back a step  
    5. Zooming in and out  

**Goals for the second milestone:**  
Build the backend:
* Construction of an automaton from rules and a buffer with the initial state
* Rule applying logic
* Proxy class for the rules_function
* Tests for the backend
