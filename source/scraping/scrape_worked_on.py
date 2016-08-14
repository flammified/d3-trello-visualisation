from trello import TrelloClient
from trello import Board

import pymysql.cursors

# Trello usernames of ceo, cto and cho in that order
ceo_cto_cho = [
    "cto",
    "ceo",
    "cho"
]

# List of the trello usernames of architects in the project
architects = [
    "Tester3"
]

# List of the trello usernames of people managers in the project
people_managers = [
    "Tester1"
]

# List of the trello usernames of project managers in the project
project_managers = [
    "Tester2"
]

# Links to add at the end, because the are missing.
# Need to be manually added
missing_links = [
    ("Tester2", "0001")
]

# Wrong links that need to be removed manually.
remove_links = [
    ("Tester1", "0001")
]


def get_memberid_from_name(connection, name):
    with connection.cursor() as cursor:
        sql = "SELECT `id` FROM `members` WHERE `name`=%s"
        cursor.execute(sql, (name,))
        result = cursor.fetchone()
        return result["id"]

def get_projectid_from_name(connection, name):
    with connection.cursor() as cursor:
        sql = "SELECT `id` FROM `projects` WHERE `name`=%s"
        cursor.execute(sql, (name,))
        result = cursor.fetchone()
        return result["id"]

def get_projectid_from_project_no(connection, number):
    with connection.cursor() as cursor:
        sql = "SELECT `id` FROM `projects` WHERE `name` LIKE %s"
        cursor.execute(sql, (number + "%",))
        result = cursor.fetchone()
        return result["id"]

client = TrelloClient(

)

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='r2d2visualisation',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


client.info_for_all_boards(())
id = ""
for board in client.all_info:
    if "Roborescue Project Board" in board["name"]:
        id = board["id"]
        break

project_board = Board(client, id)
project_board.fetch()
all_cards = project_board.all_cards()

unique_names = []
unique_project_names = []
with connection.cursor() as cursor:
    for card in all_cards:

        if b"0002" in card.name:
            continue
        if card.name in unique_project_names:
            continue
        names_already_done = []
        unique_project_names.append(card.name)

        card.fetch_actions(['addMemberToCard'])
        sql = "INSERT INTO `projects` (`name`) VALUES (%s)"
        cursor.execute(sql, (card.name))

        for action in card.actions:
            person_name = action["member"]["fullName"]

            if person_name in ceo_cto_cho:
                continue  # They dont count in this visualisation.

            if person_name not in unique_names:
                unique_names.append(person_name)

                number_role = 0
                if person_name in architects:
                    number_role = 1
                if person_name in people_managers:
                    number_role = 2
                if person_name in project_managers:
                    number_role = 3

                sql = "INSERT INTO `members` (`name`, `hours`,`role`, `lines_added`, `lines_removed`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (person_name, str(0, number_role, str(0, str(0)))

            if person_name not in names_already_done:
                names_already_done.append(action["member"]["fullName"])

                member_id = get_memberid_from_name(connection, person_name)
                project_id = get_projectid_from_name(connection, card.name)

                sql = "INSERT INTO `worked_on` (`project_id`, `member_id`) VALUES (%s, %s)"
                cursor.execute(sql, (project_id, member_id))


        connection.commit()


    for link in missing_links:
        sql = "INSERT INTO `worked_on` (`project_id`, `member_id`) VALUES (%s, %s)"
        cursor.execute(
            sql,
            (get_projectid_from_project_no(connection, link[1], get_memberid_from_name(connection, link[0]))
        )
    for link in remove_links:
        sql = "DELETE FROM worked_on WHERE `project_id`=%s AND `member_id`=%s;"
        cursor.execute(
            sql,
            (get_projectid_from_project_no(connection, link[1], get_memberid_from_name(connection, link[0]))
        )

    connection.commit()
