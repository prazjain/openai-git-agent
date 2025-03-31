
#### Steps for Developers to run this app
* Create virtual environment `python3 -m venv venv`  
* Activate the env `source venv/bin/activate`  
* Install dependencies `pip install -r requirements.txt`  

### What does this code do  

For a given problem task, this code clone the repo where the solution need to reside, then it will generate python code for solving that task by interacting with LLM models, then it will push that code to github and raise a PR.  
Problem task file has to be created inside the same repo in genai-todo directory, once the task is completed, it moves this task file into genai-completed directory.  