#!/usr/bin/env python3
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import kfp
from kfp import dsl



@dsl.pipeline(
    name='Echo pipeline',
    description='A dummy pipeline.'
)
def od_pipeline():
    """A pipeline with two sequential steps."""

    def echo():
        return dsl.ContainerOp(
            name='Echo',
            image='python:slim',
            command=['sh', '-c'],
            arguments=['ls -l'],
        )
    
    collect_task = echo()
    detection_task = echo().after(collect_task)

if __name__ == '__main__':
    print(__file__ + '.zip')
    kfp.compiler.Compiler().compile(od_pipeline, __file__ + '.zip')
