from __future__ import division, absolute_import, print_function
from airflow.plugins_manager import AirflowPlugin
import operators
import helpers
# Defining the plugin class
class CredilyticsPlugin(AirflowPlugin):
    name = "credilytics_plugin"
    operators = [
        operators.TransformOperator
    ]
    helpers = [
        helpers.SqlQueriesCredilytics
    ]