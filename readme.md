# vtu internship diary fill automatation using playwright
1. Create python environment by doing
```
python -m venv venv
```
or
```
python3 -m venv venv
```
2. Activate the python environment before installing the requirements.
```
.\venv\scripts\activate.ps1
```
3. Install dependencies.  
```
pip install -r requirements.txt 
```  
4. create `.env` file and copy the variables from `.env.example`  
5. Edit work hour in `config.py` if needed.  
6. Run the server  
```
python server.py
```
7. Select start date and end date (I prefer 1 month at a time)  

8. Select holidays to avoid generating content for those days (It should sound legitimate :-\ )  

9. Review content once (check dates and content) and Save it.  
(It will save a json file like `2025-10-08_2025-11-30_internship_details.json`)  
You are free to modify the content.  

10. Select the same file from the dropdown for automation
11. Hit Run automation
12. wait for it to complete
13. profit $$$  


