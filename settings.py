import json
from pydantic import BaseModel, Field
from typing import List
from cat.mad_hatter.decorators import plugin
from .helper import aggiorna_users_tags

class TagSettings(BaseModel):
    tag_list: List[str] = Field(
        default=["tag_1", "tag_2", "tag_3"],
        description="Lista di tag. Modifica e salva per sovrascrivere cat/static/tags.json",
        json_schema_extra={
            "ui": {
                "input_type": "textarea",
                "help": "Inserisci i tag come lista JSON, es: [\"tag1\", \"tag2\"]"
            }
        }
    )

@plugin
def settings_schema():
    return TagSettings.schema()

@plugin
def save_settings(settings: dict):
    # Percorso del file tags.json del CAT
    tags_path = "cat/static/tags.json"
    
    try:
        # Estrae la stringa della lista di tag dalle impostazioni
        tag_list_str = settings["tag_list"]
        
        # Converte la stringa JSON in una lista Python
        tag_list = json.loads(tag_list_str)
        
        # Scrive la lista nel file
        with open(tags_path, "w") as f:
            json.dump(tag_list, f, indent=4)
        
        aggiorna_users_tags()
            
    except json.JSONDecodeError as e:
        print(f"Errore nel formato della lista di tag: {str(e)}")
        raise  # Puoi gestire l'eccezione in modo diverso se preferisci
    except Exception as e:
        print(f"Errore durante l'aggiornamento di {tags_path}: {str(e)}")
        raise