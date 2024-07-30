import hashlib

def generate_manabu_token(input_string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    return sha256_hash.hexdigest()

input_string = 'beaabca38e0074f688cd119f68b3bd88-1cc4db1a3d7b1837d6538ca6cabed338-a81f3b9bcdd80a361c14af38dc09b309-7950ec0297c12322859860922e071362-619e17dc65ef9d4673a29e983f6a4dc9-b982a366e51fb7a2c53d3bfcc8283d52-0b82c67d2c389d0d50367f1f13b7a8f7-02f1239a30ddfac702d449f6e09bfc3f-a81f3b9bcdd80a361c14af38dc09b309-442d4e5c08bab4e7c0516508afe0f400-7a502a49c3fd5ac8d1b845c2031ede1c'
manabu_token = generate_manabu_token(input_string)

print('Generated Manabu Token:', manabu_token)
