from random import randint, choice
from faker import Faker

def generate_data():

    security_prefixes = {"(U)": 0, "(C)": 1, "(S)": 2, "(TS)": 3}

    # Extensive military vocab pools for realism and variation
    locations = [
        "Base Alpha", "Forward Operating Post", "Sector 7", "North Ridge", "Supply Depot",
        "Echo Outpost", "Delta Zone", "Hill 45", "Bravo Camp", "Zone Red"
    ]

    assets = [
        "drones", "armored vehicles", "satellite uplinks", "logistics convoys", "encrypted servers",
        "communication arrays", "recon helicopters", "infantry units", "radar stations", "naval vessels"
    ]

    operations = [
        "Operation Vortex", "Project Horizon", "Mission Phantom", "Directive Eclipse", "Operation Sentinel",
        "Code Red", "Nightfall Protocol", "Silent Hawk", "Iron Shield", "Thunderbolt"
    ]

    code_names = [
        "Falcon", "Ghost", "Raven", "Viper", "Cobra",
        "Hawk", "Scorpion", "Wolf", "Eagle", "Panther"
    ]

    # create fake obj
    fake = Faker()

    # Dates and times in military format for natural feel
    def random_military_date():
        return fake.date_between(start_date='-2y', end_date='today').strftime("%d %b %Y")

    def random_military_time():
        return f"{randint(0,23):02d}{randint(0,59):02d}Z"

    # base templates
    base_templates = {
        0: [  # Unclassified (U)
            "Training updates were issued to {location} on {date}.",
            "Weather conditions remain stable across {location}.",
            "Routine system diagnostics report all {asset} operational.",
            "Daily briefing completed at {time} for {location}.",
            "Logistics prepared for upcoming exercises near {location}."
        ],
        1: [  # Confidential (C)
            "Misconfiguration detected in {asset} linked to {operation}.",
            "Confidential logistics data shared with command at {location}.",
            "Internal audit flagged clearance discrepancies in {asset} units.",
            "Personnel roster updated for {location} under {operation}.",
            "Security protocols reviewed during {operation} briefing."
        ],
        2: [  # Secret (S)
            "Signal intercepts suggest enemy triangulation near {location}.",
            "Mission reports flagged by intelligence under {operation}.",
            "Blackout protocols initiated for movement of {asset}.",
            "Surveillance assets deployed near {location} at {time}.",
            "Code name {code} assigned to reconnaissance team."
        ],
        3: [  # Top Secret (TS)
            "Satellite uplinks from {location} deep surveillance activated.",
            "Operation {operation} remains Tier-4 encrypted.",
            "Top Secret {asset} relocated during last cycle on {date}.",
            "Classified briefing for {operation} held at {time}.",
            "Agent {code} tasked with securing intel at {location}."
        ]
    }

    # Military-appropriate phrase endings ("noise") that fit the tone
    noise_phrases = [
        "Details remain under review by HQ.",
        "Additional instructions will follow.",
        "No anomalies reported at this time.",
        "Tracking systems will remain active.",
        "This message will self-delete in 24 hours.",
        "Further orders expected by 0600Z.",
        "Maintain radio silence until cleared.",
        "All personnel advised to remain alert.",
        "Encryption keys updated per protocol.",
        "Recon teams report no hostile activity."
    ]


    def generate_paragraph(label, min_sentences=2, max_sentences=5):
        prefix = [k for k, v in security_prefixes.items() if v == label][0]
        num_sentences = randint(min_sentences, max_sentences)
        
        sentences = []
        for _ in range(num_sentences):
            base_template = choice(base_templates[label])
            base = base_template.format(
                location=choice(locations),
                asset=choice(assets),
                operation=choice(operations),
                code=choice(code_names),
                date=random_military_date(),
                time=random_military_time()
            )
            noise = choice(noise_phrases)
            sentence = f"{base} {noise}"
            sentences.append(sentence)
        
        # Join sentences with spaces, prefix only once at the start
        paragraph = f"{prefix} " + " ".join(sentences)
        return paragraph

    # specify number of samples
    num_samples = 50000
    labels = []
    texts = []

    # generate samles
    for _ in range(num_samples):

        # choose a random label
        label = randint(0,3)
        texts.append(generate_paragraph(label))
        labels.append(label)

    return labels, texts