from DoneDone import IssueTracker
import json,sys

# for flask decorator
from datetime import timedelta
from flask import Flask, make_response, request, current_app
from functools import update_wrapper

def get_people_in_a_project(projectId):
    peopleObj = issueTracker.getAllPeopleInProject(projectId)
    people = []
    for pp in peopleObj:
        people.append(pp)

    return json.loads("".join(people))

def find_person_id_in_people(peopleList, personName):
    for person in peopleList:
        if personName in person['Value']:
            return person['ID']
    return None

def find_project_id(projectName):
    projectsObj = issueTracker.getProjects()
    for pp in projectsObj:
        projects = json.loads(pp)
        for p in projects:
            if p['Name'] == projectName:
                return int(p['ID'])
    return None

def createIssue(issueTitle, issueDescription):
    ##
    ## Prepare Issue
    ##
    projectId = find_project_id('EWOK')
    peopleInProject = get_people_in_a_project(projectId)
    resolverId = find_person_id_in_people(peopleInProject, "Ewok");
    testerId = resolverId

    issueTags = "autoIssue"
    issuePriority = 1 # low

    ##
    ## Add issue!
    ##
    retFlag = issueTracker.createIssue(
        ewokProjectId,
        issueTitle,
        issuePriority,
        resolverId,
        testerId,
        "\n    ".join(issueDescription.split('\n')),
        issueTags
    )

    return retFlag

# from https://blog.skyred.fi/articles/better-crossdomain-snippet-for-flask.html
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

if __name__ == '__main__':

    ##########################################################
    #                      CONFIGURATION                     #
    ##########################################################

    domain = "<YOUR DONE DONE DOMAIN HERE>"
    token = "<YOUR API TOKEN GOES HERE>"
    username = "<YOUR DONEDONE USERNAME>"
    password = "<YOUR DONEDONE PASSWORD>"
    serverPort = 8011

    ###########################################################################

    issueTracker = IssueTracker(domain, token, username, password)

    app = Flask(__name__)

    @app.route('/', methods=['POST', 'OPTIONS'])
    @crossdomain(origin='*')
    def index():
        data = request.get_json()
        issueTitle = data['title']
        issueDescription = data['description']

        print "[DEBUG] Issue title:", issueTitle
        print "[DEBUG] Issue description:", issueDescription

        if createIssue(issueTitle, issueDescription):
            return '{"status" : "ok"}'
        else:
            return '{"status" : "ko"}'

    app.run(port=serverPort)
