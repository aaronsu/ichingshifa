# -*- coding: utf-8 -*-#
import json
import pickle, random, datetime, os, itertools
import numpy as np
import sxtwl


class Iching():
    # 64卦、4096種卦爻組合資料庫，爻由底(左)至上(右)起
    def __init__(self):
        base = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(base, 'data.pkl')
        self.data = pickle.load(open(path, "rb"))
        self.sixtyfourgua = self.data.get("數字排六十四卦")
        self.sixtyfourgua_description = self.data.get("易經卦爻詳解")
        self.eightgua = self.data.get("八卦數值")
        self.eightgua_element = self.data.get("八卦卦象")
        self.bagua_pure_code = self.data.get("八宮卦純卦")
        self.tiangan = self.data.get("干")
        self.dizhi = self.data.get("支")
        self.wuxin = self.data.get("五行")
        self.down = self.data.get("下卦數")
        self.up = self.data.get("上卦數")
        self.gua = self.data.get("八卦")
        self.shen = self.data.get("世身")
        self.sixtyfour_gua_index = self.data.get("六十四卦")
        self.shiying2 = self.data.get("世應排法")
        self.findshiying = dict(zip(list(self.data.get("八宮卦").values()), self.shiying2))
        self.liuqin = self.data.get("六親")
        self.liuqin_w = self.data.get("六親五行")
        self.mons = self.data.get("六獸")
        self.chin_list = self.data.get("二十八宿")
        self.gua_down_code = dict(zip(self.gua, self.down))
        self.gua_up_code = dict(zip(self.gua, self.up))
        self.ymc = [11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.rmc = list(range(1, 32))

    def new_list(self, olist, o):
        zhihead_code = olist.index(o)
        res1 = []
        for i in range(len(olist)):
            res1.append(olist[zhihead_code % len(olist)])
            zhihead_code = zhihead_code + 1
        return res1

    def chin_iter(self, olist, chin):
        new_chin_list = self.new_list(olist, chin)
        return itertools.cycle(new_chin_list)

    def jiazi(self):
        tiangan = self.tiangan
        dizhi = self.dizhi
        jiazi = [tiangan[x % len(tiangan)] + dizhi[x % len(dizhi)] for x in range(60)]
        return jiazi

    def multi_key_dict_get(self, d, k):
        for keys, v in d.items():
            if k in keys:
                return v
        return None

    def find_six_mons(self, daygangzhi):
        mons = [i[1] for i in self.data.get("六獸")]
        return self.new_list(mons, self.multi_key_dict_get(
            dict(zip([tuple(i) for i in '甲乙,丙丁,戊,己,庚辛,壬癸'.split(",")], mons)), daygangzhi[0]))

    def rev(self, l):
        r = []
        for i in l:
            r.insert(0, i)
        return r

    def show_sixtyfourguadescription(self, gua):
        sixtyfourguadescription = self.sixtyfourgua_description
        return sixtyfourguadescription.get(gua)

    # 干支
    def gangzhi(self, year, month, day, hour):
        lunar = sxtwl.Lunar()
        cdate = lunar.getDayBySolar(year, month, day)
        yy_mm_dd = self.tiangan[cdate.Lyear2.tg] + self.dizhi[cdate.Lyear2.dz], self.tiangan[cdate.Lmonth2.tg] + \
                   self.dizhi[cdate.Lmonth2.dz], self.tiangan[cdate.Lday2.tg] + self.dizhi[cdate.Lday2.dz]
        timegz = lunar.getShiGz(cdate.Lday2.tg, hour)
        new_hh = self.tiangan[timegz.tg] + self.dizhi[timegz.dz]
        return yy_mm_dd[0], yy_mm_dd[1], yy_mm_dd[2], new_hh

    # 農曆
    def lunar_date_d(self, year, month, day, hour):
        lunar = sxtwl.Lunar()
        day = lunar.getDayBySolar(year, month, day)
        return {"月": self.ymc[day.Lmc], "日": self.rmc[day.Ldi]}

    def mget_bookgua_details(self, guayao):
        getgua = self.multi_key_dict_get(self.sixtyfourgua, guayao)
        yao_results = self.sixtyfourgua_description.get(getgua)
        bian_yao = guayao.replace("6", "1").replace("9", "1").replace("7", "0").replace("8", "0")
        dong_yao = bian_yao.count("1")
        explaination = "動爻有【" + str(dong_yao) + "】根。"
        dong_yao_change = guayao.replace("6", "7").replace("9", "8")
        g_gua = self.multi_key_dict_get(self.sixtyfourgua, dong_yao_change)
        g_gua_result = self.sixtyfourgua_description.get(g_gua)
        b_gua_n_g_gua = "【" + getgua + "之" + g_gua + "】"
        top_bian_yao = bian_yao.rfind("1") + int(1)
        second_bian_yao = bian_yao.rfind("1", 0, bian_yao.rfind("1")) + int(1)
        top_jing_yao = bian_yao.rfind("0") + int(1)
        second_jing_yao = bian_yao.rfind("0", 0, bian_yao.rfind("0")) + int(1)
        top = yao_results.get(top_bian_yao)
        second = yao_results.get(second_bian_yao)
        # top_2 = yao_results.get(top_jing_yao)
        # second_2 = yao_results.get(second_jing_yao)
        explaination2 = None
        try:
            if dong_yao == 0:
                explaination2 = explaination, "主要看【" + getgua + "】卦彖辭。", yao_results[7][2:]
            elif dong_yao == 1:
                explaination2 = explaination, b_gua_n_g_gua, "主要看【" + top[:2] + "】", top
            elif dong_yao == 2:
                explaination2 = b_gua_n_g_gua, explaination, "主要看【" + top[:2] + "】，其次看【" + second[
                                                                                                 :2] + "】。", top, second
            elif dong_yao == 3:
                if bian_yao.find("1") == 0:
                    explaination2 = b_gua_n_g_gua, explaination, "【" + getgua + "】卦為貞(我方)，【" + g_gua + "】卦為悔(他方)。前十卦，主貞【" + getgua + "】卦，請參考兩卦彖辭", \
                    yao_results[7][2:], g_gua_result[7][2:]
                elif bian_yao.find("1") > 0:
                    explaination2 = b_gua_n_g_gua, explaination, "【" + getgua + "】卦為貞(我方)，【" + g_gua + "】卦為悔(他方)。後十卦，主悔【" + g_gua + "】卦，請參考兩卦彖辭", \
                    g_gua_result[7][2:], yao_results[7][2:]
            elif dong_yao == 4:
                explaination2 = b_gua_n_g_gua, explaination, "主要看【" + g_gua + "】的" + g_gua_result.get(
                    second_jing_yao)[:2] + "，其次看" + g_gua_result.get(top_jing_yao)[:2] + "。", g_gua_result.get(
                    second_jing_yao), g_gua_result.get(top_jing_yao)
            elif dong_yao == 5:
                explaination2 = b_gua_n_g_gua, explaination, "主要看【" + g_gua + "】的" + g_gua_result.get(top_jing_yao)[
                                                                                         :2] + "。", g_gua_result.get(
                    top_jing_yao)
            elif dong_yao == 6:
                explaination2 = b_gua_n_g_gua, explaination, "主要看【" + g_gua + "】卦的彖辭。", g_gua_result[7][2:]
        except (TypeError, UnboundLocalError):
            pass
        return [guayao, getgua, g_gua, yao_results, explaination2]

    def bookgua(self):  # 由底至上起爻
        shifa_results = []
        for i in range(6):
            stalks_first = 50 - 1  # 一變 (分二、掛一、揲四、歸奇)
            dividers = sorted(random.sample(range(24, stalks_first), 1))
            first_division = [a - b for a, b in zip(dividers + [stalks_first + 10], [10] + dividers)]
            guayi = 1
            right = first_division[0] - guayi
            left_extract = first_division[1] % 4
            if left_extract == 0:
                left_extract = 4
            right_extract = right % 4
            if right_extract == 0:
                right_extract = 4
            yibian = left_extract + right_extract + guayi  # 二變 (分二、掛一、揲四、歸奇)
            stalks_second = stalks_first - yibian
            second_dividers = sorted(random.sample(range(12, stalks_second), 1))
            second_division = [a - b for a, b in zip(second_dividers + [stalks_second + 5], [5] + second_dividers)]
            right_second = second_division[0] - guayi
            left_extract_second = second_division[1] % 4
            if left_extract_second == 0:
                left_extract_second = 4
            right_extract_second = right_second % 4
            if right_extract_second == 0:
                right_extract_second = 4
            erbian = left_extract_second + right_extract_second + guayi  # 三變 (分二、掛一、揲四、歸奇)
            stalks_third = stalks_second - erbian
            third_dividers = sorted(random.sample(range(6, stalks_third), 1))
            third_division = [a - b for a, b in zip(third_dividers + [stalks_third + 3], [3] + third_dividers)]
            right_third = third_division[0] - guayi
            left_extract_third = third_division[1] % 4
            if left_extract_third == 0:
                left_extract_third = 4
            right_extract_third = right_third % 4
            if right_extract_third == 0:
                right_extract_third = 4
            sanbian = left_extract_third + right_extract_third + guayi
            yao = int((stalks_first - yibian - erbian - sanbian) / 4)
            shifa_results.append(yao)
        return "".join(str(e) for e in shifa_results[:6])

    def datetime_bookgua(self, y, m, d, h):
        gangzhi = self.gangzhi(y, m, d, h)
        ld = self.lunar_date_d(y, m, d, h)
        zhi_code = dict(zip(self.dizhi, range(1, 13)))
        yz_code = zhi_code.get(gangzhi[0][1])
        hz_code = zhi_code.get(gangzhi[3][1])
        cm = ld.get("月")
        cd = ld.get("日")
        eightgua = {1: "777", 2: "778", 3: "787", 4: "788", 5: "877", 6: "878", 7: "887", 8: "888"}
        upper_gua_remain = (yz_code + cm + cd + hz_code) % 8
        if upper_gua_remain == 0:
            upper_gua_remain = int(8)
        upper_gua = eightgua.get(upper_gua_remain)
        lower_gua_remain = (yz_code + cm + cd) % 8
        if lower_gua_remain == 0:
            lower_gua_remain = int(8)
        lower_gua = eightgua.get(lower_gua_remain)
        combine_gua1 = lower_gua + upper_gua
        combine_gua = list(combine_gua1)
        bian_yao = (yz_code + cm + cd + hz_code) % 6
        if bian_yao == 0:
            bian_yao = int(6)
        elif bian_yao != 0:
            combine_gua[bian_yao - 1] = combine_gua[bian_yao - 1].replace("7", "9").replace("8", "6")
        bian_gua = "".join(combine_gua)
        ben_gua = self.multi_key_dict_get(self.sixtyfourgua, bian_gua)
        description = self.multi_key_dict_get(self.sixtyfourgua_description, ben_gua)
        g_gua = self.multi_key_dict_get(self.sixtyfourgua, (bian_gua.replace("6", "7").replace("9", "8")))
        return ben_gua + "之" + g_gua, self.eightgua_element.get(upper_gua_remain) + self.eightgua_element.get(
            lower_gua_remain) + ben_gua, "變爻為" + description[bian_yao][:2], description[bian_yao][3:]

    def bookgua_details(self):
        return self.mget_bookgua_details(self.bookgua())

    # 現在時間起卦
    def current_bookgua(self):
        now = datetime.datetime.now()
        return self.datetime_bookgua(int(now.year), int(now.month), int(now.day), int(now.hour))

    def dc_gua(self, gua):
        fivestars = self.data.get("五星")
        eightgua = self.data.get("數字排八卦")
        sixtyfourgua = self.data.get("數字排六十四卦")
        su_yao = self.data.get("二十八宿配干支")
        shiying = self.multi_key_dict_get(self.data.get("八宮卦"), self.multi_key_dict_get(sixtyfourgua, gua))
        Shiying = list(self.findshiying.get(shiying))
        dgua = self.multi_key_dict_get(eightgua, gua[0:3])
        down_gua = self.gua_down_code.get(dgua)
        ugua = self.multi_key_dict_get(eightgua, gua[3:6])
        up_gua = self.gua_up_code.get(ugua)
        dt = [self.tiangan[int(g[0])] for g in [down_gua[i].split(',') for i in range(0, 3)]]
        dd = [self.dizhi[int(g[1])] for g in [down_gua[i].split(',') for i in range(0, 3)]]
        dw = [self.wuxin[int(g[2])] for g in [down_gua[i].split(',') for i in range(0, 3)]]
        ut = [self.tiangan[int(g[0])] for g in [up_gua[i].split(',') for i in range(0, 3)]]
        ud = [self.dizhi[int(g[1])] for g in [up_gua[i].split(',') for i in range(0, 3)]]
        uw = [self.wuxin[int(g[2])] for g in [up_gua[i].split(',') for i in range(0, 3)]]
        t = dt + ut
        d = dd + ud
        w = dw + uw
        find_gua_wuxing = self.multi_key_dict_get(self.data.get("八宮卦五行"),
                                                  self.multi_key_dict_get(sixtyfourgua, gua))
        liuqin = [i[0] for i in self.liuqin]
        lq = [self.multi_key_dict_get(self.liuqin_w, i + find_gua_wuxing) for i in dw + uw]
        gua_name = self.multi_key_dict_get(sixtyfourgua, gua)
        find_su = dict(zip(self.sixtyfour_gua_index, self.chin_iter(self.chin_list, "參"))).get(gua_name)
        sy = dict(zip(self.sixtyfour_gua_index, su_yao)).get(gua_name)
        ng = [t[i] + d[i] for i in range(0, 6)]
        sy2 = [c == sy for c in ng]
        sy3 = [str(i).replace("False", "").replace("True", find_su) for i in sy2]
        ss = dict(zip(self.sixtyfour_gua_index, self.chin_iter(fivestars, "鎮星"))).get(gua_name)
        position = sy3.index(find_su)
        if position == 0:
            g = self.new_list(self.chin_list, find_su)[0:6]
        elif position == 5:
            g = list(reversed(self.new_list(self.chin_list, find_su)))[-6:]
        elif position == 4:
            g = list(reversed(self.new_list(self.chin_list, find_su)))[-6:][1:] + [
                list(reversed(self.new_list(self.chin_list, find_su)))[0]]
        elif position == 3:
            g = list(reversed(self.new_list(self.chin_list, find_su)))[-6:][2:] + list(
                reversed(self.new_list(self.chin_list, find_su)))[0:2]
        elif position == 2:
            g = list(reversed(self.new_list(self.chin_list, find_su)))[-6:][3:] + list(
                reversed(self.new_list(self.chin_list, find_su)))[0:3]
        elif position == 1:
            g = list(reversed(self.new_list(self.chin_list, find_su)))[-6:][4:] + list(
                reversed(self.new_list(self.chin_list, find_su)))[0:4]
        build_month_code = dict(zip(self.data.get("六十四卦"), self.data.get("月建"))).get(gua_name)
        build_month = self.new_list(self.jiazi(), build_month_code)[0:6]
        accumulate_code = dict(zip(self.data.get("六十四卦"), self.data.get("積算"))).get(gua_name)
        accumulate = self.new_list(self.jiazi(), accumulate_code)
        return {"卦": gua_name,
                "五星": ss,
                "世應卦": shiying + "卦",
                "星宿": g,
                "天干": t,
                "地支": d,
                "五行": w,
                "世應": Shiying,
                "六親用神": lq,
                "納甲": ng,
                "建月": build_month,
                "積算": [list(i) for i in np.array_split(accumulate, 10)]}

    def decode_gua(self, gua, daygangzhi):
        fivestars = self.data.get("五星")
        eightgua = self.data.get("數字排八卦")
        sixtyfourgua = self.data.get("數字排六十四卦")
        su_yao = self.data.get("二十八宿配干支")
        shiying = self.multi_key_dict_get(self.data.get("八宮卦"), self.multi_key_dict_get(sixtyfourgua, gua))
        Shiying = list(self.findshiying.get(shiying))
        dgua = self.multi_key_dict_get(eightgua, gua[0:3])
        down_gua = self.gua_down_code.get(dgua)
        ugua = self.multi_key_dict_get(eightgua, gua[3:6])
        up_gua = self.gua_up_code.get(ugua)
        dt = [self.tiangan[int(g[0])] for g in [down_gua[i].split(',') for i in range(0, 3)]]
        dd = [self.dizhi[int(g[1])] for g in [down_gua[i].split(',') for i in range(0, 3)]]
        dw = [self.wuxin[int(g[2])] for g in [down_gua[i].split(',') for i in range(0, 3)]]
        ut = [self.tiangan[int(g[0])] for g in [up_gua[i].split(',') for i in range(0, 3)]]
        ud = [self.dizhi[int(g[1])] for g in [up_gua[i].split(',') for i in range(0, 3)]]
        uw = [self.wuxin[int(g[2])] for g in [up_gua[i].split(',') for i in range(0, 3)]]
        t = dt + ut
        d = dd + ud
        w = dw + uw
        find_gua_wuxing = self.multi_key_dict_get(self.data.get("八宮卦五行"),
                                                  self.multi_key_dict_get(sixtyfourgua, gua))
        liuqin = [i[0] for i in self.liuqin]
        lq = [self.multi_key_dict_get(self.liuqin_w, i + find_gua_wuxing) for i in dw + uw]
        gua_name = self.multi_key_dict_get(sixtyfourgua, gua)
        find_su = dict(zip(self.sixtyfour_gua_index, self.chin_iter(self.chin_list, "參"))).get(gua_name)
        sy = dict(zip(self.sixtyfour_gua_index, su_yao)).get(gua_name)
        ng = [t[i] + d[i] for i in range(0, 6)]
        sy2 = [c == sy for c in ng]
        sy3 = [str(i).replace("False", "").replace("True", find_su) for i in sy2]
        ss = dict(zip(self.sixtyfour_gua_index, self.chin_iter(fivestars, "鎮星"))).get(gua_name)
        position = sy3.index(find_su)
        if position == 0:
            g = self.new_list(self.chin_list, find_su)[0:6]
        elif position == 5:
            g = list(reversed(self.new_list(self.chin_list, find_su)))[-6:]
        elif position == 4:
            g = list(reversed(self.new_list(self.chin_list, find_su)))[-6:][1:] + [
                list(reversed(self.new_list(self.chin_list, find_su)))[0]]
        elif position == 3:
            g = list(reversed(self.new_list(self.chin_list, find_su)))[-6:][2:] + list(
                reversed(self.new_list(self.chin_list, find_su)))[0:2]
        elif position == 2:
            g = list(reversed(self.new_list(self.chin_list, find_su)))[-6:][3:] + list(
                reversed(self.new_list(self.chin_list, find_su)))[0:3]
        elif position == 1:
            g = list(reversed(self.new_list(self.chin_list, find_su)))[-6:][4:] + list(
                reversed(self.new_list(self.chin_list, find_su)))[0:4]
        build_month_code = dict(zip(self.data.get("六十四卦"), self.data.get("月建"))).get(gua_name)
        build_month = self.new_list(self.jiazi(), build_month_code)[0:6]
        accumulate_code = dict(zip(self.data.get("六十四卦"), self.data.get("積算"))).get(gua_name)
        accumulate = self.new_list(self.jiazi(), accumulate_code)
        aa = list(set(lq))
        fu = str(str([value for value in liuqin if value not in aa]).replace("['", "").replace("']", ""))
        fu_gua = self.dc_gua(self.multi_key_dict_get(self.bagua_pure_code, gua_name))
        fu_gua_gang = fu_gua.get("天干")
        fu_gua_zhi = fu_gua.get("地支")
        fu_gua_wu = fu_gua.get("五行")
        fu_gua_lq = fu_gua.get("六親用神")
        shen = self.multi_key_dict_get(self.shen, d[Shiying.index("世")])

        try:
            fu_num = fu_gua_lq.index(fu)
            fuyao = [str(g == fu) for g in fu_gua_lq].index('True')
            fuyao1 = fu_gua_lq[fu_num] + fu_gua_gang[fu_num] + fu_gua_zhi[fu_num] + fu_gua_wu[fu_num]
            fu_yao = {"伏神所在爻": lq[fuyao], "伏神六親": fu, "伏神排爻數字": fu_num,
                      "本卦伏神所在爻": lq[fu_num] + t[fu_num] + d[fu_num] + w[fu_num], "伏神爻": fuyao1}

        except ValueError:
            fu_yao = ""

        return {"卦": gua_name,
                "五星": ss,
                "世應卦": shiying + "卦",
                "星宿": g,
                "天干": t,
                "地支": d,
                "五行": w,
                "世應爻": Shiying,
                "身爻": lq[shen] + t[shen] + d[shen] + w[shen],
                "六親用神": lq,
                "伏神": fu_yao,
                "六獸": self.find_six_mons(daygangzhi),
                "納甲": ng,
                "建月": build_month,
                "積算": [list(i) for i in np.array_split(accumulate, 10)]}

    def decode_two_gua(self, bengua, ggua, daygangzhi):
        a = self.decode_gua(bengua, daygangzhi)
        b = self.decode_gua(ggua, daygangzhi)
        try:
            fu_yao = a.get("伏神").get("伏神爻")
            fu_ben_yao = a.get("伏神").get('本卦伏神所在爻')
            g_yao = b.get("六親用神") + b.get("天干") + b.get("地支") + b.get("五行")
            if fu_yao == g_yao:
                fei = fu_ben_yao
            else:
                fei = ""
        except Exception:
            fei = ""

        return {"本卦": a, "之卦": b, "飛神": fei}

    def qigua_time(self, y, m, d, h):
        """
        阳历/公立时间
        :param y:
        :param m:
        :param d:
        :param h:
        :return:
        """
        gangzhi = self.gangzhi(y, m, d, h)
        ld = self.lunar_date_d(y, m, d, h)
        zhi_code = dict(zip(self.dizhi, range(1, 13)))
        yz_code = zhi_code.get(gangzhi[0][1])
        hz_code = zhi_code.get(gangzhi[3][1])
        cm = ld.get("月")
        cd = ld.get("日")
        eightgua = self.data.get("八卦數值")
        upper_gua_remain = (yz_code + cm + cd + hz_code) % 8
        if upper_gua_remain == 0:
            upper_gua_remain = int(8)
        upper_gua = eightgua.get(upper_gua_remain)
        lower_gua_remain = (yz_code + cm + cd) % 8
        if lower_gua_remain == 0:
            lower_gua_remain = int(8)
        lower_gua = eightgua.get(lower_gua_remain)
        combine_gua1 = lower_gua + upper_gua
        combine_gua = list(combine_gua1)
        bian_yao = (yz_code + cm + cd + hz_code) % 6
        if bian_yao == 0:
            bian_yao = int(6)
        elif bian_yao != 0:
            combine_gua[bian_yao - 1] = combine_gua[bian_yao - 1].replace("7", "9").replace("8", "6")
        bian_gua = "".join(combine_gua)
        ggua = bian_gua.replace("6", "7").replace("9", "8")
        return {**{'日期': gangzhi[0] + "年" + gangzhi[1] + "月" + gangzhi[2] + "日" + gangzhi[3] + "時"},
                **{"大衍筮法": self.mget_bookgua_details(bian_gua)}, **self.decode_two_gua(bian_gua, ggua, gangzhi[2])}

    def qigua_now(self):
        now = datetime.datetime.now()
        return self.qigua_time(int(now.year), int(now.month), int(now.day), int(now.hour))


if __name__ == '__main__':
    result = Iching().mget_bookgua_details("787987") #手動起卦，從下而上，適合以蓍草起卦者使用，譬如 "初爻7, 二爻8, 三爻9, 四爻7, 五爻8, 上爻9"，即 ichingshifa.mget_bookgua_details('789789') Manually input each of lines' value, e.g. Iching().mget_bookgua_details('789789')
    result1 =Iching().bookgua_details() #顯示隨機起卦結果 Making divination randomly
    result2 =Iching().datetime_bookgua(2019,10,11,12) #指定年月日時起卦 make divination with the specific datetime
    result3 =Iching().current_bookgua() #按現在的年月日時起卦，此法只有一動爻 make divination with the current datetime
    result4 =Iching().decode_gua("787987", "庚寅") #手動起卦，從下而上，起本卦之卦納甲
    result5 =Iching().qigua_now() #{'日期': '辛丑年戊戌月庚寅日甲申時', '大衍筮法': ['887888', '謙', '謙', {0: '亨，君子有終。', 1: '初六：謙謙君子，用涉大川，吉。', 2: '六二，鳴謙，貞吉。', 3: '九三，勞謙，君子有終，吉。', 4: '六四：無不利，撝謙。', 5: '六五：不富，以其鄰，利用侵伐，無不利。', 6: '上六：鳴謙，利用行師，征邑國。', 7: '彖︰謙，亨，天道下濟而光明，地道卑而上行。天道虧盈而益謙，地道變盈而流謙，鬼神害盈而福謙，人道惡盈而好謙。謙尊而光，卑而不可踰，君子之終也。'}, ('動爻有【0】根。', '主要看【謙】卦彖辭。', '謙，亨，天道下濟而光明，地道卑而上行。天道虧盈而益謙，地道變盈而流謙，鬼神害盈而福謙，人道惡盈而好謙。謙尊而光，卑而不可踰，君子之終也。')], '本卦': {'卦': '謙', '五星': '太白', '世應卦': '五世卦', '星宿': ['亢', '角', '軫', '翼', '張', '星'], '天干': ['丙', '丙', '丙', '癸', '癸', '癸'], '地支': ['辰', '午', '申', '丑', '亥', '酉'], '五行': ['土', '火', '金', '土', '水', '金'], '世應爻': ['初', '應', '三', '四', '世', '六'], '身爻': '兄癸酉金', '六親用神': ['父', '官', '兄', '父', '子', '兄'], '伏神': {'伏神所在爻': '官', '伏神六親': '妻', '伏神排爻數字': 1, '本卦伏神所在爻': '官丙午火', '伏神爻': '妻丁卯木'}, '六獸': ['虎', '武', '龍', '雀', '陳', '蛇'], '納甲': ['丙辰', '丙午', '丙申', '癸丑', '癸亥', '癸酉'], '建月': ['庚申', '辛酉', '壬戌', '癸亥', '甲子', '乙丑'], '積算': [['乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午'], ['辛未', '壬申', '癸酉', '甲戌', '乙亥', '丙子'], ['丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午'], ['癸未', '甲申', '乙酉', '丙戌', '丁亥', '戊子'], ['己丑', '庚寅', '辛卯', '壬辰', '癸巳', '甲午'], ['乙未', '丙申', '丁酉', '戊戌', '己亥', '庚子'], ['辛丑', '壬寅', '癸卯', '甲辰', '乙巳', '丙午'], ['丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子'], ['癸丑', '甲寅', '乙卯', '丙辰', '丁巳', '戊午'], ['己未', '庚申', '辛酉', '壬戌', '癸亥', '甲子']]}, '之卦': {'卦': '謙', '五星': '太白', '世應卦': '五世卦', '星宿': ['亢', '角', '軫', '翼', '張', '星'], '天干': ['丙', '丙', '丙', '癸', '癸', '癸'], '地支': ['辰', '午', '申', '丑', '亥', '酉'], '五行': ['土', '火', '金', '土', '水', '金'], '世應爻': ['初', '應', '三', '四', '世', '六'], '身爻': '兄癸酉金', '六親用神': ['父', '官', '兄', '父', '子', '兄'], '伏神': {'伏神所在爻': '官', '伏神六親': '妻', '伏神排爻數字': 1, '本卦伏神所在爻': '官丙午火', '伏神爻': '妻丁卯木'}, '六獸': ['虎', '武', '龍', '雀', '陳', '蛇'], '納甲': ['丙辰', '丙午', '丙申', '癸丑', '癸亥', '癸酉'], '建月': ['庚申', '辛酉', '壬戌', '癸亥', '甲子', '乙丑'], '積算': [['乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午'], ['辛未', '壬申', '癸酉', '甲戌', '乙亥', '丙子'], ['丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午'], ['癸未', '甲申', '乙酉', '丙戌', '丁亥', '戊子'], ['己丑', '庚寅', '辛卯', '壬辰', '癸巳', '甲午'], ['乙未', '丙申', '丁酉', '戊戌', '己亥', '庚子'], ['辛丑', '壬寅', '癸卯', '甲辰', '乙巳', '丙午'], ['丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子'], ['癸丑', '甲寅', '乙卯', '丙辰', '丁巳', '戊午'], ['己未', '庚申', '辛酉', '壬戌', '癸亥', '甲子']]}, '飛神': ''}
    result6 =Iching().qigua_time(2019,10,11,12)


    print(json.dumps(result))
    print(json.dumps(result1))
    print(json.dumps(result2))
    print(json.dumps(result3))
    print(json.dumps(result4))
    print(json.dumps(result5))
    print(json.dumps(result6))
    print(result)
    print(result1)
    print(result2)
    print(result3)
    print(result4)
    print(result5)
    print(result6)





