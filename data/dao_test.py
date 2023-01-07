import dao
import secrets

def main():
    print(secrets.token_hex(32))

if __name__ == '__main__':
    main()