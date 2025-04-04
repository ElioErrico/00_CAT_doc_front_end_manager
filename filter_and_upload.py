from cat.mad_hatter.decorators import hook
import json
from cat.log import log

@hook  # default priority = 1
def before_cat_recalls_declarative_memories(declarative_recall_config, cat):
    # filter memories using custom metadata. 
    # N.B. you must add the metadata when uploading the document! 

    user=cat.user_id
    user_status_path="cat/static/user_status.json"
    file=open(user_status_path, "r")
    user_status=json.load(file)
    user_status[user][user] = True
    # cat.send_ws_message(f"{str(user_status[user])}","chat")

    declarative_recall_config["metadata"] = user_status[user]
    # Filtra il dizionario mantenendo solo le coppie chiave-valore con valore True
    declarative_recall_config["metadata"]={k: v for k, v in declarative_recall_config["metadata"].items() if v}
    # cat.send_ws_message(f"{str(user_status[user])}","chat")
    log.critical(f'metadata: {str(declarative_recall_config["metadata"])}')



    return declarative_recall_config


@hook
def before_rabbithole_stores_documents(docs, cat):

    user=cat.user_id
    user_status_path="cat/static/user_status.json"
    file=open(user_status_path, "r")
    user_status=json.load(file)
    metadata_for_upload = user_status[user]

    for doc in docs:
        doc.metadata.update(metadata_for_upload)

        cat.send_ws_message(f"{str(metadata_for_upload)}","chat")

    return docs
