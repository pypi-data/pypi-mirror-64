# Copyright © 2020 Michael Meyer <me@entrez.cc>
#
# This file is part of pyfreewheel.
#
# pyfreewheel is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# pyfreewheel is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import requests
import json

from .errors import _APIExceptions
errors = _APIExceptions()

class APIResponse:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class API:
    def __init__(self, token):
        self.token = token
        self._uri = 'https://sfx.freewheel.tv/api/inbound/{endpoint}/{item}'

    def update(self, endpt: str, data: dict, **kwargs):
        s_id = kwargs.get('id', '')
        params = { 'token': self.token }
        uri = self._uri.format(endpoint = endpt,
                               item = s_id)
        if endpt not in data.keys():
            data = { endpt: data }
        r = requests.put(uri, params = params, data = json.dumps(data))
        if r.status_code == 200:
            rd = r.json()
            result = APIResponse(**rd)
            return result
        else:
            errors._handle_response_error(r)

    def create(self, endpt: str, data: dict, **kwargs):
        s_id = kwargs.get('id', '')
        params = { 'token': self.token }
        uri = self._uri.format(endpoint = endpt,
                               item = s_id)
        if endpt not in data.keys():
            data = { endpt: data }
        r = requests.post(uri, params = params, data = json.dumps(data))
        if r.status_code == 200:
            rd = r.json()
            result = APIResponse(**rd)
            return result
        else:
            errors._handle_response_error(r)

    def retrieve(self, endpt: str, query: dict = {}, **kwargs):
        s_id = kwargs.get('id', '')
        params = { 'token': self.token }
        params.update(query)
        uri = self._uri.format(endpoint = endpt,
                               item = s_id)
        r = requests.get(uri, params = params)
        if r.status_code == 200:
            rd = r.json()
            result = APIResponse(**rd)
            return result
        else:
            errors._handle_response_error(r)

    def delete(self, endpt: str, **kwargs):
        s_id = kwargs.get('id', '')
        params = { 'token': self.token }
        uri = self._uri.format(endpoint = endpt,
                               item = s_id)
        r = requests.delete(uri, params = params)
        if r.status_code == 200:
            rd = r.json()
            result = APIResponse(**rd)
            return result
        else:
            errors._handle_response_error(r)
