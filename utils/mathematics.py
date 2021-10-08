import math
import cv2
import numpy as np


class duongthang:

    def setheso(self, hesoa, hesob):
        self.a = hesoa
        self.b = hesob

    def __init__(self, x1, y1, x2, y2, hesoa=None, hesob=None, hesoc=None):
        '''
        giải hpt bậc nhất 2 ẩn, lưu hệ số.
        phương trình đường thẳng có hệ số a, b không đồng thời bằng 0.
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        '''
        """
        duongthang đi qua 2 điểm có VTCP u(x2-x1,y2-y1)
        pt tham số:
            x = x1 + (x2-x1)t
            y = y1 + (y2-y1)t
        <->
            (x - x1)/(x2-x1) = t
            (y - y1)/(y2-y1) = t
        <->
            (x - x1)/(x2-x1) = (y - y1)/(y2-y1)
        <-> (x - x1)*(y2-y1) = (y - y1)*(x2-x1)
        <-> x*(y2-y1) - x1*(y2-y1) = y*(x2-x1) - y1*(x2-x1)
        <-> x*(y2-y1) - y*(x2-x1) + y1*(x2-x1) - x1*(y2-y1) = 0 (có dạng pt bậc nhất)  
        tổng quát hóa:
            ax + by + c = 0  
        """
        self.IS_DEBUG_duongthang = False
        if hesoa is not None and hesob is not None and hesoc is not None:
            self.a = hesoa
            self.b = hesob
            self.c = hesoc
        elif not (hesoa == 0 and hesob == 0):
            self.a = y2 - y1
            self.b = x1 - x2
            self.c = y1 * (x2 - x1) - x1 * (y2 - y1)
            # if self.vitrituongdoi(x1, y1) != 0 and self.vitrituongdoi(x2, y2) != 0:
            #     print("phương trình giải sai")
            #     exit(-1)
            # else:
            #     print("phương trình giải đúng")
            # if IS_DEBUG:
            #     print("phương trình đường thẳng có hệ số là:", self.a, self.b, self.c)
        else:
            print("lỗi input")
            return

    def getY(self, x):
        return - round((self.a * x + self.c) / self.b)

    def getX(self, y):
        if self.a == 0:
            return 0
        return round((-self.c - self.b * y) / self.a)

    def getToaDoB(self, x1, y1, khoangcach, flag):
        '''
        tìm vị trí điểm biên cạnh và biên đáy CMND qui về bài toán:
        xác định tọa độ điểm B(x,y) thuộc đường thẳng [duongthang] và cách A(x1,y1) thuộc [duongthang] một khoảng = [khoangcach].
        :param x1:
        :param y1:
        :param khoangcach:
        :param flag: flag = {1, -1}. Nếu flag = 1 : căn lấy tọa độ biên cạnh , -1: lấy tọa độ biên đáy
        :return: (X,Y)
        '''
        # kiểm tra A(x1, y1) có thuộc [duongthang] hay không
        # if self.vitrituongdoi(x1, y1) == 0:
        #     print("điểm M nằm trên đường thẳng")
        # else:
        #     print("điểm M cách đường thẳng:", self.vitrituongdoi(x1, y1))
        #     exit(-1)
        """ giai hpt:
            Với hệ số a # 0 và b # 0:
                khoangcach = sqrt(pow(x-x1)+pow(y-y1)) (1)
                ax+by+c=0 
             -> y=(-ax-c)/b (2)
            thay (2) vào (1) ta được:
        (1) <-> pow(khoangcach) = pow(x-x1) + pow((-ax-c)/b-y1)
            <-> pow(khoangcach) = pow(x) - 2*x*x1 + pow(x1) + pow[(-ax-c)/b] - 2*[(-ax-c)/b]*y1 + pow(y1) 
            <-> pow(khoangcach) = pow(x) - 2*x*x1 + pow(x1) + pow(-ax-c)/pow(b) - [(-2ax-2c)*y1]/b + pow(y1) 
            <-> pow(khoangcach) = pow(x) - 2*x*x1 + pow(x1) + pow(-ax-c)/pow(b) - (-2axy1-2cy1)/b + pow(y1) (3)
            giải pow(-ax-c)/pow(b) = pow(ax+c)/pow(b)
                                   = [pow(ax)+2axc+pow(c)]/pow(b)
                                   = [pow(a)*pow(x)+2axc+pow(c)]/pow(b) (4)
            thay (4) vào (3) ta được:
                (3) <-> pow(khoangcach) = pow(x) - 2*x*x1 + pow(x1) + [pow(a)*pow(x)+2axc+pow(c)]/pow(b) - (-2axy1-2cy1)/b + pow(y1)
                    <-> pow(x) + pow(a)*pow(x)/pow(b)+2axc/pow(b) + 2axy1/b - 2*x*x1 = pow(khoangcach) - pow(y1) - pow(x1) - 2cy1/b - pow(c)/pow(b)
                    <-> pow(x)[1 + pow(a)/pow(b)] + x*[2ac/pow(b) + 2ay1/b - 2*x1] - pow(khoangcach) + pow(y1) + pow(x1) + 2cy1/b + pow(c)/pow(b) = 0 (có dạng pt bậc 2) (5)
            giải pt bậc 2 (5) ta luôn được 2 nghiệm chính là tọa độ trục x (hoành) của image opencv. 
                Từ X1, X2, thay vào ptduongthang ta tìm được Y1, Y2.
            Với hệ số a = 0 (đường thẳng vuông góc với trục Oy), phương trình có 2 No là: X1(x1-khoangcach, y1) và X2(x1+khoangcach, y1)
            Với hệ số b = 0 (đường thẳng vuông góc với trục Ox), phương trình có 2 No là: X1(x1, y1-khoangcach) và X2(x1, y1+khoangcach)


                Chọn tọa độ thỏa mãn điều kiện theo flag để chọn một Nghiệm phù hợp & return. 
        """
        if round(khoangcach) == 0:
            return x1, y1
        if self.a != 0 and self.b != 0:
            if self.IS_DEBUG_duongthang: print("ax2+bx+c = 0, với a,b,c =", 1 + pow(self.a, 2) / pow(self.b, 2),
                                               2 * self.a * self.c / pow(self.b, 2) + 2 * self.a * y1 / self.b - 2 * x1,
                                               pow(khoangcach, 2) - pow(y1, 2) - pow(x1,
                                                                                     2) - 2 * self.c * y1 / self.b - pow(
                                                   self.c, 2) / pow(self.b,
                                                                    2))
            X1, X2 = giaipt2(1 + pow(self.a, 2) / pow(self.b, 2),
                             2 * self.a * self.c / pow(self.b, 2) + 2 * self.a * y1 / self.b - 2 * x1,
                             - pow(khoangcach, 2) + pow(y1, 2) + pow(x1, 2) + 2 * self.c * y1 / self.b + pow(self.c,
                                                                                                             2) / pow(
                                 self.b, 2))
            if self.IS_DEBUG_duongthang: print("X1, X2, Y1, Y2: ", X1, X2, self.getY(X1), self.getY(X2))
            if self.IS_DEBUG_duongthang: print("hệ số a, b, c trước khi trả về tọa độ điểm biên: ", self.a, self.b,
                                               self.c)
            if flag == -1:  # căn dọc chữ
                return (round(X1), self.getY(X1)) if self.getY(X1) > y1 else (round(X2), self.getY(X2))
            else:  # căn ngang chữ

                return (round(X1), self.getY(X1)) if X1 > x1 else (round(X2), self.getY(X2))
        if self.a == 0:
            if flag == 1:
                return round(x1 + khoangcach), y1
            else:
                return x1, round(y1 + khoangcach)
        elif self.b == 0:
            if flag == 1:
                return x1, round(y1 - khoangcach)
            else:
                return x1, round(y1 + khoangcach)

    def getPttieptuyen(self, x, y):
        '''
        get phương trình tiếp tuyến đi qua M(x,y) của đường thẳng vuông góc với đường thẳng (d) ax +by +c =0
        a.a' = -1 (với a # 0)
        với a = 0:
        pttieptuyen là ptduongthẳng đi qua M(x,y) và N(x, 0),
        :param x, y: là tọa độ M(x_m, y_m)
        :return: (ptduongthang) pttieptuyen
        '''
        """ tìm duongthang y = a'x +b'  thỏa mãn:
                a.a' = -1 (a # 0)

            Giải:
            https://hoctoan24h.net/tim-hinh-chieu-vuong-goc-cua-diem-len-duong-thang/
            vì d' vuông góc với d nên d' có dạng:
                -[b]x + [a]y +c = 0 (a, b là hệ số xác định của đường thẳng d)
            vì M(x_M, y_M) thuộc d' nên M(x_M, x_M) là nghiệm của pt d':
                -[b]*x_M + [a]*y_M +c = 0
                    -> c = [b]*x_M - [a]*y_M

        """

        if self.a == 0:
            return duongthang(x, y, x, 0)
        elif self.b == 0:
            return duongthang(x, y, 0, y)
        return duongthang(None, None, None, None, -self.b, self.a, self.b * x - self.a * y)

    def getToadoBphuongtrinhsongsong(self, x1, y1, khoangcach):
        '''
        Trả về tọa độ điểm B(x_b, y_b) thuộc phương trình song với duongthang và đi qua M(x,y) cách M một khoảng = khoangcach.

        :param khoangcach: khoảng cách từ M() đến điểm return.
        :param x1, y1: tọa độ điêm M.
        :return: x, y
        '''
        """Gọi d':a'x+b'y+c=0 là đt song song với duongthang -> a' = [a], b' = [b]
        Vì d' đi qua M(x1,y1):
            ax1+by1+c =0 -> c = -ax1-by1
        """
        duongthang_sonsong = duongthang(None, None, None, None, self.a, self.b, -self.a * x1 - self.b * y1)
        return duongthang_sonsong.getToaDoB(x1, y1, khoangcach, 1)

    def vitrituongdoi(self, x, y):
        '''
        xác định vị trí tương đối giữa một điểm đến một đường thẳng.
        :param x:
        :param y:
        :return: khoangcach từ điểm đó đến đường thẳng
        '''

        """ công thức tính khoảng cách từ một điểm đến đường thẳng: d(M, duongthang): |axM+yM+c|/ sqrt(pow(a) + pow(b))
        trong thuật toán này cần phân biệt vị trí tương đối (nằm trên hay dưới, bên trái hay phải) -> bỏ dấu giá trị tuyệt đối trong công thức.
        """
        return round((self.a * x + self.b * y + self.c) / math.sqrt(pow(self.a, 2) + pow(self.b, 2)))

    def gettoadogiaodiem(self, dt1):
        '''
        nhập vào đường thẳng, trả về tọa độ giao điểm duongthang với dt1
        :param dt1: đường thẳng cắt
        :return:
            (x,y) : nếu dt1 cắt duongthang
            None  : nếu không cắt
        '''
        """ giải hpt:
        a1x+b1y+c1 = 0 -> x = (-b1y-c1)/a1 (1)
        a2x+b2y+c2 = 0 
    <-> [a2(-b1y-c1)]/a1 + b2y + c2 = 0
    <-> -b1ya2/a1-c1a2/a1 + b2y + c2 = 0
    <-> -b1ya2/a1 + b2y = c1a2/a1 - c2  
    <-> y(-b1a2/a1 + b2)  = c1a2/a1 - c2  
     -> y  = (c1a2/a1 - c2)/(-b1a2/a1+ b2)  
     -> x  = (-b1*((c1a2/a1 - c2)/(-b1a2/a1+ b2))-c1)/a1  
        Với 2đt vuông góc hoặc song song với trục tọa độ:
            return (x,y), trong đó:
                x : -c1/a1 (với a1x+c1 = 0 là đường thẳng có hệ số b = 0)
                y : -c2/b2 (với b2x+c2 = 0 là đường thẳng có hệ số a = 0)
        """
        if self.a == 0 or self.b == 0:
            x = -self.c / self.a if self.b == 0 else -dt1.c / dt1.a
            y = -dt1.c / dt1.b if dt1.a == 0 else -self.c / self.b
            return round(x), round(y)
        return (round((-self.b * ((self.c * dt1.a / self.a - dt1.c) / (
                -self.b * dt1.a / self.a + dt1.b)) - self.c) / self.a),
                round((self.c * dt1.a / self.a - dt1.c) / (
                        -self.b * dt1.a / self.a + dt1.b)))


