from client_sdk_python.module import (
    Module,
)
import json
import rlp
from hexbytes import HexBytes


class Debug(Module):
    def economicConfig(self):
        return json.loads(self.web3.manager.request_blocking("debug_economicConfig", []))

    def setValidatorList(self, node_list):
        data_list = []
        for node_id in node_list:
            data_list.append(bytes.fromhex(node_id))
        data = HexBytes(rlp.encode(data_list)).hex()
        return self.web3.manager.request_blocking("debug_setValidatorList", [data])

    def getWaitSlashingNodeList(self):
        result = self.web3.manager.request_blocking("debug_getWaitSlashingNodeList", [])
        if not result:
            result = []
        return result

