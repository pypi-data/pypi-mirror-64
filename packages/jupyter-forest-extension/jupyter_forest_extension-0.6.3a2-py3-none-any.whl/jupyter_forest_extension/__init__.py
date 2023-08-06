##############################################################################
# Copyright 2019-2020 Rigetti Computing
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
##############################################################################
from jupyter_forest_extension.jupyter_version_check_handler import JupyterVersionCheckHandler
from jupyter_forest_extension.version_check_code_handler import VersionCheckCodeHandler
from jupyter_forest_extension.version_check_handler import VersionCheckHandler
from notebook.utils import url_path_join


def _jupyter_server_extension_paths():
    """
    Set up the server extension for collecting metrics
    """
    return [{
        'module': 'jupyter_forest_extension',
    }]


def load_jupyter_server_extension(nbapp):
    """
    Called during notebook start
    """
    check_code_pattern = url_path_join(nbapp.web_app.settings['base_url'], '/version_management/check_code')
    check_pattern = url_path_join(nbapp.web_app.settings['base_url'], '/version_management/check')
    check_jupyter_extensions_pattern = url_path_join(nbapp.web_app.settings['base_url'],
                                                     '/version_management/check_jupyter_extensions')
    # update_pattern = url_path_join(nbapp.web_app.settings['base_url'], '/version_management/update')
    # update_jupyter_extensions_pattern = url_path_join(nbapp.web_app.settings['base_url'],
    #                                                   '/version_management/update_jupyter_extensions')
    nbapp.web_app.add_handlers('.*', [(check_pattern, VersionCheckHandler),
                                      (check_code_pattern, VersionCheckCodeHandler),
                                      (check_jupyter_extensions_pattern, JupyterVersionCheckHandler)])
