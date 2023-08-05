import logging
import os
import re
from tempfile import NamedTemporaryFile
from appdirs import user_config_dir

import pandas as pd
from pandas import DataFrame

import sensiml.base.utility as utility
from sensiml.datamanager import (
    Functions,
    PlatformDescriptions,
    PipelineSeeds,
    Projects,
    SegmenterSet,
)
from sensiml.datamanager.knowledgepack import get_knowledgepack, get_knowledgepacks
from sensiml.datasets import DataSets
from sensiml.connection import Connection

# from sensiml.base.exceptions import *
from sensiml.pipeline import Pipeline
from sensiml.base.snippets import Snippets, function_help
from time import sleep

config_dir = user_config_dir(__name__.split(".")[0], False)

logger = logging.getLogger("SensiML")


def print_list(func):
    """ This is a wrapper for printing out lists of objects stored in SensiML Cloud """

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if len(result.keys()) == 0 and kwargs.get("silent", False) == False:
            print(
                "No {} stored on SensiML Cloud for this project.".format(
                    " ".join(func.__name__.split("_")[1:])
                )
            )
            return None
        if kwargs.get("get_objects", False) is True:
            return result

        tmp_dict = [
            {"Name": name, "UUID": item.uuid, "Created": item.created_at}
            for name, item in result.items()
        ]

        return DataFrame(tmp_dict, columns=["Name", "Created", "UUID"])

    return wrapper


