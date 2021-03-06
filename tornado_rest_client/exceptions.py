# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright 2014 Nextdoor.com, Inc
"""
:mod:`tornado_rest_client.exceptions`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All common exceptions
"""


class BaseException(Exception):

    """Base Tornado REST Client Exception"""


class RecoverableFailure(BaseException):

    """Base exception that allows calls to be retried"""


class UnrecoverableFailure(BaseException):

    """Base exception that prevents any calls from being retried"""


class InvalidOptions(UnrecoverableFailure):

    """Invalid option arguments passed"""


class InvalidCredentials(UnrecoverableFailure):

    """Invalid or missing credentials"""
