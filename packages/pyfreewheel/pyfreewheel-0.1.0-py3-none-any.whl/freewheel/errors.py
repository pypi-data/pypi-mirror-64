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
import re

class _APIExceptions:
    class APIError(Exception):
        '''general bad response from Freewheel API'''
    class BadToken(APIError):
        '''issue with user-provided API token'''
    class BadTarget(APIError):
        '''issue with user-provided target (i.e. item id)'''
    def _handle_response_error(self, resp):
        token_regex = re.compile('Token (parameter is missing|is invalid)')
        target_regex = re.compile('The (\w+ targeted|targeted \w+) is invalid\.')
        try:
            j = resp.json()
        except ValueError:
            j = {}

        msg = j.get('message', 'API call returned {0:n} {1:s}'.format(
            resp.status_code, resp.reason
        ))

        if token_regex.match(msg) is not None:
            raise self.BadToken(msg)
        elif target_regex.match(msg) is not None:
            raise self.BadTarget(msg)
        else:
            raise self.APIError(msg)
