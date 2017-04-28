from . import DAG
from . import utils
from . import nodes
import asyncio

class Subgraph(DAG.Multigraph, nodes.Component):

    def __init__(self, name):
        super(Subgraph, self).__init__(name)
        self.inputs = utils.PortRegister(self)
        self.outputs = utils.PortRegister(self)
        self.color ='grey'


    def export_input(self, port):
        for node in self.iternodes():
            if port in node.inputs.values():
                self.inputs.add(port)

    def export_output(self, port):
        for node in self.iternodes():
            if port in node.outputs.values():
                self.outputs.add(port)
                return


    async def __call__(self):
        if self.dag:
             self.dag.log.debug("Component {} is a subgraph: Adding all nodes to the executor of {}".format(self.name, self.dag.name))
             futures = asyncio.gather(*[asyncio.ensure_future(node())for node in self.iternodes()])
             return futures