def khoangcach(x1, y1, x2, y2):
    return round(math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2)))


def giaipt2(a, b, c):
    if a == 0:
        if b == 0:
            return None
        return -c / b
    delta = b * b - 4 * a * c
    if delta > 0:
        return float((-b + math.sqrt(delta)) / (2 * a)), float((-b - math.sqrt(delta)) / (2 * a))
    elif delta == 0:
        return -b / (2 * a)
    return None


def getToaDoBien(duongthang, diemneo, width_image, heigh_image, ranges):
    '''
    get tọa độ biên của range
    :param duongthang:
    :param ranges: [xmin, xmax, ymin, ymax] : tỉ lệ
    :return: [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    '''
    list_to_return = [0] * 4
    ## mục tiêu: xác định tọa độ điểm biên, biết hình chiếu của điểm biên trên ptduongthang cách điểm neo một khoảng = width_cutted_cmnd*[tỉ lệ tương ứng]
    # xác định tọa độ hình chiều của tọa độ biên.
    x_bien, y_bien = duongthang.getToaDoB(diemneo[0], diemneo[1],
                                          round(ranges[0] * width_image), 1)
    # xác định phương trình tiếp tuyến đi qua tọa độ trên (đi qua tọa độ điểm biên và tọa độ hình chiếu). Note: pttieptuyen_bien là đường thẳng đi qua điểm biên.
    pttieptuyen_bien = duongthang.getPttieptuyen(x_bien, y_bien)
    # từ pttieptuyen đi qua điểm biên và khoảng cách của nó đến hình chiếu đã được xác định, xác định vị trí điểm biên.
    list_to_return[0] = pttieptuyen_bien.getToaDoB(x_bien, y_bien,
                                                   round(ranges[2] * heigh_image), -1)
    list_to_return[3] = pttieptuyen_bien.getToaDoB(x_bien, y_bien,
                                                   round(ranges[3] * heigh_image), -1)
    # xác định tọa độ hình chiều của tọa độ biên.
    x_bien, y_bien = duongthang.getToaDoB(diemneo[0], diemneo[1],
                                          round(ranges[1] * width_image), 1)
    # xác định phương trình tiếp tuyến đi qua tọa độ trên (đi qua tọa độ điểm biên và tọa độ hình chiếu). Note: pttieptuyen_bien là đường thẳng đi qua điểm biên.
    pttieptuyen_bien = duongthang.getPttieptuyen(x_bien, y_bien)
    # từ pttieptuyen đi qua điểm biên và khoảng cách của nó đến hình chiếu đã được xác định, xác định vị trí điểm biên.
    list_to_return[1] = pttieptuyen_bien.getToaDoB(x_bien, y_bien,
                                                   round(ranges[2] * heigh_image), -1)
    list_to_return[2] = pttieptuyen_bien.getToaDoB(x_bien, y_bien,
                                                   round(ranges[3] * heigh_image), -1)
    return list_to_return


