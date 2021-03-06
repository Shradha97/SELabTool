# SELabTool

### Dependencies:

1. Git should be installed in the system and accessable through command line.
2. Python 3.5 should be installed in the system
3. Run the following command:
    > pip install -r requirements.txt

### Current Status:

The tools take a repository name (example - korolvs/snake_nn) and checks the merged pull request and calculates the cyclomatic complexity as well as other details about each function and displays it.
Also, for each of the original file/pull request, the varaition of the CC is displayed graphically.

### Repository Structure:

The repository contains a single python file for performing the above task.

### How to run the code:

1. Open Python IDLE (Python 3.5) and open the code with the editor.
2. Run the code by pressing F5.
3. Enter the name of the repository to check.
4. The data will be displayed for the first 2 pull requests only(for testing purposes).

### To Do

1. Delete temporary files created by the program.
2. GUI
3. Displaying only relavant data based on user needs
4. Showing software evolution through cyclomatic complexity.
5. Currently, the variation of CC for the whole file is shown, variation of CC for individual functions of each pull request has to be displayed.
