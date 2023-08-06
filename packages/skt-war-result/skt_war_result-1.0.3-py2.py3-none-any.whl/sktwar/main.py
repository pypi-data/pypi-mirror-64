# -*- coding: utf-8 -*-

import requests
from lxml import html


def main():
    serverlist = [[1,"デポ1"],
                  [2,"デポ2"],
                  [3,"デポ3"],
                  [4,"ケン1"],
                  [5,"ケン2"],
                  [6,"ケン3"],
                  [7,"イシ1"],
                  [8,"イシ2"],
                  [9,"イシ3"]]

    msg = ""
    msg += "城獲得日"
    msg += "\t"
    msg += "サーバー名"
    msg += "\t"
    msg += "ケント城"
    msg += "\t"
    msg += "オーク砦"
    msg += "\t"
    msg += "ウィダウッド城"

    print(msg)

    for x in serverlist:

        page_content = requests.get('https://lineagem-jp.com/siege?categoryId=' + str(x[0]))
        tree = html.fromstring(page_content.content)

        data0 = tree.xpath('/html/body/div[1]/div[2]/div/div[3]/div[1]/div/div[1]/div/div[3]/text()')

        data1 = tree.xpath('/html/body/div[1]/div[2]/div/div[3]/div[1]/div/div[2]/div[1]/div[1]/span[2]/text()')
        data2 = tree.xpath('/html/body/div[1]/div[2]/div/div[3]/div[2]/div/div[2]/div[1]/div[1]/span[2]/text()')
        data3 = tree.xpath('/html/body/div[1]/div[2]/div/div[3]/div[3]/div/div[2]/div[1]/div[1]/span[2]/text()')

        msg = ""
        msg += str(data0[0])
        msg += "\t"
        msg += str(x[1])
        msg += "\t"
        msg += str(data1[0])
        msg += "\t"
        msg += str(data2[0])
        msg += "\t"
        msg += str(data3[0])

        print(msg)


if __name__ == "__main__":
    main()
