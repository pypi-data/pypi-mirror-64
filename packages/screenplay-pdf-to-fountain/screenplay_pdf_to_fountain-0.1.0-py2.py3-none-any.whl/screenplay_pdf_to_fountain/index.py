import json
import argparse
import pprint
# from screenplain.export.fdx import to_fdx

pp = pprint.PrettyPrinter(indent=4)


def addCharacter(fountainOutput, whichCharacter, section):
    modifier = " ({})".format(section["content"][whichCharacter]["modifier"]) if section[
        "content"][whichCharacter]["modifier"] != None else ""
    character = section["content"][whichCharacter]["character"]
    isDual = "^" if whichCharacter == "character2" else ""
    fountainOutput += "{}{}{}\n".format(
        character, modifier, isDual)
    for dialogue in section["content"][whichCharacter]["dialogue"]:
        fountainOutput += "{}\n".format(
            dialogue.encode('utf-8'))
    return fountainOutput


def generateFountain(scriptJson):
    fountainOutput = ""
    for page in scriptJson:
        currentSceneNumber = 0
        for content in page["content"]:
            if "scene_number" in content and content["scene_number"] != currentSceneNumber:
                currentSceneNumber = content["scene_number"]
                currentScene = content["scene_info"]
                time = " ".join(
                    currentScene["time"]) if currentScene["time"] != None else ""
                fountainOutput += "{} {} {}\n\n".format(
                    currentScene["region"].encode('utf-8'), currentScene["location"].encode('utf-8'), time)

            if "scene" in content:
                for section in content["scene"]:
                    if section["type"] == "ACTION":
                        for i, sectionContent in enumerate(section["content"]):
                            fountainOutput += "{}\n".format(
                                sectionContent["text"].encode('utf-8'))
                            if i + 1 < len(section["content"]):
                                fountainOutput += "\n"
                    elif section["type"] == "CHARACTER":
                        modifier = " ({})".format(
                            section["content"]["modifier"].encode('utf-8')) if section["content"]["modifier"] != None else ""
                        fountainOutput += "{}{}\n".format(
                            section["content"]["character"].encode('utf-8'), modifier)
                        for dialogue in section["content"]["dialogue"]:
                            fountainOutput += "{}\n".format(
                                dialogue.encode('utf-8'))
                    elif section["type"] == "TRANSITION":
                        fountainOutput += "{}\n".format(
                            section["content"]["text"].encode('utf-8'))
                    elif section["type"] == "DUAL_DIALOGUE":
                        fountainOutput = addCharacter(
                            fountainOutput, "character1", section)
                        fountainOutput += "\n"
                        fountainOutput = addCharacter(
                            fountainOutput, "character2", section)
                    fountainOutput += "\n"
            else:
                fountainOutput += "{}\n\n".format(
                    content["text"].encode('utf-8'))

    return fountainOutput


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Parse Screenplay PDF into JSON')
    parser.add_argument('-s', metavar='screenplay', type=str,
                        help='screenplay PDF filename', required=True)

    parser.add_argument('-o', metavar='output file', type=int,
                        help='name of ouput file', required=False)

    # start from skipPage set up by user.  default to 0
    args = parser.parse_args()

    scriptPath = args.s
    outputPath = args.o if args.o else args.s[0: args.s.index(
        '.')] + ".fountain"

    with open(scriptPath) as f:
        scriptJson = json.load(f)
        fountainOutput = generateFountain(scriptJson)
        file1 = open('./result.fountain', 'w+')
        file1.write(fountainOutput)
        file1.close()
