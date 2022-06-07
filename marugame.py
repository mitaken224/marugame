import csv
import operator
import os
import random

# カレントディレクトリの変更
os.chdir("../Public/product/py/marugame")


# うどんのメニュー(csv)を配列udon_dataに格納
# csvには各うどんの名前、量、価格が入っている
udon_data = []
with open("data/udon.csv", encoding="utf-8-sig") as f:
    for row in csv.reader(f):
        row[2] = int(row[2])  # 価格をint型にする
        udon_data.append(row)

# udon_dataを価格順(昇順)にソート
udon_data = sorted(udon_data, key=operator.itemgetter(2))


# サイドメニュー(csv)を配列side_menu_dataに格納
# csvには各サイドメニューの名前、種類、価格が入っている
side_menu_data = []
with open("data/side_menu.csv", encoding="utf-8-sig") as f:
    for row in csv.reader(f):
        row[2] = int(row[2])  # 価格をint型にする
        side_menu_data.append(row)

# side_menu_dataを価格順(昇順)にソート
side_menu_data = sorted(side_menu_data, key=operator.itemgetter(2))


# 最初のメッセージ
print("【丸亀製麵・満腹セット】")


# 予算の入力
while True:
    print("予算を入力してください")

    budget = input()  # 予算

    if not budget.isdecimal():  # 0～9の数字以外が入力された場合、再入力させる
        print("予算は0～9の数字のみで記入してください")
        continue
    elif int(budget) < side_menu_data[0][2]:  # 最も安い商品も買えない場合、再入力させる
        print("その予算では何も買えません")
        continue
    else:
        budget = int(budget)
        break

money = budget  # 残金 -> 商品を買うごとに価格分引いていく


###うどんの選択###

# 乱数を設定する際のパラメータをudon_dataの配列数で初期化
param = len(udon_data)

# うどんが買えたかどうかフラグ(買えない(False)で初期化)
udon_flg = False

# 所持金の範囲内でうどんを1杯買う
while True:
    # 0以上param未満の整数をランダムに選出
    rand = random.randrange(param)

    # rand番目に安いうどんが買えない場合、
    # それより安いうどんから再抽選する
    # 最も安いうどんも買えなければループ終了
    if udon_data[rand][2] > money:
        if rand == 0:
            break  # udon_flg = False のままループ終了
        param = rand
        continue

    udon_flg = True  # うどんを買うことができた

    udon = udon_data[rand]
    u_name = udon[0]  # うどんの名前
    u_size = udon[1]  # うどんの量
    u_price = int(udon[2])  # うどんの価格

    break


###選ばれたうどんの出力###

print("------------------------------------")

# うどんを買えたかどうかで分岐する
if udon_flg:
    print("{} サイズ:{} {}円".format(u_name, u_size, u_price))

    money -= u_price  # 予算からうどん代を引く
else:
    print("うどんを買えませんでした")

print()


###サイドメニューの選択###

# 乱数を設定する際のパラメータをside_menu_dataの配列数で初期化
param = len(side_menu_data)

# 所持金が残っている限りサイドメニューを買い続ける
while True:
    # 0以上param未満の整数をランダムに選出
    rand = random.randrange(param)

    # rand番目に安いサイドメニューが買えない場合、
    # それより安いメニューから再抽選する
    # 最も安いメニューも買えなければループ終了
    if side_menu_data[rand][2] > money:
        if rand == 0:
            break
        param = rand
        continue

    side_menu = side_menu_data[rand]
    s_name = side_menu[0]  # サイドメニューの名前
    # s_type = side_menu[1]       #サイドメニューの種類
    s_price = int(side_menu[2])  # サイドメニューの価格

    # 選ばれたサイドメニューの出力
    print("{} {}円".format(s_name, s_price))

    # 予算からサイドメニュー代を引く
    money -= s_price


###合計金額の出力###

print()
print("合計:" + str(budget - money) + "円")  # (予算 - 残金)で合計金額を求める
print("------------------------------------")
