import yaml


def parse_yaml(filename):
    yamlDict = None

    try:
        with open(filename, "r") as inFile:
            yamlDict = yaml.load(inFile, Loader=yaml.FullLoader)
    except Exception as err:
        print(format(err))
        raise err

    return yamlDict
