from re_common.facade.mysqlfacade import MysqlUtiles

strings = """
        host = 192.168.30.209
        user = root
        passwd = vipdatacenter
        db = data_gather_record
        port = 3306
        chartset = utf8
        """

dicts_change = {"key为原来的": "values为现在的"}

from re_common.baselibrary.tools.stringtodicts import StringToDicts

dicts = StringToDicts().string_to_dicts_by_equal(strings)
mysqlutils = MysqlUtiles("", "", builder="MysqlBuilderForDicts", dicts=dicts)