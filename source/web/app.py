import json
import flask
import pymysql


app = flask.Flask(__name__)

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='r2d2visualisation',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


@app.route("/")
def index():
    """
    When you request the root path, you'll get the index.html template.

    """
    return flask.render_template("index.html")


@app.route("/people")
def people():
    """
    On request, returns all the persons in the database.

    :returns data:
        A JSON string of all persons in the database.

    """
    with connection.cursor() as cursor:
        sql = "SELECT `id`,`name`, `role`, `lines_added`, `lines_removed` FROM `members`"
        cursor.execute(sql)
        result = cursor.fetchall()
        for person in result:
            person["id"] = "M" + str(person["id"])
            person["type"] = "Member";
        return json.dumps(result)


@app.route("/projects")
def projects():
    """
    On request, returns all the projects in the database.

    :returns data:
        A JSON string of all projects in the database.

    """
    with connection.cursor() as cursor:
        sql = "SELECT `id`,`name` FROM `projects`"
        cursor.execute(sql)
        result = cursor.fetchall()
        for project in result:
            project["id"] = "P" + str(project["id"])
            project["type"] = "Project"
        return json.dumps(result)

@app.route("/worked_on")
def worked_on():
    """
    On request, returns the worked_on table of the database.

    :returns data:
        A JSON string containing links between people and projects

    """
    with connection.cursor() as cursor:
        sql = "SELECT `member_id`,`project_id` FROM `worked_on`"
        cursor.execute(sql)
        result = cursor.fetchall()
        for link in result:
            link["source"] = "M" + str(link["member_id"])
            link["target"] = "P" + str(link["project_id"])
            link["type"] = "link"
            del link["member_id"]
            del link["project_id"]
        return json.dumps(result)


if __name__ == "__main__":
    import os

    port = 8085

    # Open a web browser pointing at the app.
    os.system("open http://localhost:{0}".format(port))

    # Set up the development server on port 8000.
    app.debug = True
    app.run('0.0.0.0', port=port)
