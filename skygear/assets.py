# Copyright 2015 Oursky Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os.path
import logging
import shutil


log = logging.getLogger(__name__)


class CollectorException(Exception):
    pass


class StaticAssetsCollector:
    def __init__(self, dist):
        self.dist = os.path.abspath(dist)

    @property
    def base_path(self):
        return os.path.join(self.dist, 'static')

    def _prefix_path(self, prefix):
        prefix_path = os.path.abspath(os.path.join(self.base_path, prefix))
        if not prefix_path.startswith(self.base_path):
            raise CollectorException('Prefix {} is incorrect.'.format(prefix))
        return prefix_path

    def collect(self, prefix, path):
        prefix_path = self._prefix_path(prefix)
        log.debug('Prefix path is %s', prefix_path)
        shutil.copytree(path, prefix_path, symlinks=True)

    def clean(self):
        shutil.rmtree(self.dist)
