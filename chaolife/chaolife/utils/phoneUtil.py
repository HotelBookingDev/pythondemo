# -*- coding:utf-8 -*-
"""
*手机号码
*移动：134[0 - 8], 135, 136, 137, 138, 139, 150, 151, 157, 158, 159, 182, 187, 188
*联通：130, 131, 132, 152, 155, 156, 185, 186
*电信：133, 1349, 153, 180, 189
* /
"""


def phone_is_legal(phone_number):
    # phoneprefix=['130','131','132','133','134','135','136','137','138','139','150','151','152','153',
    #              '156','157','158','159','170','183','182','185','186','188','189']
    if len(phone_number)!=11:
        return False
    else:
        # 检测是否全部是数字
        if phone_number.isdigit():
            if phone_number[0] == '1':
                return True
            else:
                return False

