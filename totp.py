# 
# conda env export -n <env-name> > environment.yml

import hmac, base64, struct, hashlib, time, secrets

def get_hotp_token(secret, random_seq, intervals_no):
    intervals_no = int(str(intervals_no) + random_seq)
    print('intervals_no = ', intervals_no)
    key = base64.b32decode(secret, True)
    print('Key = ', key)
    #decoding our key
    msg = struct.pack(">Q", intervals_no)
    print('Msg = ', msg)
    #conversions between Python values and C structs represente
    h = hmac.new(key, msg, hashlib.sha1).digest()
    print('h = ', h[19])
    o = o = h[19] & 15
    print('o = ', o)
    #Generate a hash using both of these. Hashing algorithm is HMAC
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    print("second h = ", h)
    #unpacking
    return h
def get_totp_token(secret, random_seq):
    #ensuring to give the same otp for 30 seconds
    x =str(
      get_hotp_token(
        secret, 
        random_seq,
        int(time.time())//120, 
        ))
    print('Full x = ', x)
    #adding 0 in the beginning till OTP has 6 digits
    while len(x)!=6:
        x+='0'
    return x
#base64 encoded key


# Generate seed
seed = secrets.token_hex(32)

# Generate secret key
m = hashlib.sha256(str.encode(seed))
m.digest()
hex_string = m.hexdigest()
secret_key = base64.b32encode(bytearray(hex_string, 'ascii')).decode('utf-8')

# No need to regenerate, use the 'users' secret key
secret_key = "HA2GKZBRGM2GINRQGM3TGYRUGNQTMYZYGZSDKMJWMZQTEZRYGU2DSZJTMZQWCMBQGY2GCZBZMZRDOMTDGM3TKMRXHA4TAZBSGMZGCZQ="



print(get_totp_token(secret_key, "0000"))