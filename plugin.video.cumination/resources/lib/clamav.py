# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import clamd


class CuminationPlugin(object):
    plugin_name = 'ClamAV'

    def __init__(self, file_data):
        self.file_data = file_data
        self.cd = clamd.ClamdUnixSocket()

    def analyse(self):
        file_name = '/tmp/%s' %  self.file_data['file_uuid']
        scan_data = self.cd.scan(file_name)

        for k,v in scan_data.items():
            malware = v[0]
            classification = v[1]

        if malware == 'OK':
            malware = False
        else:
            malware = True

        result = {"success": True,
                  "result": {'is_malware': malware,
                             'malware_type': classification},
                  "message": None}
        return result

