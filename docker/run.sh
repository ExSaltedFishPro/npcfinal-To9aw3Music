python3 copyflag.py
rm -rf copyflag.py
python3 rm_ds_store.py .
rm -rf rm_ds_store.py

gcc -o /readFlag /readFlag.c
chown root:root /readFlag && chmod 4755 /readFlag
rm -rf /readFlag.c
rm -rf /etc/nginx/sites-enabled/default

chown -R app:app /app/app.py
unset FLAG


service nginx start & \
su -s /bin/bash app -c "python3 app.py" & \
cd vite && \
su -s /bin/bash app -c "npx vite --host 0.0.0.0"
