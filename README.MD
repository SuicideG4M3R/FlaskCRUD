## Flask CRUD

---

### How to run it?
First, clone it:
```bash
git clone https://github.com/SuicideG4M3R/FlaskCRUD.git
```
Enter directory:
```bash
cd FlaskCRUD
```
Run:
```bash
python app.py
```
you can also use the following:
```bash
flask run
```
Application uses **flask_sqlalchemy**, creates new sqlite database in project directory\
creates simple model User and saves your changes.

| Operation  |                     url                     |
|:-----------|:-------------------------------------------:|
| **C**reate | ```'/create-user'```, ```/generate-users``` |
| **R**ead   |   ```'/users'``` , ```'/user/<int:id>'```   |
| **U**pdate |         ```'/user/<int:id>/edit'```         |
| **D**elete |        ```'/user/<int:id>/delete'```        |

