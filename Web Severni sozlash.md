# SSH ULANISH:
    username: root
    ip address: 45.138.158.199
    password:ProjectsPlatformAdmin

# Tizimni yangilash har safar qilinishi kerak ish!
    1. Paketlar ro'yxatini yangilash:
        sudo apt update

    2. O'rnatilgan paketlarni yangilash:
        sudo apt upgrade
    
    3. Barcha paketlarni va tizimni yangilash (optsional):
        sudo apt full-upgrade
    
    4. Tizimni qayta yuklash:
        sudo reboot

# PostgreSQL ma'lumotlar bazasini o'rnatish:
    1. sudo apt install postgresql
    2. sudo apt install -y postgresql-common
    3. sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
    4. sudo systemctl start postgresql
    5. sudo systemctl enable postgresql


# Nginx serverni yuklash:
    1. Nginx paketini o'rnating:
        sudo apt install nginx

    2. Nginx xizmatini ishga tushiring va avtomatik boshlanishini ta'minlang:
        sudo systemctl start nginx
        sudo systemctl enable nginx
    
    3. Nginx holatini tekshiring:
        sudo systemctl status nginx
    
    4. Nginx qayta ishga tushiring:
        sudo systemctl restart nginx

# SSL sertifikat olish:
    1. SSL sertifikat olish:
        sudo apt install certbot
        sudo apt-get install python3-certbot-nginx
<<<<<<< HEAD
        sudo certbot --nginx



<!-- SSH ORQALI FILELAR VVA FOLDER O'TKAZISH -->

# SSH orqali file o'tkazish severga
    folder o'tkzish:
        1. scp -r /local/folder/path username@remote_host:/remote/folder/path
    
    file o'tkzish:
        1. scp /local/file/path username@remote_host:/remote/file/path
    
    EXAMPLE:
        1. Folder o'tkazish:
            scp -r C:/Users/dilmu/ProjectsPlatform root@45.138.158.199:/projects/

        2. File o'tkazish:
            scp C:/Users/dilmu/ProjectsPlatform/bot.py root@45.138.158.199:/projects/ProjectsPlatform/bot.py
=======
        sudo certbot --nginx
>>>>>>> 340a437b1ce802d8b37f0b8f3be24dddc7446c85
