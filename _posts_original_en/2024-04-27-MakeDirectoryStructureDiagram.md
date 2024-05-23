# How to Easily Create a Directory Structure Diagram (Includes Python Code)
::tags{RPA, Python}::

---

This article introduces two methods for creating a directory structure diagram, depending on the situation.

## What You Will Learn
You'll learn how to easily create directory structure diagrams (folder structure diagrams) like the following:
```
C:\Users\xxx
 ├── aa
 │    ├── aa
 │    ├── bb
 │    │    └── cc
 │    ├── dd
 │    │    ├── ee
 │    │    │    └── ff
 │    │    └── gg
 │    │         ├── hh
 │    │         └── ii
 │    └── jj
 ├── kk
 └── ll
```

## Two Methods
### [Tree](https://tree.nathanfriend.io/)
- By entering the directory structure as text on this web page, it converts it into a nice text-based diagram.
- Useful if the folder does not yet exist.

- The [source code](https://gitlab.com/nfriend/tree-online) is also available.

### [directory-structure-diagram](https://github.com/hitbug0/directory-structure-diagram)
- Written by me!
- Running this Python code in the directory whose structure you want to know produces a nice diagram (`directory_structure.txt`).
- Useful if the folder and its contents already exist.
- Ideal for company tasks since processing is completed locally, and the only action required is running the program.

- Can be easily integrated into other programs.

## About Method 2
Since I wrote the code, here's a brief introduction.

### How to Use
1. Install Python
    - Version: I use `3.10`, but anything `3.6` or later should work.

1. Download the code from GitHub's [directory-structure-diagram](https://github.com/hitbug0/directory-structure-diagram)
1. Place `directory-structure-diagram.py` and `run.bat` in the directory whose structure you want to know
1. Run `run.bat`
    - Alternatively, you can run `directory-structure-diagram.py` (the bat file is just for convenience)

That's it!

### Code
#### directory-structure-diagram.py
You can change the branch length and spacing in the diagram by adjusting `NUM_INDENTS`, `BRANCH`, and `LEAF` at the beginning of the code.
```Python
import os

NUM_INDENTS = 1
BRANCH = " "*NUM_INDENTS + "├── "
LEAF   = " "*NUM_INDENTS + "└── "
LINE   = " "*NUM_INDENTS + "│   "
SPACE  = " "*NUM_INDENTS + "    "

def make_line(lst):
    result = ""
    for item in lst:
        if item == 0:
            result += SPACE
        elif item == 1:
            result += LINE
    return result

def make_branch(item, depth, shape=BRANCH):
    return make_line(depth) + shape + item + "\n"

def explore_directory(directory, depth=[]):
    result = ""
    items = os.listdir(directory)
    items.sort()
    for index, item in enumerate(items):
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            if index == len(items) - 1:
                result += make_branch(item, depth, shape=LEAF)
                add_depth = 0
            else:
                result += make_branch(item, depth)
                add_depth = 1
            result += explore_directory(path, depth + [add_depth])
        else:
            if index == len(items) - 1:
                result += make_branch(item, depth, shape=LEAF)
                depth = depth[:-1]+[0]
            else:
                result += make_branch(item, depth)
    return result

def output_directory_structure(directory):
    structure = explore_directory(directory)
    with open("directory_structure.txt", "w", encoding="utf-8") as file:
        file.write(directory + "\n")
        file.write(structure)

current_directory = os.getcwd()
output_directory_structure(current_directory)
```

#### run.bat
```cmd
python directory-structure-diagram.py
```

## Summary
I introduced two methods for creating directory structure diagrams, suitable for different situations.  
I hope you find this helpful!