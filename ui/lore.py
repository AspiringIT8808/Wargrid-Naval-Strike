"""
FLEET CODEX CONTENT - flavor text for the ship compendium (ui/screens/codex.py).

Pure data: no game logic, no pygame calls. Real-world ship blurbs are kept
short on purpose - this is a field dossier, not a textbook.
"""

SHIP_LORE = {
    "Frigate": {
        "class_tag": "FRIGATE-CLASS ESCORT",
        "blurb": "Real frigates are fast, multi-role escorts built to screen "
                 "larger fleets and strike hard before the enemy can react.",
        "tip": "Save BARRAGE for when you already have a confirmed hit - four "
               "shots land best when you already know roughly where the rest "
               "of the hull is.",
    },
    "Destroyer": {
        "class_tag": "DESTROYER-CLASS",
        "blurb": "Destroyers were built for speed and maneuver - historically "
                 "hunting submarines and darting away from bigger guns rather "
                 "than trading blows.",
        "tip": "RELOCATE is a one-time escape. Hold it until this ship has "
               "actually taken a hit - don't waste it moving a healthy hull.",
    },
    "Carrier": {
        "class_tag": "CARRIER-CLASS",
        "blurb": "Carriers project power from a distance, launching aircraft "
                 "to scout and strike far beyond the reach of deck guns.",
        "tip": "Use RECON when you have no live target to chase - it turns a "
               "blind guess into two or three informed shots next turn.",
    },
    "Cruiser": {
        "class_tag": "CRUISER-CLASS",
        "blurb": "Cruisers balance firepower and range, often patrolling and "
                 "gathering intelligence independently of the main fleet.",
        "tip": "ROW SCAN pays off most on a row you haven't shot yet - don't "
               "spend it re-checking a row you've already half covered.",
    },
    "Submarine": {
        "class_tag": "SUBMARINE-CLASS",
        "blurb": "Submarines survive by staying hidden, slipping past a "
                 "hunting fleet rather than standing and trading fire.",
        "tip": "STEALTH still gives you a shot, so use it the instant this "
               "ship takes its first hit - don't wait for a second one.",
    },
}

MECHANIC_LORE = {
    "Bomb": {
        "class_tag": "HIDDEN ORDNANCE",
        "blurb": "A mine sown in open water before the battle - it punishes "
                 "an eager attacker instead of the fleet that hid it.",
        "tip": "Place it in open water your opponent has no reason to avoid, "
               "away from where your own ships are likely to be searched.",
    },
    "Repair": {
        "class_tag": "DAMAGE CONTROL",
        "blurb": "Field repair crews patch a wounded hull well enough to "
                 "keep fighting - the classic damage-control party.",
        "tip": "Repairing re-opens that cell to attack, so patch a ship "
               "that's safe for now, not one under active fire.",
    },
    "Shield": {
        "class_tag": "POINT DEFENSE",
        "blurb": "A defensive screen over a single compartment - it survives "
                 "one hit before that protection is gone for good.",
        "tip": "Shield your biggest, healthiest ship before it's ever hit - "
               "shielding a ship the enemy is already hunting is often too late.",
    },
}