def istextboxinrange(inrange, textbox, isdebug=False):
    '''

    :param inrange: range [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    :param textbox: textbox as vertices
    :return: True | Flase
    '''
    """ tính tỉ lệ bao phủ của range lên textbox.
    1. tính chiều cao và chiều rộng textbox
    2. tính ptduongthang_range_horizontal_upper
    3.
     a, xét vị trí tương đối trên, vttd_tren = [textbox[0], ptduongthang_range_horizontal_upper]
        Nếu vttd_tren < 0: tile_y_tren = 0 (0 : flag: tile_y_tren = 0 khi [range] bao phủ hết phầm trên của textbox, 0 không đại diện cho giá trị tỉ lệ)
        Nếu vttd_tren < 0: tile_y_tren = 1 - vttd/chiều cao textbox (vttd < 0 khi [range] không bao phủ hết cạnh textbox phía trên. giá trị {1 - vttd/chiều cao textbox} là tỉ lệ vùng textbox không bị bao phủ bơi [range])
    tương tự để tính vttd_duoi, vttd_trai, vttd_phai
         tile_y = (tile_y_tren + tile_y_duoi) if tile_y_tren != 0 or tile_y_tren != 0 else tile_y = 1
         tương tự với tile_x
    tile = tile_x*tile_y
    4. Nếu tile > 0.8, return True else return False. (qui ước nếu range bao phủ trên 80% textbox thì textbox thuộc về range)
    """
    # Top bottom left right
    textbox_heigh = khoangcach(textbox[0].x, textbox[0].y, textbox[3].x, textbox[3].y)
    textbox_width = khoangcach(textbox[0].x, textbox[0].y, textbox[1].x, textbox[1].y)
    # print("textbox_heigh, textbox_width", textbox_heigh, textbox_width)
    # phương trình đường thẳng các cạnh của range
    ptduongthang_range_top = duongthang(inrange[0][0], inrange[0][1], inrange[1][0], inrange[1][1])
    ptduongthang_range_bottom = duongthang(inrange[2][0], inrange[2][1], inrange[3][0], inrange[3][1])
    ptduongthang_range_left = duongthang(inrange[0][0], inrange[0][1], inrange[3][0], inrange[3][1])
    ptduongthang_range_right = duongthang(inrange[1][0], inrange[1][1], inrange[2][0], inrange[2][1])
    # tính tỉ lệ bao phủ các cạnh của range lên các cạnh của textbox
    vttd = ptduongthang_range_top.vitrituongdoi(textbox[0].x, textbox[0].y)
    if vttd < 0:
        ratio_top = 0
    elif vttd < textbox_heigh:
        ratio_top = 1 - vttd / textbox_heigh
    else:
        return False
    vttd = ptduongthang_range_bottom.vitrituongdoi(textbox[3].x, textbox[3].y)
    if vttd < 0:
        ratio_botton = 0
    elif vttd < textbox_heigh:
        ratio_botton = 1 - vttd / textbox_heigh
    else:
        return False
    vttd = ptduongthang_range_left.vitrituongdoi(textbox[0].x, textbox[0].y)
    if vttd > 0:
        ratio_left = 0
    elif -vttd < textbox_width:
        # if isdebug: print("vttd left textbox[0]", vttd)
        ratio_left = 1 + vttd / textbox_width
    else:
        # print("False")
        return False
    vttd = ptduongthang_range_right.vitrituongdoi(textbox[3].x, textbox[3].y)
    if vttd < 0:
        ratio_right = 0
        if isdebug: print("vttd right textbox[3]", vttd)
    # elif vttd < textbox_width:
    #     if isdebug: print("vttd right textbox[3]", vttd)
    #     ratio_right = 1 - vttd / textbox_width
    else:
        return False
    # ratio_right = 0 if vttd < 0 else 1 - vttd / textbox_width
    # tính tỉ lệ diện tích bao phủ: , ratio_vertical
    ratio_horizontal = ratio_top + ratio_botton if ratio_top != 0 or ratio_botton != 0 else 1
    ratio_vertical = ratio_left + ratio_right if ratio_left != 0 or ratio_right != 0 else 1
    if isdebug: print("ratio = ratio_horizontal * ratio_vertical", ratio_horizontal, ratio_vertical,
                      "ratio_left, ratio_right",
                      ratio_left, ratio_right)
    ratio = ratio_horizontal * ratio_vertical
    return ratio > 0.8


def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy
