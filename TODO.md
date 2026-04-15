# CloudFund Render Deployment TODO

## Steps (Approved Plan)

- [x] 1. Create requirements.txt with Django, gunicorn, psycopg2-binary, whitenoise
- [x] 2. Create Procfile with 'web: gunicorn cloudfund.wsgi'
- [x] 3. Edit cloudfund/settings.py: 
  - Add env handling for SECRET_KEY and DEBUG
  - Set ALLOWED_HOSTS = ['*']
  - Add STATIC_ROOT = BASE_DIR / 'staticfiles'
  - Add Whitenoise for static
- [x] 4. Install: pip install -r requirements.txt
- [x] 5. Test: python manage.py collectstatic --noinput --dry-run
- [x] 6. Test run: gunicorn cloudfund.wsgi
- [x] 7. Check migrations: python manage.py showmigrations
- [ ] 8. Render: Set env vars (SECRET_KEY new gen, DEBUG=False), Build/Start cmds, deploy

