import yaml


GG_CITY_KEY = "city"
GG_CITY_NAME_KEY = "name"
GG_CITY_REGION_KEY = "region"
GG_CITY_RACE_KEY = "ethnicity"


def parse_yaml(filename):
    yamlDict = None

    try:
        with open(filename, "r") as inFile:
            yamlDict = yaml.load(inFile, Loader=yaml.FullLoader)
    except Exception as err:
        print(format(err))  # DEBUGGING

    return yamlDict
