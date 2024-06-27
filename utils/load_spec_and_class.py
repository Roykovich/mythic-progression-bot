import discord
from discord import app_commands
import typing

detailed_classes = {
    "Death Knight": {
        "Blood": "tank",
        "Frost": "dps",
        "Unholy": "dps"
    },
    "Demon Hunter": {
        "Havoc": "dps",
        "Vengeance": "tank"
    },
    "Druid": {
        "Balance": "dps",
        "Feral": "dps",
        "Guardian": "tank",
        "Restoration": "healer"
    },
    "Evoker": {
        "Augmentation": "dps",
        "Devastation": "dps",
        "Preservation": "healer"
    },
    "Hunter": {
        "Beast Mastery": "dps",
        "Marksmanship": "dps",
        "Survival": "dps"
    },
    "Mage": {
        "Arcane": "dps",
        "Frost": "dps",
        "Fire": "dps"
    },
    "Monk": {
        "Brewmaster": "tank",
        "Mistweaver": "healer",
        "Windwalker": "dps"
    },
    "Paladin": {
        "Holy": "healer",
        "Protection": "tank",
        "Retribution": "dps"
    },
    "Priest": {
        "Holy": "healer",
        "Shadow": "dps",
        "Discipline": "healer"
    },
    "Rogue": {
        "Assassination": "dps",
        "Outlaw": "dps",
        "Subtlety": "dps"
    },
    "Shaman": {
        "Elemental": "dps",
        "Enhancement": "dps",
        "Restoration": "healer"
    },
    "Warlock": {
        "Affliction": "dps",
        "Demonology": "dps",
        "Destruction": "dps"
    },
    "Warrior": {
        "Arms": "dps",
        "Fury": "dps",
        "Protection": "tank"
    }
}

classes = [
    "Death Knight -> Blood",
    "Death Knight -> Frost",
    "Death Knight -> Unholy",
    "Demon Hunter -> Havoc",
    "Demon Hunter -> Vengeance",
    "Druid -> Balance",
    "Druid -> Feral",
    "Druid -> Guardian",
    "Druid -> Restoration",
    "Evoker -> Augmentation",
    "Evoker -> Devastation",
    "Evoker -> Preservation",
    "Hunter -> Beast Mastery",
    "Hunter -> Marksmanship",
    "Hunter -> Survival",
    "Mage -> Arcane",
    "Mage -> Frost",
    "Mage -> Fire",
    "Monk -> Brewmaster",
    "Monk -> Mistweaver",
    "Monk -> Windwalker",
    "Paladin -> Holy",
    "Paladin -> Protection",
    "Paladin -> Retribution",
    "Priest -> Holy",
    "Priest -> Shadow",
    "Priest -> Discipline",
    "Rogue -> Assassination",
    "Rogue -> Outlaw",
    "Rogue -> Subtlety",
    "Shaman -> Elemental",
    "Shaman -> Enhancement",
    "Shaman -> Restoration",
    "Warlock -> Affliction",
    "Warlock -> Demonology",
    "Warlock -> Destruction",
    "Warrior -> Arms",
    "Warrior -> Fury",
    "Warrior -> Protection"
]



def get_classes(similarities: str) -> list:
    return [class_spec for class_spec in classes if similarities.lower() in class_spec.lower()][:24]

async def classes_and_spec_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> typing.List[app_commands.Choice]:
    if not current:
        return []
    
    classes_and_spec = []
    class_and_spec_dictionary = get_classes(current)

    for class_spec in class_and_spec_dictionary:
        classes_and_spec.append(app_commands.Choice(name=class_spec, value=class_spec))
    
    if not classes_and_spec:
        classes_and_spec.append(app_commands.Choice(name=current, value=current))

    return classes_and_spec

