# ProjectsPlatform
    projectsplatform.uz 2024



# Accounts
    Models:
        ForRegister:
            id: Primey Key
            tg_id: nullable=True
            phone: str
            token: ganarate
            created_at: datetime.now
            expires_at: datetime.now+time
        
        Users:
            id: Primey Key
            full_name: str
            sex: Boolean
            email: email
            phone: strs
            username: str
            password: str
            tg_id: BigInteger
            balace:default=0 add paymaent by admin 
            created_at: datetime.now
            updated_at: datetime.now
            last_login: datetime.now
            code: nullable=True
            how_online: Boolean
            token: str
        ReportsBalance:
            user_id: Foregin Key from Users
            size: kirim(+) or Chiqim(-)
            date:datetime.now
            bio: str nullable=True
        Products:
            user_id: int, primary_key=True
            name: str
            bio: str
            price: int

    Functions:
        refresh_user_api:
            post:
                user_id: str
                old_token: str
            refresh user.token
            except:
                new_token
        about_account:
            post:
                token: str
            responce:
                full_name: str
                sex: Boolean
                email: email
                phone: strs
                username: str
                password: str
                tg_id: Foregin Key from ForRegister in tg_id
                balace:default=0 add paymaent by admin
        for_register_bot_api:
            post:
                phone: str
                tg_id: int
            ForRegister.create(phone, tg_id, generate_token)
            response:
                token: ganarated token
        cheack_token_api:
            post:
                token: str
            response:
                True or False

        register_api:
            post:
                full_name: str
                sex: Boolean
                email: str
                username: str
                password: str
                token: str

            response:
                created account sucssessfull and redirect to login


        get_code_api:
            post:
                username: str
                password: str
            response:
                True or False

        login_api:
            post:
                username: str
                code: cheack code from Users.code
            response:
                True or False
                DAVOMI BOR...
                
                




# Kundalikcom
    Models:
        SchoolData:
            user_id: Foregin Key from Users in Accounts
            viloyat: str
            tuman:str
            school_number:str
        PcKundalikCom:
            user_id: Foregin Key from Users in Accounts
            token: ganarate
            start_active_date: datetime.now
            end_active_date: end_active_dateq
            device_id: str
            end_use_date: datetime
        MobileKundalikCom:
            user_id: Foregin Key from Users in Accounts
            start_active_date: datetime.now
            end_active_date: end_active_dateq
            device_id: str
        LoginsData:
            user_id: Foregin Key from Users in Accounts
            login: str
            password: str
        MajburiyObuna:
            user_id: Foregin Key from Users in Accounts
    FunctionsPC:
        buy_api:
            post:
                token: user tokeni
                months_count: int
            responce:
                how:
                    True or False
                message:
                    "Balansingizga yetarli mablag' mavjud emas!"
                    "To'lov muvaffaqiyatli amalga oshirildi."
                    "Nimadur xato ketdi"
        price_months:
            post:
                months_count: int
            responce:
                all so'm months
        check_pc:
            post:
                device_id: str
                token: str
            responce:
                how: True or False
                end_date: "2025-yil, 2-Sentabr gacha"
                size: "10 oyu 12 kun" or "0"
                users:
                    json -> "[login parollar]"
                    bunda -> {"login": str, "password": str}
                message: "" or "Xatolik haqida habar"
        login_user:
            post:
                token: str
                device_id: str
            responce:
                how: True or False
                message: "" or "Xatolik haqida habar"
        


# TestMax
    TeachersModel:
        user_id: Foregin Key from Users in Accounts
        subjects: choice(fanlar.list)
        start_active_date: datetime.now
        end_active_date: end_active_dateq
        device_id: str
    EdecationCenters:
        user_id: Foregin Key from Users in Accounts
        start_active_date: datetime.now
        end_active_date: end_active_dateq
        device_id: str


# Aloqa -----> keyinchalik
# Admin Panel
    Models:
        Admins:
            id: Primey Key
            username: str
<<<<<<< HEAD
            password: str
=======
            password: str 
>>>>>>> c936c837bdd2ad782f1e4a9190ec13718fb8c62a
            tg_id: int
            created_at: datetime.now
            updated_at: datetime.now
            token: str
        Products:
            id: int primary_key=True
            name: str
            about: str
            settings: str json
    Functions:
        is_admin:
            post:
                token: str
            responce:
                True or False # tokenga mos admin bor yuqligini tekshiradi
        add_admin:
            post:
                token: str
                username: str
                password: str
                tg_id: int
            responce:
                how: Boolean
                token: str
        remove_admin:
            post:
                token: str
                id: str
            responce:
                True or False
        set_product:
            post:
                token: str
                id: int
                name: str
                about: str
                settings: str json
            responce:
                how: True or False
                message: "" or "Xatolik haqida matn"
        add_product:
            post:
                token: str
                name: str
                about: str
                settings: str json
            responce:
                how: True or False
                id: int
        remove_product:
            post:
                token: str
                id: int
            responce:
                how: True or False
                message: "Muvaffaqiyatli o'chirildi" or "Bunday product mavjud emas!"
        about_product:
            post:
                id: int
            responce:
                how: True
                name: str
                about: str
                settings: str json
                # or
                how: False
                message: Ayni paytda bunday product mavjud emas!
        

        
            



