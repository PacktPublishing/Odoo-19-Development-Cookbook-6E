# Chapter 01 – Odoo 19 Development Environment (Command Reference)

This document contains **all command-line commands and configuration steps** used in Chapter 01.
---

# Table of Contents

1. System Update & Core Dependencies  
2. Install wkhtmltopdf  
3. PostgreSQL Installation & Configuration  
4. Git Configuration  
5. Clone Odoo 19 Source Code  
6. Python Virtual Environment  
7. Install Python Requirements  
8. Create Database & Start Odoo  
9. Optional: Node.js & RTL Support  
10. Nginx Installation & Load Balancing  
11. PostgreSQL Performance Tuning  
12. Odoo Configuration File  
13. Database Management via CLI  
14. Debugging & Development  
15. Update Add-on Modules List  
16. Quick Start Summary  

---

# 1. System Update & Core Dependencies

```bash
sudo apt-get update
sudo apt install -y openssh-server fail2ban python3-pip python3-dev python3-venv \
libxml2-dev libxslt1-dev zlib1g-dev libsasl2-dev libldap2-dev build-essential \
libssl-dev libffi-dev libmysqlclient-dev libpq-dev libjpeg-dev liblcms2-dev \
libblas-dev libatlas-base-dev git curl
```

---

# 2. Install wkhtmltopdf (Required for PDF Reports)

```bash
sudo apt update
sudo apt install -y fontconfig libxrender1 xfonts-75dpi xfonts-base

wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
sudo dpkg -i wkhtmltox_0.12.6.1-2.jammy_amd64.deb
sudo apt-get install -f
```

---

# 3. PostgreSQL Installation & Configuration

Install PostgreSQL:

```bash
sudo apt install postgresql -y
```

Create PostgreSQL user (same as Linux user):

```bash
sudo -u postgres createuser -s $USER
sudo -u postgres psql -c "ALTER ROLE $USER WITH PASSWORD 'your_password';"
```

---

# 4. Git Configuration

```bash
git config --global user.name "Your Name"
git config --global user.email youremail@example.com
```

---

# 5. Clone Odoo 19 Source Code

```bash
mkdir ~/odoo-dev
cd ~/odoo-dev
git clone -b 19.0 --single-branch --depth 1 https://github.com/odoo/odoo.git
```

---

# 6. Python Virtual Environment

Create virtual environment:

```bash
python3 -m venv ~/venv-odoo-19.0
```

Activate it:

```bash
source ~/venv-odoo-19.0/bin/activate
```

---

# 7. Install Python Requirements

```bash
cd ~/odoo-dev/odoo/
pip3 install -r requirements.txt
```

---

# 8. Create Database & Start Odoo

Create database:

```bash
createdb odoo-test
```

Start Odoo:

```bash
python3 odoo-bin -d odoo-test -i base --addons-path=addons --db-filter=odoo-test$
```

Alternative:

```bash
./odoo-bin -d odoo-test -i base --addons-path=addons --db-filter=odoo-test$
```

Access in browser:

```
http://localhost:8069
```

Default credentials:

```
Username: admin
Password: admin
```

---

# 9. Optional: Node.js & RTL Support

```bash
sudo apt-get install nodejs npm -y
sudo npm install -g rtlcss
```

---

# 10. Nginx Installation & Load Balancing

Install Nginx:

```bash
sudo apt update
sudo apt install nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

Test configuration:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Example Load Balancer Configuration:

```bash
sudo nano /etc/nginx/conf.d/odoo_loadbalancer.conf
```

```nginx
upstream odoo_backend {
    server 127.0.0.1:8069;
    server 127.0.0.1:8070;
}

server {
    listen 80;
    server_name odoo.yourdomain.com;

    location / {
        proxy_pass http://odoo_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

# 11. PostgreSQL Performance Tuning

Edit PostgreSQL configuration:

```bash
sudo nano /etc/postgresql/*/main/postgresql.conf
```

Recommended baseline:

```conf
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB
max_connections = 100
checkpoint_completion_target = 0.9
wal_buffers = 16MB
checkpoint_timeout = 10min
max_wal_size = 1GB
random_page_cost = 1.1
effective_io_concurrency = 200
default_statistics_target = 100
```

Apply changes:

```bash
sudo systemctl reload postgresql
sudo systemctl restart postgresql
```

Verify:

```bash
sudo -u postgres psql
SHOW shared_buffers;
SHOW effective_cache_size;
SHOW work_mem;
```

---

# 12. Odoo Configuration File

Generate config file:

```bash
./odoo-bin --save --config myodoo.cfg --stop-after-init
```

Run with config:

```bash
./odoo-bin -c myodoo.cfg
```

Recommended production config:

```ini
[options]
workers = 4
db_maxconn = 64
limit_memory_hard = 2684354560
limit_memory_soft = 2147483648
limit_request = 8192
limit_time_cpu = 60
limit_time_real = 120
log_level = info
logfile = /var/log/odoo/odoo.log
admin_passwd = your_secure_master_password
list_db = False
```

Worker formula:

```
workers = (CPU cores × 2) + 1
```

---

# 13. Database Management via CLI

Create & start:

```bash
createdb testdb && odoo-bin -d testdb
```

Duplicate:

```bash
createdb -T dbname newdbname
cp -r ~/.local/share/Odoo/filestore/dbname ~/.local/share/Odoo/filestore/newdbname
```

Delete:

```bash
dropdb dbname
rm -rf ~/.local/share/Odoo/filestore/dbname
```

Backup:

```bash
pg_dump -Fc -f dbname.dump dbname
tar cjf dbname.tgz dbname.dump ~/.local/share/Odoo/filestore/dbname
```

Restore:

```bash
tar xf dbname.tgz
pg_restore -C -d dbname dbname.dump
```

---

# 14. Debugging & Development

Enable module-specific logging:

```bash
./odoo-bin --log-handler=odoo.addons.my_module:DEBUG
```

Python breakpoint:

```python
import pdb; pdb.set_trace()
```

Enable full debug mode:

```bash
./odoo-bin --dev=all
```

---

# 15. Update Add-on Modules List (UI)

Apps → Update Apps List → Update

---

# 16. Quick Start Summary

```bash
source ~/venv-odoo-19.0/bin/activate
cd ~/odoo-dev/odoo
./odoo-bin -d odoo-test -i base --addons-path=addons
```

Open:

```
http://localhost:8069
```