class SensiML(object):
    """Entrance to SensiML Analytic Suite"""

    # Server Minimum Version For Campatibility
    __minversion__ = "2019.1.0"

    def __init__(
        self,
        server="https://sensiml.cloud/",
        path="connect.cfg",
        use_jedi=False,
        **kwargs
    ):

        self._project = None
        self._pipeline = None
        self._knowledgepack_list = None
        auth_url = server + "oauth/"

        self._connection = Connection(
            server=server, auth_url=auth_url, path=path, **kwargs
        )

        self.validate_client_version(kwargs.get("skip_validate", True))
        self.projects = Projects(self._connection)
        self.datasets = DataSets()
        self.functions = Functions(self._connection)
        self.platforms = PlatformDescriptions(self._connection)
        self.seeds = PipelineSeeds(self._connection)
        self.snippets = Snippets(
            self.list_functions(kp_functions=False),
            self.functions.function_list,
            self.seeds,
        )
        self._feature_files = None

        if use_jedi is False:
            self.setup_jedi_false()

    def setup_jedi_false(self):
        """ This is a temporary bug fix in ipython autocomplete """
        try:
            mgc = get_ipython().magic
            mgc("%config Completer.use_jedi = False")
        except:
            pass

    @property
    def knowledgepack_list(self):
        if self._knowledgepack_list is None:
            self.knowledgepack_list = get_knowledgepacks(self._connection)

        return self._knowledgepack_list

    @knowledgepack_list.setter
    def knowledgepack_list(self, value):
        if value is None:
            self._knowledgepack_list = None
        else:
            self._knowledgepack_list = value.rename(
                columns={
                    "name": "Name",
                    "project_name": "Project",
                    "sandbox_name": "Pipeline",
                    "uuid": "kp_uuid",
                    "created_at": "Created",
                }
            )

    def validate_client_version(self, skip_validate=True):
        """ Perform a Validation check to see if this version of SensiML is up to date with the latest. """

        if skip_validate:
            return

        url = "version"

        response = self._connection.request("get", url)
        response_data, err = utility.check_server_response(response)

        if response_data["SensiML_Python_Library_Windows"] != self.__minversion__:
            print(
                "SensiML Python Client Library is out of date. Update before connecting to the server."
            )
            print("In order to update sensiml client use 'pip install sensiml -U'.")
            print(
                "For Instrunctions on updating SensiML Client for the Analytic Studio visit https://sensiml.atlassian.net/wiki/spaces/SS/pages/115179614/Updating+SensiML+Client"
            )
            raise Exception("Python Client is out of date.")

    def logout(self, name=None):
        """Logs out of the current connection."""
        if name is None:
            name = self._connection.server_name

        Connection.logout(name)

    def get_function(self, name):
        """Gets a function method call"""
        return self.functions.function_list[name]

    def function_description(self, name):
        """Gets a description of a pipeline function."""
        print(self.functions.create_function_call(name).__doc__)

    def function_help(self, name):
        """Prints a shortened description of a function. """
        print(function_help(self.functions.function_list[name]))

    def list_functions(
        self, functype=None, subtype=None, kp_functions=False
    ):
        """Lists all of the functions available on SensiML Cloud

        Returns:
            Dataframe

        Args:
            functype (str, None): Return only functions with the specified type. ie. "Segmenter"
            subtype (str, None): Return only functions with the specified subtype. ie. "Sensor"
            kp_functions (boolean, True): Return only functions that run on tbe loaded to a device.
            Excludes functions such as feature selection and model training.
        """

        df = (
            DataFrame(
                [
                    {
                        "NAME": f.name,
                        "TYPE": f.type,
                        "DESCRIPTION": f.description.lstrip("\n").lstrip(" "),
                        "SUBTYPE": f.subtype,
                        "KP FUNCTION": f.has_c_version,
                    }
                    for f in self.functions.get_functions()
                ]
            )
            .sort_values(by=["TYPE", "SUBTYPE"])
            .reset_index(drop=True)[
                ["NAME", "TYPE", "SUBTYPE", "DESCRIPTION", "KP FUNCTION"]
            ]
        )

        if functype:
            df = df[df["TYPE"] == functype]

        if subtype:
            df = df[df["SUBTYPE"] == subtype]

        if kp_functions:
            df = df[df["KP FUNCTION"] == True][
                ["NAME", "TYPE", "SUBTYPE", "DESCRIPTION"]
            ]

        return df.reset_index(drop=True)

    def delete_project(self):
        """Deletes a project """
        if self._project is not None:
            self._project.delete()

    @print_list
    def list_projects(self, get_objects=False, silent=False):
        """Lists all of the projects on SensiML Cloud

        Returns:
            DataFrame: projects on SensiML Cloud
        """
        return self.projects.build_project_dict()

    def list_segmenters(self,):
        if self._project is None:
            print("project must be set to list segmenters.")
            return None

        segmenters = SegmenterSet(self._connection, self._project)

        if not len(segmenters.objs):
            print("No segmenters stored on the Cloud.")
            return None

        return segmenters.to_dataframe()

    def list_seeds(self):
        """Lists all of the pipeline seeds on SensiML Cloud

        Returns:
            DataFrame: pipeline seeds on SensiML Cloud
        """
        return DataFrame(
            {
                "Name": [s.name for s in self.seeds],
                "Description": [s.description for s in self.seeds],
            }
        )

    def list_knowledgepacks(self, unnamed=False):
        """Lists all of the knowledgepacks associated with a team

        Returns:
            DataFrame: knowledgepacks on SensiML Cloud
        """
        if self.knowledgepack_list is None:
            print("No Knowledgepacks stored for this team on the cloud.")
            return None

        knowledgepack_list = self.knowledgepack_list
        knowledgepack_list = knowledgepack_list.rename(
            columns={"knowledgepack_description": "kp_description"}
        )

        if unnamed:
            return knowledgepack_list[
                ["Name", "Created", "Project", "Pipeline", "kp_uuid", "kp_description"]
            ]

        return knowledgepack_list[knowledgepack_list["Name"] != ""][
            ["Name", "Created", "Project", "Pipeline", "kp_uuid", "kp_description"]
        ]

    def get_knowledgepack(self, uuid):
        """retrieve knowledgepack by uuid from the server associated with current project

        Args:
            uuid (str): unique identifier for knowledgepack

        Returns:
            TYPE: a knowledgepack object
        """

        return get_knowledgepack(uuid, self._connection)

    @property
    def project(self):
        """The active project"""
        return self._project

    @print_list
    def list_featurefiles(self, get_objects=False, silent=False):
        """List all feature and data files for the active project.

        Args:
            get_objects (bool, False): Also return the featurefile objects.

        """
        if self._project is None:
            raise Exception("Project must be set to perform this action.")
        return self._project._feature_files.build_featurefile_list()

    @print_list
    def list_datafiles(self, get_objects=False, silent=False):
        """List all feature and data files for the active project.

        Args:
            get_objects (bool, False): Also return the featurefile objects.

        """
        if self._project is None:
            raise Exception("Project must be set to perform this action.")

        return self._project._feature_files.build_featurefile_list()

    @print_list
    def list_captures(self, get_objects=False):
        """List all captures for the active project

        Args:
            get_objects (bool, False): Also return the capture objects.

        """
        if self._project is None:
            raise Exception("Project must be set to perform this action.")

        return self._project._captures.build_capture_list()

    @print_list
    def list_capture_configurations(self, get_objects=False):
        """List all captures for the active project

        Args:
            get_objects (bool, False): Also return the capture objects.

        """
        if self._project is None:
            raise Exception("Project must be set to perform this action.")

        return self._project._capture_configurations.build_capture_list()

    @print_list
    def list_sandboxes(self, get_objects=False):
        """List all sandboxes for the active project.

        Args:
            get_objects (bool, False): Also return the sandbox objects.

        """
        if self._project is None:
            raise Exception("Project must be set to perform this action.")
        return self._project._sandboxes.build_sandbox_list()

    @print_list
    def list_queries(self, get_objects=False):
        """List all queries for the active project.

        Args:
            get_objects (bool, False): Also return the query objects.

        """
        if self._project is None:
            raise Exception("Project must be set to perform this action.")
        return self._project._queries.build_query_list()

    @project.setter
    def project(self, name):
        self._project = self.projects.get_or_create_project(name)

    @property
    def pipeline(self):
        """The active pipeline"""
        return self._pipeline

    @pipeline.setter
    def pipeline(self, name):
        if self._project is None:
            raise Exception("Project must be set before a pipeline can be created")

        self._pipeline = Pipeline(self, name=name)

    def create_query(
        self,
        name,
        columns=[],
        metadata_columns=[],
        metadata_filter="",
        segmenter=None,
        label_column="",
        combine_labels=None,
        force=False,
        renderer=None,
    ):
        """Create a query to use as input data in a pipeline.

        Args:
            name (str): Name of the query.
            columns (list, optional): Columns to add to the query result.
            metadata_columns (list, optional): Metadata to add to the query result.
            metadata_filter (str, optional): Filter to apply to the query.
            segmenter (int, optional): Segmenter to filter query by.
            force (bool, False): If True overwrite the query on kb cloud.

        Returns:
            object: Returns a query object that was created.
        """
        query = self.project.queries.get_query_by_name(name)
        new = False
        if query is not None and not force:
            raise QueryExistsException(
                "Query already exists. Set force=True to overwrite."
            )
        elif query is not None and force:
            query.columns.clear()
            query.metadata_columns.clear()
            query.metadata_filter = ""
            query.label_column = ""
        else:
            query = self.project.queries.new_query()
            query.name = name
            new = True

        for col in columns:
            logger.debug("query_column:" + str(col))
            query.columns.add(col)

        for col in metadata_columns:
            logger.debug("query_metadata_column:" + str(col))
            query.metadata_columns.add(col)

        if metadata_filter:
            logger.debug("query_metadata_filter:" + str(metadata_filter))
            query.metadata_filter = metadata_filter

        if label_column:
            query.label_column = label_column

        if combine_labels:
            query.combine_labels = combine_labels

        query.segmenter = segmenter

        if new:
            query.insert(renderer=renderer)
        else:
            query.update(renderer=renderer)

        return query

    def get_query(self, name):
        if self.project is None:
            print("Project must be set first")
            return

        return self.project.queries.get_query_by_name(name)

    def upload_data_file(self, name, path, force=False):
        """Upload data source from local CSV file"""
        logger.debug("set_feature_file:" + name + ":" + path)
        print('Uploading file "{}" to SensiML Cloud.'.format(name))
        if name[-4:] != ".csv":
            name = "{}.csv".format(name)

        feature_file = self._project._feature_files.get_featurefile_by_name(name)
        if feature_file is None:
            new = True
            feature_file = self._project.featurefiles.new_featurefile()
        else:
            new = False
            if not force:
                raise FeatureFileExistsException()

        feature_file.filename = name
        feature_file.path = path
        if new:
            feature_file.insert()
        else:
            feature_file.update()

        print('Upload of file "{}"  to SensiMLKB  Cloud completed.'.format(name))

        return self

    def upload_dataframe(self, name, dataframe, force=False):
        """Set data source from a pandas DataFrame."""
        logger.debug("set_data:" + name)

        with NamedTemporaryFile(delete=False) as temp:
            dataframe.to_csv(temp.name, index=False)
            logger.debug("set_dataframe:" + name + ":" + temp.name)
            self.upload_data_file(name, temp.name, force=force)

        os.remove(temp.name)

        return self

    def clear_session_cache(self):
        for _, _, filenames in os.walk(config_dir):
            for filename in filenames:
                if re.match(r"_token.json$", filename):
                    os.unlink(filename)

    def get_feature_statistics_results(self, query_name):
        query = self._project.queries.get_query_by_name(query_name)

        for i in range(100):
            results = query.get_feature_statistics()

            if results.get("results", None):
                return pd.DataFrame(results["results"])
            sleep(5)

        print("Not able to reach the results in the expected time. ")
        return results
