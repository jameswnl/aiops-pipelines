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
    name='Outlier Detection pipeline',
    description='A pipeline for Outlier Detection.'
)
def od_pipeline():
    """A pipeline with two sequential steps."""

    mount = '/mnt'

    vop = dsl.VolumeOp(
        name="create_pvc",
        resource_name="my-pvc",
        size="2Gi",
        modes=dsl.VOLUME_MODE_RWM
    )

    
    def data_collection():
        return dsl.ContainerOp(
            name='Data collection',
            image='jameswong/data-collector:latest',
            command=['sh', '-c'],
            arguments=['git show --summary && cp /app/*.json $0 && touch /app/results.txt && ls -l /app', mount],
            file_outputs={
                'data': '/app/results.txt',
            },
            pvolumes={mount: vop.volume}
        )

    def detection(input):
        return dsl.ContainerOp(
            name="Outlier Detection",
            image='jameswong/outlier-detection:latest',
            command=["sh", "-c"],
            arguments=[
                "git show --summary && ls -al $0 && ls $1 && python start.py --input_path $0/$2 --output_path $0 --job_id 1",
                mount,
                input,
                '1212729.json',
            ],
            pvolumes={mount: vop.volume}
        )
    
    collect_task = data_collection().set_image_pull_policy('Always')
    detection_task = detection(collect_task.output).set_image_pull_policy('Always')

if __name__ == '__main__':
    print(__file__ + '.zip')
    kfp.compiler.Compiler().compile(od_pipeline, __file__ + '.zip')

