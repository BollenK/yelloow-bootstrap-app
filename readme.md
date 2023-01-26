# Yelloow - Backend Platform
In dit document wordt het doel, de architectuur en de opzet van het Yelloow Backend Platform beschreven. Het Yelloow Backend Platform zal de laag zijn tussen externe databronnen– zoals Harvest en Confluence– en de applicatie in PowerBI. Het Backend Platform zal een applicatie bevatten die data uit verschillende bronnen kan ontsluiten, om kan zetten in het standaard formaat (zoals gedefinieerd in het GDM) en vervolgens ook weg kan schrijven in het GDM. Ook zal het Backend Platform de database beheren. De tabellen en relaties tussen de tabellen staan gedefinieerd in de code en op basis daarvan zal de database worden gegenereerd. Als laatste kan het Backend Platform in een later stadium een component bevatten dat ervoor zorgt dat de data in het GDM up-to-data is met de externe databronnen. 

## Architectuur
### Project structuur
Het project is opgedeeld in een bepaalde structuur waarin het mogelijk is voor verschillende onderdelen van het systeem gedeelde logica en schema definities kunnen gebruiken. De structuur is als volgt:
* src
    * yelloow
    * adapters `# sub project waarin de logica en definities van de adapters staan`
    * api `# sub project voor de api`
    * app `# sub project voor de applicatie`
    * shared `# gedeelde folder die vanuit alle sub projecten te benaderen is`
        * models `# model definities`
        * database `# definitie voor connectie naar database en helper functies voor het toevoegen van bijvoorbeeld een database sessie als keyword  argument aan een functie`
        * (bijv.) KPI (een domein klasse)
        * crud.py `# Voor alle domein klasse, een los crud bestand waar de meest gebruikte database operaties worden gedefinieerd`
        * config.py `# het- zoals hieronder beschreven- config bestand dat alle onderdelen van het systeem toegang geeft tot een single point of reference als het aankomt op configuratie variablen.`
        * enums.py `# alle enumeraties`
        * log.py `# logging functionaliteit`

### Docker
Alle onderdelen in de backend van Yelloow zijn gecontaineriseerd. De database draait in een container alsmede de applicatie die over een netwerk verbinding met elkaar kunnen maken. Zowel de applicatie als de database draaien in een Docker container. Voor beide zijn images gedefinieerd, de database kan worden benaderd via andere containers en vanaf je lokale apparaat door de exposed port.

### Globale architectuur
In dit kopje wordt de globale architectuur/opzet van het backend platform beschreven met nadruk op het ophalen, combineren en wegschrijven van kpi data. Het platform bestaat uit vier componenten:
* Adapters: verantwoordelijk voor de logica van het daadwerkelijke ophalen van data uit externe bronnen (lokale bestanden of via de cloud).
* Database
* App: de app is verantwoordelijk voor het ophalen en combineren van data uit adapters, te bewerken en om te zetten in het format van het generieke datamodel en dat vervolgens weg te schrijven naar de database.
* Api: de api is nog niet ontwikkeld.

![Globale opzet yelloow backend platform](./files/architecture.png "Architecture Yelloow Platform")


### Development
#### Environments
Om het ontwikkelen en uitrollen van de software makkelijker te maken, wordt er gebruik gemaakt van verschillende environments. In de root van het project staat een `.env-example` bestand. Dit bestand bevat de definities van alle environment variables die nodig zijn om zowel de database als de applicatie te draaien. Zoals **in de readme** ook te lezen is, dient de inhoud van dit bestand te worden gekopieerd naar een nieuw bestand: `.env` in de root van het project. Voor andere omgevingen kunnen er andere .env bestanden worden aangemaakt, bijvoorbeeld voor het draaien van de applicatie in de Docker omgeving. Als Docker een bepaald .env bestand moet gebruiken, zorg ervoor dat hiernaar verwezen wordt in het docker-compose bestand, en specificeer daar de environment in het volgende format: `docker-<name_of_environment>` als het .env bestand: `.env-docker-<name_of_environment>` heet. Voorbeelden van environment variablen zijn: MYSQL_PASSWORD of AUTHJWT_SECRET_KEY.  Het uitlezen van deze environment variables wordt op twee manieren gedaan:
  1. Het .env bestand wordt in het docker-compose bestand benoemd als bron voor system environment variables, zodat deze beschikbaar zijn vanuit de docker container. 
  2. Onder 'src/yelloow/shared/config.py' leest variablen direct uit het .env bestand. Uit welk .env bestand hier wordt gelezen wordt bepaald aan de hand van de environment waarin gewerkt wordt.

Naast de environment variables bestaat er ook nog een .config bestand. In dit bestand worden andere onderdelen gedefinieerd die minder afhankelijk zijn van bijvoorbeeld de machine of omgeving waarop de containers draaien. Denk hierbij aan de string_collation van tabellen in de database. Of de maximale lengte van een varchar veld.

#### Alembic en SQLAlchemy
Het generieke datamodel is gedefinieerd middels python classes onder `src/yelloow/shared/models/*`. Deze modellen worden door een databasemigratietool Alembic automatisch de database ingezet. Het is mogelijk om na het creeeren van de tabellen wijzigingen aan te brengen of binnen te halen van de Github aan de modellen. Onder het kopje `gebruik` wordt uitgelegd hoe je van je bestaande migratie kan migreren naar de volgende.

## Gebruik
Om de eerste keer de applicatie en de database succesvol te kunnen draaien moeten er een aantal dingen gebeuren

1. Kopieer de inhoud van *.env-example* in twee nieuwe bestanden: *.env-docker-dev* en *.env*. Pas de waarden in de nieuwe bestanden aan. het *.env* bestand is bedoeld voor het configureren van environment variablen op je lokale machine en *.env-docker-dev* voor op de docker container. Hier zit verschil in, bijvoorbeeld de connectie variables van de database. 
2. Zorg ervoor dat 'poetry' is geinstalleerd met pip: `pip install poetry`
3. Run: `poetry install`
4. Run: `make mysql-db`, dit intialiseert de container en start een mysql-server met de credentials zoals in .env-docker-dev
5. Op je lokale machine, run: `python seed_data_dimensation_table.py` en daarna `python initial_seed.py` om de database met tabellen te creeeren, de dimensie tabel te vullen met data en de yelloow_test_data toe te voegen aan het de database.

Om je database te migreren naar de nieuwste versie:
1. Zet de credentials goed in het .ENV bestand
2. Run: `alembic revision --autogenerate -m "<migratie message>"`
3. (Optioneel) Onder: `alembic/versions` is een nieuw bestand verschenen waarin de wijzingen aan de tabellen in python code staan gedefinieerd. In sommige gevallen is het nodig om handmatig wat data om te sluizen om data te behouden. Pas dit zo nodig aan.
4. Run: `alembic upgrade head` om naar de nieuwste migratie te upgraden.