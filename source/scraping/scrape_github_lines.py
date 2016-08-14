import pymysql.cursors
import itertools


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='r2d2visualisation',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)



#Github to Trello
name_conversion_table = {
    "test_on_github": "test_on_trello"
}

lines_added_total = {}
lines_removed_total = {}

with open("github/sum.txt") as file:
    lines = file.read().split("\n")
    for line in lines:
        if line == "":
            continue
        information = line.split(" ")
        name = information[0]
        name = name_conversion_table[name]
        lines_added = information[1].split(",")[0]
        lines_removed = information[1].split(",")[1]
        lines_added_total[name] = int(lines_added_total.get(name, 0)) + int(lines_added)
        lines_removed_total[name] = int(lines_removed_total.get(name, 0)) + int(lines_removed)

        print(lines_added, lines_removed)

with connection.cursor() as cursor:
    for name, lines_added in lines_added_total.items():
        sql = "UPDATE `members` SET `lines_added`=%s WHERE `name`=%s"
        cursor.execute(sql, (lines_added, name))

    for name, lines_removed in lines_removed_total.items():
        sql = "UPDATE `members` SET `lines_removed`=%s WHERE `name`=%s"
        cursor.execute(sql, (lines_removed, name))

    connection.commit()
