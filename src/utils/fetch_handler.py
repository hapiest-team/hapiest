from utils.hapiest_util import *
from windows.main_window import *
from worker.hapi_worker import *
from utils.log import *
from worker.work_request import *



class FetchErrorKind:
    BadParameter = 1  # This wont be used
    BadParameterGroup = 2  # This wont be used
    BadNuMin = 3  # This wont be used
    BadNuMax = 4  # This wont be used
    BadConnection = 5
    BadIsoList = 6
    FailedToRetreiveData = 7
    FailedToOpenThread = 8
    EmptyName = 9



class FetchError:
    # Constructor for FetchError
    #
    # errors: a FetchErrorKind object
    # description: a textual description of the error
    def __init__(self, error, description=''):
        self.error = error
        self.description = description


class FetchHandler:
    DATA_FILE_REGEX = re.compile('(?P<data_handle>.+)\\.data\\Z')


    @staticmethod
    def get_all_data_names():
        """
        Returns a list of all the different data-names in the data directory.
        """
        files = listdir(Config.data_folder)
        datas = []
        for f in files:
            match = FetchHandler.DATA_FILE_REGEX.match(f)
            if match == None:
                continue
            datas.append(match.groupdict()['data_handle'])
        return datas

    def __init__(self, data_name: str, fetch_window: 'MainWindow', iso_id_list: List[GlobalIsotopologueId],
                 numin: float, numax: float,
                 parameter_groups: List[str] = (), parameters: List[str] = ()):
        """
        test.
        """
        self.data_name = data_name
        self.worker = None
        self.fetch_window = fetch_window
        fetch_window.disable_fetch_button()
        work = HapiWorker.echo(
            data_name=self.data_name,
            iso_id_list=iso_id_list,
            numin=numin,
            numax=numax,
            parameter_groups=parameter_groups,
            parameters=parameters)

        self.worker = HapiWorker(WorkRequest.FETCH, work, callback=fetch_window.fetch_done)
        self.worker.start()
