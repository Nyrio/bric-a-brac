# -*- coding: utf-8 -*-
import os
import sys
import re
import json
from collections import defaultdict

TOP_LIMIT = 3
NB_REACTIONS = 100


def main():
    dirpath = sys.argv[1]
    outfile = sys.argv[2]

    print("Running analysis...")
    msg_files = get_messages_backup_files(dirpath)

    with open(os.path.join(dirpath, "users.json"), 'r') as fhandler:
        users_json = json.loads(fhandler.read())
    users = {user["id"]: user["name"]
             for user in users_json}

    reactions_per_user = {user: defaultdict(int) for user in users}
    reactions_counters = defaultdict(int)
    for msg_file in msg_files:
        with open(msg_file, 'r') as fhandler:
            json_data = json.loads(fhandler.read())
        for message in json_data:
            if "reactions" in message:
                for reaction in message["reactions"]:
                    reactions_counters[reaction["name"]] += 1
                    for user in reaction["users"]:
                        reactions_per_user[user][reaction["name"]] += 1

    all_reactions_count = sorted(reactions_counters.items(),
                                 key=lambda x: -x[1])[:NB_REACTIONS]
    top_per_user = {
        user_name: sorted(reactions_per_user[user_id].items(),
                          key=lambda x: -x[1])[:TOP_LIMIT]
        for user_id, user_name in users.items()
    }
    with open(outfile, "w") as fhanfler:
        fhanfler.write(
            "\n".join("%s: %s" % (reac_name, reac_count)
                      for reac_name, reac_count in all_reactions_count)
            + "\n\n---\n\n"
            + "\n".join("%s: %s"
                        % (user_name,
                           " ".join(name for name, cnt in top))
                        for (user_name, top) in top_per_user.items() if top)
        )


def get_messages_backup_files(dirpath):
    """Return all the messages backup files in the given directory recursively
    """
    msg_files = []
    for subdirpath, dirnames, filenames in os.walk(dirpath):
        for filename in filenames:
            if re.search(r"\d{4}-\d{2}-\d{2}\.json", filename):
                msg_files.append(os.path.join(subdirpath, filename))
    return msg_files


if __name__ == "__main__":
    main()
