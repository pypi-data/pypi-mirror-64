# -*- coding: utf-8 -*-
# Smart Contract Reverse Engineering Toolkit: Creation Contract Class
#
# Copyright (C) 2019-2020 CRTK Project
# Author: Hao-Nan Zhu <hao-nan.zhu@outlook.com>
# URL: <https://github.com/Yzstr/CRTK>
# For license information, see LICENSE

# from CRTK.contract import Contract
from CRTK.runtimecontract import RuntimeContract
from CRTK.utilities import split_bytecode


class CreationContract(RuntimeContract):
    def __init__(self, bytecode, address=''):
        self.deployment_bytecode, self.runtime_bytecode, self.bzzr, self.constructor_arguments = split_bytecode(
            bytecode=bytecode)
        super(CreationContract, self).__init__(
            bytecode=self.runtime_bytecode, address=address)
        self.runtime_contract = False

        if self.deployment_bytecode[:2] == '0x':
            self.deployment_bytecode = self.deployment_bytecode[2:]
        else:
            pass

        self.address = super().get_address()

    def get_constructor_arguments(self):
        return self.constructor_arguments

    def get_bzzr(self):
        return self.bzzr
