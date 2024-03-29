class ServerConfig(object):
    """docstring for Config"""

    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    # SQLALCHEMY_POOL_RECYCLE = 3600
    # SQLALCHEMY_POOL_SIZE = 40

    HASH_SALT = 'v\xffz\x8e\xdc\xf9\xe1^[\x18E\x0e/\xb1\xfb\xdbjt\xd6m\xbd\x94\xfe"w\xf0\xde\xa3\xa7\xfa#%\x0b\xcb@\xf6@\xdc(\x9a\xe5\xfc\x9f\xc8\xc7\x9d"K\x1f[\xa8]\xc7^\xcb\x9ar\\\xb1\xce\x13U\x87{'
    SECRET_KEY = "1\xcf\xda\xe3\x81\x8a\xde,\x15\x16\xe32\xbdU,\xf5v\xfdr\xa1 \xcf{r\x9b_\xa5\x87\x1e\x06Bz\xf2)F{\x14\xb5\xfe/\x0bf\x88\x06&\x9a\x8a\xc5\xe6lk\x1c\xa2k%\x1c\xa6\xa6\x97\x81\xbc?!\xf2'\x9c=\xbbo\xfe\xf4K\x88\xbd\x9ah\xa9\x80\xa0\xa7\x85i\x8d\xa3\xe2\xaf<TYY\xf7\xc9\x01\x89\x0c\x93Q\xd8\xb5\xb9\x92T\x03l\xeb\x1e\xbf.\xb5\x07qn&\x8aK\xc9\xf1\xe1-\xf6I\xc0\xa4\xcc\xa6\xaez>"
    JWT_SECRET_KEY = '\xe3\xcd\x8an\x02f\x11\x89\x96\xc7W\x18_\xa2\xbaY\xc3\xde\x80\xad\xf8c\xed\x98&\xca\xa7\xb8\x99)(l\xa0^-\xf5\xc7v\xaf`O\xac+\xe4\x0e\xa4\x8c4\x98\x8b\xd0y`\x89>\x0e\x99u\xa0\xe5\x1e\xa7h\x82\xa8\x90%\xbb\xef\xa0/\xd1\xc9Qxq\xf14\xb4\xfd\xd7\xda9`\xe3\xb6s\xca\xb2\x89\xa4\xf5\x94\x01H\xe4\tZ\xd8\x93l\xe4\xe6i+\x9d\xb2M\r|K\x8e@5W}\xf31p\x8c$\xdcN\x91k\x98Pv'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    STATIC_VERSION = "1"