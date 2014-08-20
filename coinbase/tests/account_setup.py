from coinbase import CoinbaseAccount


def without_auth():
    return CoinbaseAccount()


def with_key():
    return CoinbaseAccount(api_key=api_key)


def with_oauth():
    # Don't actually set up oauth2 credentials, because this will fail if
    # we're testing under python3. Some day when we have an oauth2 client
    # that supports python 3, we can change this.
    a = CoinbaseAccount()
    a.authenticated = True
    a.auth_params = {}
    return a


api_key = ('f64223978e5fd99d07cded069db2189a'
           '38c17142fee35625f6ab3635585f61ab')

oauth_json = """
{
    "_class": "OAuth2Credentials",
    "_module": "oauth2client.client",
    "access_token":
        "c15a9f84e471db9b0b8fb94f3cb83f08867b4e00cb823f49ead771e928af5c79",
    "client_id":
        "2df06cb383f4ffffac20e257244708c78a1150d128f37d420f11fdc069a914fc",
    "client_secret":
        "7caedd79052d7e29aa0f2700980247e499ce85381e70e4a44de0c08f25bded8a",
    "id_token": null,
    "invalid": false,
    "refresh_token":
        "90cb2424ddc39f6668da41a7b46dfd5a729ac9030e19e05fd95bb1880ad07e65",
    "revoke_uri": "https://accounts.google.com/o/oauth2/revoke",
    "token_expiry": "2014-03-31T23:27:40Z",
    "token_response": {
        "access_token":
            "c15a9f84e471db9b0b8fb94f3cb83f08867b4e00cb823f49ead771e928af5c79",
        "expires_in": 7200,
        "refresh_token":
            "90cb2424ddc39f6668da41a7b46dfd5a729ac9030e19e05fd95bb1880ad07e65",
        "scope": "all",
        "token_type": "bearer"
    },
    "token_uri": "https://www.coinbase.com/oauth/token",
    "user_agent": null
}
"""
