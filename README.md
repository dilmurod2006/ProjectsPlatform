# ProjectsPlatform
projectsplatform.uz 2024



# Accounts
    Models:
        ForRegister:
            id: Primey Key
            tg_id: nullable=True
            phone: str
            token: ganarate
            timer: session
        
        Users:
            id: Primey Key
            full_name: str
            sex: Boolean
            email: email
            phone: strs
            username: str
            password: str
            tg_id: Foregin Key from ForRegister in tg_id
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
    Functions:
        refresh_user_api:
            post:
                user_id: str
                old_token: str
            refresh user.token
            except:
                new_token
        about_account_api:
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
            psost:
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
    Functions:
        buy_api:
            post:
                months_count: int
                token: user tokeni
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
    Admins:
        id: Primey Key
        username: str
        password: str 
        tg_id: int
        active: Boolean
        created_at: datetime.now
        updated_at: datetime.now



