# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Constraint propagation is the process of eliminating all values not possible in the solution space of a value based on information gathered from related values then repeating the process if the resulting change provides new information to allow for more reductions. In the case of the sudoku puzzle, the value is the digits in a box and the solution space is '123456789' and related values are digits in other boxes in the list of peers for each box. 

To apply the Naked Twin strategy to constraint propagation, we use the reduction process dictated by the Naked Twin strategy in each iteration of the constraint propagation in addition to the eliminate and only choice strategies. 

The Naked Twin Strategy dictates that if two boxes, in the same peer group, contain the same two digits, only those two boxes, naked twins, are allowed to have either the first or second digit assigned to them in the final result. This logic, in turn, dictates that all other boxes in the same peer group may NOT contain either of the two digits assigned to the naked twin boxes. This allows us to eliminate the same two digits from all other boxes in the peer group during each iteration. 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: This was the simpler of the challenges. All we needed to do was add more units to the unit lists. This, in turn, resulted in more peers to be considered during each of the eliminate, only choice and naked twin strategies. 

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

