## Video-Store
Install pip dependenices using:
```
pip install -r pip_reqs.txt
```
### Usage
- Ensure Videos folder in present in the repo folder
- Ensure all videos,sub-directories,file names are exactly same as dataset
- Ensure csv file present in the repo folder with the exact same name as dataset
- .index , .csv and /Videos can be kept in repo even during commits - .gitignore will take care
```
python main.py
```
### Dataset - SVW
Data set used is [Sports Videos in the Wild (SVW): A Video Dataset for Sports Analysis](http://cvlab.cse.msu.edu/project-svw.html)
### Repository Maintenance
- Each functionality is to be written in seperate python modules
- Each module has to be included in main.py
- main.py will be the main file used for full system and integration testing
- Update README.md and/or requirements.txt with all libraries that need to be installed. This helps all teammates to run code.
- Please add function description at the beginning of the function in triple quotes and one word for input parameter and return variable(example can be see in query_parser.py).
