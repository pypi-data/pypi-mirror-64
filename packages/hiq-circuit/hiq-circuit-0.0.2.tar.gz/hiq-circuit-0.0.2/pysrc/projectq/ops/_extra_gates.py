#   Copyright 2019 <Huawei Technologies Co., Ltd>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from projectq.ops import FastForwardingGate, ClassicalInstructionGate


class MetaSwapGate(FastForwardingGate):
    """ Command to the simulator to swap global and local qubits """
    def __str__(self):
        return "SW"


MetaSwap = MetaSwapGate()


class AllocateQuregGate(ClassicalInstructionGate):
    def __init__(self, init=0):
        self.interchangeable_qubit_indices = []
        self._init = init

    @property
    def init(self):
        return self._init

    def __str__(self):
        return "AllocateQureg"
