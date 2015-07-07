# -*- coding: utf-8 -*-

def getMonthStr(mnum):
    tg = "甲乙丙丁戊己庚辛壬癸".decode('utf8')
    dz = "子丑寅卯辰巳午未申酉戌亥".decode('utf8')
    yearnum = mnum / 12 + 16
    str1 = tg[yearnum % 10] + dz[yearnum % 12]
    mnum += 14
    str2 = tg[mnum % 10] + dz[mnum % 12]
    return str1 + "_" + str2

print getMonthStr(0)