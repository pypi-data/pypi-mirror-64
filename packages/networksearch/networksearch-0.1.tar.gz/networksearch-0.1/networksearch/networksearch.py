import netaddr
from netaddr import IPNetwork, IPRange

class NetworkTree():

    def __init__(self):
        self.root = Node(None)

    def add(self, val):
        networks = getNetworks(val)
        for network in networks:
            path = toBits(network.ip.value)[:network.prefixlen]
            self._add(path, network, self.root)

    def _add(self, path, val, node):
        if(node.value != None):
            return

        if(len(path) == 0):
            node.value = val
            node.left = None
            node.right = None
            return
        
        p = path[:1]
        path = path[1:]

        if(node.left == None):
            node.left = Node(None)
        if(node.right == None):
            node.right = Node(None)

        if(p[0] == 0):
            n = node.left
        else:
            n = node.right

        self._add(path, val, n)

    def deleteTree(self):
        self.root = None

    def printTree(self):
        for val in self.runTree():
            print(str(val) + ' ')

    def runTree(self):
        if(self.root != None):
            for val in self._runTree(self.root):
                yield val

    def _runTree(self, node):
        if(node != None):
            for val in self._runTree(node.left):
                yield val

            if(node.value != None):
                yield node.value

            for val in self._runTree(node.right):
                yield val

    def overlaps(self, val):
        if(self.root != None):
            for network in getNetworks(val):
                path = toBits(network.value)[:network.prefixlen]
                if(self._overlaps(path, self.root)):
                    return True
        return False

    def _overlaps(self, path, node):
        if(node.value != None):
            return True

        p = path[:1]
        path = path[1:]
        
        if(p[0] == 0):
            n = node.left
        else:
            n = node.right

        if(n == None):
            return False

        return self._overlaps(path, n)

        

class Node():
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value

def getNetworks(value):
    try:
        if not isinstance(value, IPNetwork):
            s = value.strip().split('-')
            cidrs=None
            if(len(s) == 2):
                cidrs = netaddr.iprange_to_cidrs(s[0], s[1])
            else:
                cidrs = netaddr.iprange_to_cidrs(s[0], s[0])
            for cidr in cidrs:
                yield cidr
        else:
            yield value
    except GeneratorExit:
        pass
    except:
        print("Bad value: " + value)
        raise

def toBits(val):
    return [val >> i & 1 for i in range(31,-1,-1)]