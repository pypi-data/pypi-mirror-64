
def load_config(file_name: str):

    with open(file_name) as f:
        configs = {}
        for s in f.read().splitlines():
            configs[s.split(' ')[0]] = s.split(' ')[-1]
        return configs
