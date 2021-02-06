from tinydb import TinyDB, where

db = TinyDB('./data/scans_db.json')
user_input = input("enter scan_id> ")


def main():
    if user_input:
        result = db.search(where('id') == user_input)
        if result:
            print(f"********** [{user_input}] **********\n")
            print(f"[{user_input}] STATUS : {result[0]['status']} ")
            print(f"[{user_input}] TTL : {result[0]['ttl']}\n")
            print(f"********************************\n")
        else:
            print(f"[{user_input}] Not-Found")
    else:
        print(f"[ERROR] Input not valid")


if __name__ == "__main__":
    main()
