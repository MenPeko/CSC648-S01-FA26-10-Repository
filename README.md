# CSC648-S01-FA26-team10 Repository

**Application URL: <https://example.com>**

## Before completing Milestone 0

1. On the Github classroom invite link, you will only have to enter your `team number` everything else is a prefix.
2. The name of the repository should look like csc648-S0X-FA24-teamNN.
   - S0X will be one of 01 or 04 (Already prefilled).
   - teamNN should be your team number. Team numbers whose value is less than
     10, please pad with a 0 (e.g. team 1 is Team01 team 11 is Team11). Please
     make sure to also **remove the username from the repository as well**!
     Teams with an incorrectly named repository will have points deducted from
     their milestone 0 grades.
   - Examples: `csc648-04-sp24-Team01`, `csc648-01-sp24-Team05`
3. Add ALL members of your team to this repository. For it to count, **they must
   ACCEPT the invite**.
4. Fill out the table below

| Student Name | Student Email | GitHub Username | Student's role |
| :----------: | :-----------: | :-------------: | :------------: |
|   John Doe   | jdoe@sfsu.edu |      jdoe       |  Team Leader   |

**NO code should be stored in the root of your repository. You may rename the
`application/` folder to your team's application name if you'd like, but all the
source code should be stored inside that folder.**


## Current Approved CTO/CEO Tech Stack 
Server Host: AWS EC2, t3.micro (2 vCPU, 1 GB RAM)
Operating System: Ubuntu Server 24.04 LTS
Database: MySQL 8.0
Web Server: Nginx 1.24.0
Server-Side Language: Python 3.12

Additional Technologies:
Web Framework: Flask
Templates: Jinja2
Application Server: Gunicorn, managed by systemd
Database Driver: PyMySQL
Database Layer: SQLAlchemy
Database Migrations: Alembic
Authentication: Flask-Login, with password hashing from werkzeug.security
Form Security: Flask-WTF
Frontend: HTML5, CSS3, vanilla JavaScript (no React or Vue)
Testing: pytest
Code Formatting: ruff
Environment: python3-venv with a pinned requirements.txt
SSL Certificate: Let's Encrypt (Certbot)
Version Control: Git / GitHub
