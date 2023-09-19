# llama-index-bug-report
This is code to reproduce the issue reported here: https://github.com/jerryjliu/llama_index/issues/7724

To run the reproduction scenario you will need to do the following (note: these instructions likely only work on linux/osx and will need to be adapted to windows):
1. Install pipenv as follows: ```pip install --user pipenv``` - after the install make sure pipenv is in your path as follows: ```pipenv -h```.  If it isn't in your path then you may have to add it.  Look here for instructions: https://pipenv.pypa.io/en/latest/installation/
2. Clone this repo and cd into it
3. Install all dependencies by running ```pipenv install --dev```
4. Copy .env.development to .env.development.local and fill in the required env vars
5. To run the fastapi server do ```pipenv run uvicorn main:app --reload --env-file .env.development.local```
6. To see the issue reproduced go to another terminal window and run ```curl localhost:8000/query```
7. With v0.7.23 of llama-index you will see it work.  With v0.7.24.post1 and any later version you will see it hang.
8. To switch between different versions of llama-index update the version in the Pipfile and then run ```pipenv update```
   
