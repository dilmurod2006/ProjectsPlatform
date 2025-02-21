from nanoid import generate


def generate_id():
    return generate(
        alphabet="_-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",size=16)
print(len("Gle8bDtDPDdLt57O"))