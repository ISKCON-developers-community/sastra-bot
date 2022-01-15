from config import ROOT_ID


class Users:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
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
