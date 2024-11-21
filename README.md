## Installing Git
1) Open your terminal and check if git is installed with the [git --version] command.
2) If it isn't already installed, type [xcode-select --install]. 
3) then simply type [git clone https://github.com/AnilTek/DjangoUploadProject.git] to install the project. 
## Creating a virtual environment 
1) Go to the directory of the project in VScode
2) Use the [python3 -m venv myvenv] command to create one.
3) Activate your venv with the [source myvenv/bin/activate] command
## Installing Requirements
1) There is a text file name requirement.txt. It should be requirements. txt, please rename it if you want 
2) then type [pip install -r requirements.txt]. This command will provide you the required libraries for this project. 
## Google Auth Settings
1) There is a file named [settings.py]. Under the myproject folder, please fill the [client_id and secret] section. 
## Running the Code
1) Please go to the directory where [manage.py] is, then simply write this command: [python manage.py runserver or python3 manage.py runserver].
2) [http://127.0.0.1:8000/] then paste this to go to server
## Accesing to the admin page 
1) [http://127.0.0.1:8000/admin] is where you can enter the admin portal. 
2) If there isn't any admin account, type [ctrl+c] to stop the server and write down [python manage.py createsuperuser] and create an account.


### Note: 
1) If you are on a PC instead of a Mac, there is no reason to create a new virtual environment; you can just use the existing one.
2) This guideline already assumes that you have both [Visual Studio Code and Python] installed in your computer; if it is not, please first install these two.
