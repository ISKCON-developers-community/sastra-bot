from config import ROOT_ID, logfile, users_db_file


def get_id_from_log(string: str):
    try:
        user_id = string.split()[3]
        user_id = int(user_id)
    except Exception:
        return None
    else:
        return user_id


class Users:
    def __init__(self) -> None:
        self.file_name = users_db_file
        self.users = self.__get_users_from_file()

    def __get_users_from_file(self) -> set[int]:
        try:
            with open(self.file_name) as f:
                lines = f.readlines()
        except:
            return set()
        else:
            return set([int(l) for l in lines])

    def add_user(self, user_id: int) -> None:
        l = len(self.users)
        if user_id != ROOT_ID:
            self.users.add(user_id)
        if l < len(self.users):
            with open(self.file_name, 'a') as f:
                print(user_id, file=f)

    def from_log_to_db(self):
        with open(logfile, 'r') as f:
            users = [get_id_from_log(l)
                     for l in f.readlines() if get_id_from_log(l)]
            for user in users:
                self.add_user(user)


if __name__ == '__main__':
    db = Users()
    db.from_log_to_db()
