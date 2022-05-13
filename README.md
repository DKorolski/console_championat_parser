# Setup the project

## 1. Open the project folder in VS Code

## 2. In VS Code, open the Command Palette `(View > Command Palette or (Ctrl+Shift+P))`

Then select: `Python: Select Interpreter`  
Then select: `Python 3.9`  
Then select: `Python: Select Linter`  
Then select: `Flake8`

## 3. Run Terminal: `Create New Integrated Terminal (Ctrl+`))`  

``` bash
python -m venv env
env\scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Execute app.py

``` 
python console application
extracts data from https://www.championat.com/ with given list of urls
collects data into dataframe pandas
save dataset into output format - csv

```


