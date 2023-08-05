from flask import Flask, request, send_from_directory, make_response  # Import Flask
from flask_restful import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint
import time
app = Flask(__name__)  # Init Flask + API
api = Api(app)

# Swagger Code
@app.route('/swag/<path:path>')
def send_js(path):
    return send_from_directory('swag', path)
swaggerui_blueprints = get_swaggerui_blueprint('/swagger', '/swag/swag.json', config={'app-name': 'TimeKeeper'})
app.register_blueprint(swaggerui_blueprints, url_prefix='/swagger')

# Dictionaries | Variables
TimeKeeper = []  # Log Dictionary
TaskKeeper = []  # Task Dictionary
simpleResponse = True  # Text or JSON Response
def txtresponse(resp):  # Set Headers to Text for simple Responses
    response = make_response(resp, 200)
    response.mimetype = "text/plain"
    return response
def timeelapsed(sec):  # Formatted Time Elapsed
    return time.strftime("%H:%M:%S", time.gmtime(sec))
def displog(reports):  # Returns Formatted Time Log
    logged = reports.copy()
    if 'Stop' in logged:  # Calculates Time and Prettify
        logged['Duration'] = timeelapsed(logged['Stop'] - logged['Start'])
        logged['Stop'] = time.ctime(logged['Stop'])
    else:
        logged['Elapsed'] = timeelapsed(time.time() - logged['Start'])
    logged['Start'] = time.ctime(logged['Start'])  # NOTE: THIS IS INTENTIONALLY OUTSIDE THE ELSE BLOCK
    return logged
def pTrack(name):  # Creates a New Log and Ends Previous Log if it's continuing.
    if len(TimeKeeper) != 0:
        if not ('Stop' in TimeKeeper[-1]):
            TimeKeeper[-1]['Stop'] = time.time()
    if (len(TaskKeeper) != 0) and name.isnumeric and (int(name) < (len(TaskKeeper) )):
        if int(name) < 0:
            name = "Watch Log"
        else:
            index=(0-1-int(name))
            name=TaskKeeper[index]['Log']
    Tem = {'Log': name, 'Summary': 'http://127.0.0.1:5000/Summary/' + name, 'Start': time.time()}
    TimeKeeper.append(Tem.copy())
    Tem['Start'] = time.ctime(Tem['Start'])
    return txtresponse("1") if simpleResponse else Tem
def dTrack(name):  # Stops Log with given Name
    for ind, x in enumerate(TimeKeeper):
        if x['Log'] == name:
            if not ('Stop' in x):
                x['Stop'] = time.time()
def Track(name):  # Gets the Last Log of Provided Name
    for reports in reversed(TimeKeeper):
        if reports['Log'] == name:
            return displog(reports)
    if len(TimeKeeper) != 0:
        return {"Log": TimeKeeper[-1]}
    else:
        return {"Log": "Dead"}
class CreateTracker(Resource):
    def __init__(self):
        pass
    def get(self, name):  # Gets the Last Log of Provided Name
        return Track(name)
    def post(self, name):  # Creates a New Log and Ends Previous Log if it's continuing.
        return pTrack(name)
    def delete(self, name):  # Stops Log with given Name
        dTrack(name)
class pCreateTracker(Resource):
    def __init__(self):
        pass
    def get(self, name):  #  Creates a New Log and Ends Previous Log if it's continuing.
        return pTrack(name)
class dCreateTracker(Resource):
    def __init__(self):
        pass
    def get(self, name): # Stops Log with given Name
        dTrack(name)
def dSummary(name):  # Clears Everything
    global TimeKeeper
    TimeKeeper = []
def Summary(name):   # Gets all the Logs of Provided Name
    FinalReport = []
    CompleteReport = []
    TotalDuration = 0
    for reports in (TimeKeeper):
        logged = displog(reports)
        CompleteReport.append(logged)
        if reports['Log'] == name:
            FinalReport.append(logged)
            if 'Stop' in logged:
                timeexpenditure = reports['Stop'] - reports['Start']
            else:
                timeexpenditure = time.time() - reports['Start']
            TotalDuration += timeexpenditure
    if len(FinalReport) == 0:
        return CompleteReport
    else:
        return {"Expenditure": timeelapsed(TotalDuration), "Report": name, "Data": FinalReport}
class SummaryReport(Resource):
    def __init__(self):
        pass
    def get(self, name):  # Gets all the Logs of Provided Name
        return Summary(name)
    def delete(self, name):  # Clears Everything
        dSummary(name)
class dSummaryReport(Resource):
    def __init__(self):
        pass
    def get(self, name):  # Clears Everything
        dSummary(name)
def pTask(name): # Adds New Task
    Tem = {'Log': (name[:17] + '..') if len(name) > 17 else name}
    TaskKeeper.append(Tem.copy())
    return txtresponse("1") if simpleResponse else Tem
def dTask(name):  # Clears Everything
    global TaskKeeper
    TaskKeeper = []
def Task(name): # Gets the last n task names. Default n = 30
    TaskReversed = []
    TaskSimple = ""
    maxTask = int(name) if name.isnumeric() else 30
    curTask = 0
    for report in reversed(TaskKeeper):
        curTask += 1
        if curTask > maxTask:
            break
        if simpleResponse:
            TaskSimple += report['Log'] + " " * (19 - len(report['Log'])) + "\n"
        else:
            TaskReversed.append(report)
    if len(TaskKeeper) != 0:
        return txtresponse(TaskSimple.rstrip('\n')) if simpleResponse else {"Data": TaskReversed}
    else:
        return txtresponse("0") if simpleResponse else {"Data": "Dead"}

class TaskList(Resource):
    def __init__(self):
        pass
    def get(self, name):  # Gets the last n task names. Default n = 30
        return Task(name)
    def post(self, name):  # Adds New Task
        return pTask(name)
    def delete(self, name):  # Clears Everything
        dTask(name)
        if simpleResponse:
            return txtresponse("1")
class pTaskList(Resource):
    def __init__(self):
        pass
    def get(self, name):  # Adds New Task
        return pTask(name)
class dTaskList(Resource):
    def __init__(self):
        pass
    def get(self, name):  # Clears Everything
        dTask(name)
        if simpleResponse:
            return txtresponse("1")

api.add_resource(CreateTracker, '/Track/<string:name>')
api.add_resource(pCreateTracker, '/pTrack/<string:name>')
api.add_resource(dCreateTracker, '/dTrack/<string:name>')


api.add_resource(SummaryReport, '/Summary/<string:name>')
api.add_resource(dSummaryReport, '/dSummary/<string:name>')

api.add_resource(TaskList, '/Task/<string:name>')
api.add_resource(pTaskList, '/pTask/<string:name>')
api.add_resource(dTaskList, '/dTask/<string:name>')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
