# Team 10 Application

Flask site for CSC 648-848, Fall 2026, Section 01, Team 10. For Milestone 0 it
serves the team ABOUT page plus one page per team member.

Everyone's local environment must match the deployment server. Use **Python 3.12**
and run behind **Gunicorn** locally, exactly as the server does.

## Layout

```
application/
├── app/
│   ├── __init__.py             app factory, team info, .env loading
│   ├── members.py              reads members/*.json
│   ├── routes.py               / and /members/<username>
│   ├── static/css/style.css    shared stylesheet
│   ├── static/img/members/     individual photos
│   └── templates/
│       ├── base.html           shared header and footer
│       ├── index.html          the ABOUT page with one button per member
│       ├── member.html         default individual page
│       └── members/            optional hand-written individual pages
├── members/                    one JSON file per team member
├── deploy/                     nginx and systemd configuration
├── tests/                      pytest suite
├── requirements.txt            pinned to the approved stack
└── wsgi.py                     Gunicorn entry point
```

The home page discovers members by globbing `members/*.json`, so **no shared file
lists the team**. Adding yourself touches only files that belong to you, which is
what keeps our branches from conflicting when we merge.

## Local setup

Run these once, from the `application/` directory:

```bash
# 1. Confirm you have Python 3.12 (matches the server). On macOS: brew install python@3.12
python3.12 --version

# 2. Create and activate the virtual environment
python3.12 -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate

# 3. Install the pinned stack
pip install -r requirements.txt

# 4. Create your local secrets file at the repository root
cp ../.env.example ../.env          # then fill in the values
```

`venv/` and `.env` are both git-ignored. **Never commit `.env`.**

Run the site the same way the server does:

```bash
gunicorn --bind 127.0.0.1:8000 wsgi:app
```

Then open <http://127.0.0.1:8000>. For auto-reload while editing, `python wsgi.py`
works too, but test with Gunicorn before you push.

Checks to run before opening a pull request:

```bash
pytest          # every member page must return 200 and show a name and an image
ruff check .    # lint
ruff format .   # formatting
```

## Adding your own page

Each member does this individually, on their own branch.

1. Branch off `master`:
   ```bash
   git switch -c member/<your-github-username>
   ```
2. Edit **your** file in `members/`, named after your GitHub username in lowercase
   (for example `members/menpeko.json`). Fill in `headline` and `bio`.
3. Optional but recommended: add a photo to `app/static/img/members/`, named after
   your username (for example `menpeko.jpg`), and set `"photo": "menpeko.jpg"` in
   your JSON. Leave `"photo": null` to use the placeholder avatar.
4. Optional: for full control over your page's HTML, create
   `app/templates/members/<your-username-lowercase>.html`. Copy
   `app/templates/members/menpeko.html` as a starting point. If you skip this step,
   `member.html` renders your JSON with the shared layout.
5. Verify locally with `pytest` and by loading
   <http://127.0.0.1:8000/members/your-username>.
6. Push and open a pull request against `master`:
   ```bash
   git add members/<you>.json app/static/img/members/<you>.jpg app/templates/members/<you>.html
   git commit -m "Add <your name> member page"
   git push -u origin member/<your-github-username>
   ```

Only use HTML5, CSS3, and vanilla JavaScript. No React or Vue, per the approved
tech stack.

## Deploying to the server

SSH into the Ubuntu 24.04 EC2 instance and run:

```bash
curl -fsSL https://raw.githubusercontent.com/MenPeko/CSC648-S01-FA26-10-Repository/master/application/deploy/bootstrap.sh | sudo bash
```

`deploy/bootstrap.sh` installs the packages, clones the repository to
`/srv/CSC648-S01-FA26-10-Repository`, builds the virtual environment, generates a
production `.env`, starts Gunicorn under systemd, installs the Nginx site, and
verifies the result. It is safe to re-run: after the first run it updates the
checkout to the latest `master`, so it doubles as the redeploy command.

Re-run it after every pull request merge:

```bash
sudo bash /srv/CSC648-S01-FA26-10-Repository/application/deploy/bootstrap.sh
```

The script cannot change AWS settings. The instance's security group must allow
inbound TCP 80 (and 443 once HTTPS is set up) from `0.0.0.0/0`, plus 22 for SSH.
The site is then reachable at
<http://ec2-13-52-242-59.us-west-1.compute.amazonaws.com>.

To diagnose whether an unreachable site is AWS or the application: if the script
reports `Nginx on 127.0.0.1:80 -> 200` but the public URL times out, the security
group is the problem, not the code.

Two follow-ups on the address:

- That auto-assigned hostname changes whenever the instance is stopped and
  started. Allocate an **Elastic IP** and associate it with the instance so the
  URL we hand in stays valid, then update `server_name` in
  `deploy/nginx-team10.conf` and the Application URL in the root README.
- HTTPS needs a domain we control. Let's Encrypt refuses to sign
  `*.compute.amazonaws.com` names, so `certbot` cannot secure the address above.
  Once we point a real domain at the Elastic IP, run:
  ```bash
  sudo certbot --nginx -d <our-domain>
  ```

Troubleshooting:

```bash
sudo systemctl status team10        # is Gunicorn running?
sudo journalctl -u team10 -n 50     # application logs and tracebacks
sudo tail -f /var/log/nginx/team10.error.log
```

If a page loads but is unstyled, the `/static/` alias in `deploy/nginx-team10.conf`
does not match where the repository is checked out.
