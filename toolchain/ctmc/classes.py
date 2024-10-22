class Slave:
    num_slaves = 0

    def __init__(self):
        Slave.num_slaves += 1
        self.index = Slave.num_slaves

    def __repr__(self):
        return 'S' + str(self.index)


class Port:
    num_ports = 0

    def __init__(self):
        Port.num_ports += 1
        self.index = Port.num_ports

    def __repr__(self):
        return 'P' + str(self.index)


class Link:
    num_links = 0

    def __init__(self):
        Link.num_links += 1
        self.index = Link.num_links

    def __repr__(self):
        return 'L' + str(self.index)


class Guardian:
    num_guardians = 0

    def __init__(self):
        Guardian.num_guardians += 1
        self.index = Guardian.num_guardians

    def __repr__(self):
        return 'Pg' + str(self.index)


class Switch:
    num_switches = 0

    def __init__(self):
        Switch.num_switches += 1
        self.index = Switch.num_switches

    def __repr__(self):
        return 'Sw' + str(self.index)