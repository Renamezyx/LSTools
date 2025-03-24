from dao.dao_script_storage import DaoScriptStorage
from dao.dao_users import DaoUsers


class UsersService:
    @staticmethod
    def users_insert(headers, phone, username) -> int:
        if headers is None or phone is None:
            return -1
        else:
            dao_users = DaoUsers()
            is_exit = dao_users.select(phone=phone)
            if len(is_exit) == 0:
                res = dao_users.insert((headers, username, phone))
                return res
            else:
                return -2

    @staticmethod
    def users_update(headers, phone, username, id) -> int:
        if id is None or headers is None or phone is None or username is None:
            return -1
        else:

            dao_users = DaoUsers()
            is_exit = dao_users.select(phone=phone)
            if len(is_exit) == 1:
                res = dao_users.update(headers=headers, username=username, phone=phone, id=id)
            else:
                return -1
            return res

    @staticmethod
    def users_delete(id) -> int:
        if id is None:
            return -1
        else:
            dao_users = DaoUsers()
            res = dao_users.delete(id)
            return res

    @staticmethod
    def users_select(phone=None, script_name=None) -> list:
        dao_users = DaoUsers()
        res = dao_users.select(phone=phone)

        return res
