import discord
import typing
from discord import app_commands

US = {
  "region": "US",
  "servers": [
    {
      "name": "Aegwynn",
      "type": "PvE",
      "population": "High"
    },
    {
      "name": "Aerie Peak",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Agamaggan",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Aggramar",
      "type": "PvE",
      "population": "High"
    },
    {
      "name": "Akama",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Alexstrasza",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Alleria",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Altar of Storms",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Alterac Mountains",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Aman'Thul",
      "type": "PvE",
      "population": "High"
    },
    {
      "name": "Andorhal",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Anetheron",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Antonidas",
      "type": "PvE",
      "population": "High"
    },
    {
      "name": "Anub'arak",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Anvilmar",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Arathor",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Archimonde",
      "type": "PvP",
      "population": "High"
    },
    {
      "name": "Area 52",
      "type": "PvE",
      "population": "High"
    },
    {
      "name": "Argent Dawn",
      "type": "RP",
      "population": "Medium"
    },
    {
      "name": "Arthas",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Arygos",
      "type": "PvE",
      "population": "Low"
    },
    {
      "name": "Azgalor",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Azjol-Nerub",
      "type": "PvE",
      "population": "Low"
    },
    {
      "name": "Azralon",
      "type": "PvP",
      "population": "High"
    },
    {
      "name": "Azshara",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Azuremyst",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Baelgun",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Balnazzar",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Barthilas",
      "type": "PvP",
      "population": "High"
    },
    {
      "name": "Black Dragonflight",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Blackhand",
      "type": "PvE",
      "population": "Low"
    },
    {
      "name": "Blackrock",
      "type": "PvP",
      "population": "High"
    },
    {
      "name": "Blackwater Raiders",
      "type": "RP",
      "population": "Low"
    },
    {
      "name": "Blackwing Lair",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Blades Edge",
      "type": "PvE",
      "population": "Low"
    },
    {
      "name": "Bladefist",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Bleeding Hollow",
      "type": "PvP",
      "population": "High"
    },
    {
      "name": "Blood Furnace",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Bloodhoof",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Bloodscalp",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Bonechewer",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Borean Tundra",
      "type": "PvE",
      "population": "High"
    },
    {
      "name": "Boulderfist",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Bronzebeard",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Burning Blade",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Burning Legion",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Caelestrasz",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Cairne",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Cenarion Circle",
      "type": "RP",
      "population": "Medium"
    },
    {
      "name": "Cenarius",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Cho'gall",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Chromaggus",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Coilfang",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Crushridge",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Daggerspine",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Dalaran",
      "type": "PvE",
      "population": "High"
    },
    {
      "name": "Dalvengyr",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Dark Iron",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Darkspear",
     

 "type": "PvP",
      "population": "High"
    },
    {
      "name": "Darrowmere",
      "type": "PvE",
      "population": "Low"
    },
    {
      "name": "Dath'Remar",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Dawnbringer",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Deathwing",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Demon Soul",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Dentarg",
      "type": "PvE",
      "population": "Low"
    },
    {
      "name": "Destromath",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Dethecus",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Detheroc",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Doomhammer",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Draenor",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Dragonblight",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Dragonmaw",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Drak'Tharon",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Drak'thul",
      "type": "PvE",
      "population": "Low"
    },
    {
      "name": "Draka",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Drakkari",
      "type": "PvP",
      "population": "High"
    },
    {
      "name": "Dreadmaul",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Drenden",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Dunemaul",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Durotan",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Duskwood",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Earthen Ring",
      "type": "RP",
      "population": "Medium"
    },
    {
      "name": "Echo Isles",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Eitrigg",
      "type": "PvE",
      "population": "Low"
    },
    {
      "name": "Eldre'Thalas",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Elune",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Emerald Dream",
      "type": "RP",
      "population": "High"
    },
    {
      "name": "Eonar",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Eredar",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Executus",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Exodar",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Farstriders",
      "type": "RP",
      "population": "Low"
    },
    {
      "name": "Feathermoon",
      "type": "RP",
      "population": "Medium"
    },
    {
      "name": "Fenris",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Firetree",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Fizzcrank",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Frostmane",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Frostmourne",
      "type": "PvP",
      "population": "High"
    },
    {
      "name": "Frostwolf",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Galakrond",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Gallywix",
      "type": "PvP",
      "population": "High"
    },
    {
      "name": "Garithos",
      "type": "PvE",
      "population": "Low"
    },
    {
      "name": "Garona",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Garrosh",
      "type": "PvE",
      "population": "Low"
    },
    {
      "name": "Ghostlands",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Gilneas",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Gnomeregan",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Goldrinn",
      "type": "PvE",
      "population": "High"
    },
    {
      "name": "Gorefiend",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Gorgonnash",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Greymane",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Grizzly Hills",
      "type": "PvE",
      "population": "High"
    },
    {
      "name": "Gul'dan",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Gundrak",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Gurubashi",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Hakkar",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Haomarush",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Hellscream",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Hydraxis",
      "type": "PvE",
      "population": "Low"
    },
    {
      "name": "Hyjal",
      "type": "PvE",
      "population": "High"
    },
    {
      "name": "Icecrown",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Illidan",
      "type": "PvP",
      "population": "High"
    },
    {
      "name": "Jaedenar",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Jubei'Thos",
      "type": "PvP",
      "population": "High"
    },
    {
      "name": "Kael'thas",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Kalecgos",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Kargath",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Kel'Thuzad",
      "type": "PvP",
      "population": "High"
    },
    {
      "name": "Khadgar",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Khaz Modan",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Khaz'goroth",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Kil'jaeden",
      "type": "PvP",
      "population": "High"
    },
    {
      "name": "Kilrogg",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Kirin Tor",
      "type": "RP",
      "population": "Medium"
    },
    {
      "name": "Korgath",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Korialstrasz",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Kul Tiras",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Laughing Skull",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Lethon",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Lightbringer",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Lightning's Blade",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Lightninghoof",
      "type": "RP",
      "population": "Low"
    },
    {
      "name": "Llane",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Lothar",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Madoran",
      "type": "PvE",
      "population": "Low"
    },
    {
      "name": "Maelstrom",
      "type": "RP",
      "population": "Low"
    },
    {
      "name": "Magtheridon",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Maiev",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Mal'Ganis",
      "type": "PvP",
      "population": "High"
    },
    {
      "name": "Malfurion",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Malorne",
      "type": "PvE",
      "population": "Low"
    },
    {
      "name": "Malygos",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Mannoroth",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Medivh",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Misha",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Mok'Nathal",
      "type": "PvE",
      "population": "Low"
    },
    {
      "name": "Moon Guard",
      "type": "RP",
      "population": "High"
    },
    {
      "name": "Moonrunner",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Mug'thol",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Muradin",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Nagrand",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Nathrezim",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Ner'zhul",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Nesingwary",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Nordrassil",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Norgannon",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Onyxia",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Perenolde",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Proudmoore",
      "type": "PvE",
      "population": "High"
    },
    {
      "name": "Quel'Thalas",
      "type": "PvE",
      "population": "High"
    },
    {
      "name": "Ragnaros",
      "type": "PvP",
      "population": "High"
    },
    {
      "name": "Ravencrest",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Ravenholdt",
      "type": "RP",
      "population": "Low"
    },
    {
      "name": "Rexxar",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Rivendare",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Runetotem",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Sargeras",
      "type": "PvP",
      "population": "High"
    },
    {
      "name": "Saurfang",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Scarlet Crusade",
      "type": "RP",
      "population": "Low"
    },
    {
      "name": "Scilla",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Sen'jin",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Sentinels",
      "type": "RP",
      "population": "Medium"
    },
    {
      "name": "Shadow Council",
      "type": "RP",
      "population": "Low"
    },
    {
      "name": "Shadowmoon",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Shadowsong",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Shandris",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Shattered Halls",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Shattered Hand",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Shu'halo",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Silver Hand",
      "type": "RP",
      "population": "Low"
    },
    {
      "name": "Silvermoon",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Sisters of Elune",
      "type": "RP",
      "population": "Medium"
    },
    {
      "name": "Skullcrusher",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Skywall",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Smolderthorn",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Spinebreaker",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Spirestone",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Staghelm",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Steamwheedle Cartel",
      "type": "RP",
      "population": "Low"
    },
    {
      "name": "Stonemaul",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Stormrage",
      "type": "PvE",
      "population": "High"
    },
    {
      "name": "Stormreaver",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Stormscale",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Suramar",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Tanaris",
      "type":

 "PvE",
      "population": "Medium"
    },
    {
      "name": "Terenas",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Terokkar",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Thaurissan",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "The Forgotten Coast",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "The Scryers",
      "type": "RP",
      "population": "Low"
    },
    {
      "name": "The Underbog",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "The Venture Co",
      "type": "RP",
      "population": "Low"
    },
    {
      "name": "Thorium Brotherhood",
      "type": "RP",
      "population": "Low"
    },
    {
      "name": "Thrall",
      "type": "PvE",
      "population": "High"
    },
    {
      "name": "Thunderhorn",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Thunderlord",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Tichondrius",
      "type": "PvP",
      "population": "High"
    },
    {
      "name": "Tortheldrin",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Trollbane",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Turalyon",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Twisting Nether",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Uldaman",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Uldum",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Undermine",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Ursin",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Uther",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Vashj",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Vek'nilash",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Velen",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Warsong",
      "type": "PvP",
      "population": "Medium"
    },
    {
      "name": "Whisperwind",
      "type": "PvE",
      "population": "High"
    },
    {
      "name": "Wildhammer",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Windrunner",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Winterhoof",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Wyrmrest Accord",
      "type": "RP",
      "population": "Medium"
    },
    {
      "name": "Ysera",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Ysondre",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Zangarmarsh",
      "type": "PvE",
      "population": "Medium"
    },
    {
      "name": "Zul'jin",
      "type": "PvE",
      "population": "High"
    },
    {
      "name": "Zuluhed",
      "type": "PvP",
      "population": "Low"
    },
    {
      "name": "Zuluhed",
      "type": "PvP",
      "population": "Low"
    }
  ]
}

def get_realms(similarities: str) -> list:
    return [server for server in US["servers"] if similarities.lower() in server["name"].lower()][:24]

async def realms_autocomplete(
    interaction: discord.Interaction, 
    current: str
) -> typing.List[app_commands.Choice[str]]:
    if not current:
        return []
    
    realms = []
    realm_dictionary = get_realms(current)
    
    for realm in realm_dictionary:
        realms.append(app_commands.Choice(name=realm['name'], value=realm['name']))

    if not realms:
        return [app_commands.Choice(name=current, value=current)]

    return realms