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
        ReportsBalance:
            user_id: Foregin Key from Users
            size: kirim(+) or Chiqim(-)
            date:datetime.now
            bio: str nullable=True
    Functions:
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