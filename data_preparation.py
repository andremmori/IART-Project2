import numpy
from lxml import etree as et


def cleanup(matches):
    try:
        del matches["possession"]
        del matches["corner"]
        del matches["card"]
        del matches["foul"]
        del matches["shoton"]
        del matches["shotoff"]
    except KeyError:
        print("Already deleted")


def extract_possession(matches):
    possession = et.Element("possession")
    for id, row in zip(matches['id'], matches['possession']):
        # print(et.tostring(row, pretty_print=True).decode())
        if len(row.getchildren()):
            match = et.SubElement(possession, 'match')
            match.set('id', str(id))
            for child in row[-1].getchildren():
                el = et.fromstring(et.tostring(child))
                match.append(el)
    file = open('possession.xml', 'w+')
    file.write(et.tostring(possession, pretty_print=True).decode())
    idx = 0
    for _, element in et.iterparse("possession.xml", tag='match'):
        matches.at[idx, "HP"] = element.findtext('homepos')
        matches.at[idx, "AP"] = element.findtext('awaypos')

        idx += 1
        element.clear(keep_tail=True)


def extract_cards(matches):
    card = et.Element("card")

    for id, row in zip(matches['id'], matches['card']):
        if len(row.getchildren()):
            match = et.SubElement(card, 'match')
            match.set('id', str(id))
            for child in row.getchildren():
                el = et.fromstring(et.tostring(child))
                match.append(el)

    file = open('card.xml', 'w+')
    file.write(et.tostring(card, pretty_print=True).decode())

    matches['HY'] = 0
    matches['AY'] = 0
    matches['HR'] = 0
    matches['AR'] = 0
    for _, element in et.iterparse("card.xml", tag='match'):
        id = element.get('id')
        idx = matches[matches['id'] == numpy.int64(id)].index.values.astype(int)[0]

        for child in element:
            if child.findtext('team') == str(matches.at[idx, 'home_team_id']):
                if child.findtext('card_type') == 'y':
                    matches.at[idx, 'HY'] += 1
                else:
                    matches.at[idx, 'HR'] += 1

            elif child.findtext('team') == str(matches.at[idx, 'away_team_id']):
                if child.findtext('card_type') == 'y':
                    matches.at[idx, 'AY'] += 1
                else:
                    matches.at[idx, 'AR'] += 1

        element.clear(keep_tail=True)


def prepare_dataframe(matches):
    # Get XML data from the dataframe
    matches['possession'] = matches['possession'].apply(lambda x: et.fromstring(x))
    matches['card'] = matches['card'].apply(lambda x: et.fromstring(x))
    matches['foul'] = matches['foul'].apply(lambda x: et.fromstring(x))
    matches['corner'] = matches['corner'].apply(lambda x: et.fromstring(x))
    matches['shoton'] = matches['shoton'].apply(lambda x: et.fromstring(x))
    matches['shotoff'] = matches['shotoff'].apply(lambda x: et.fromstring(x))


def extract_fouls(matches):
    foul = et.Element("foul")

    for id, row in zip(matches['id'], matches['foul']):
        if len(row.getchildren()):
            match = et.SubElement(foul, 'match')
            match.set('id', str(id))
            for child in row.getchildren():
                el = et.fromstring(et.tostring(child))
                match.append(el)

    file = open('foul.xml', 'w+')
    file.write(et.tostring(foul, pretty_print=True).decode())

    matches['HF'] = 0
    matches['AF'] = 0
    for _, element in et.iterparse("foul.xml", tag='match'):
        id = element.get('id')
        idx = matches[matches['id'] == numpy.int64(id)].index.values.astype(int)[0]

        for child in element:
            if child.findtext('team') == str(matches.at[idx, 'home_team_id']):
                matches.at[idx, 'HF'] += 1

            elif child.findtext('team') == str(matches.at[idx, 'away_team_id']):
                matches.at[idx, 'AF'] += 1

        element.clear(keep_tail=True)


def extract_corners(matches):
    corner = et.Element("corner")

    for id, row in zip(matches['id'], matches['corner']):
        if len(row.getchildren()):
            match = et.SubElement(corner, 'match')
            match.set('id', str(id))
            for child in row.getchildren():
                el = et.fromstring(et.tostring(child))
                match.append(el)

    file = open('corner.xml', 'w+')
    file.write(et.tostring(corner, pretty_print=True).decode())

    matches['HC'] = 0
    matches['AC'] = 0
    for _, element in et.iterparse("corner.xml", tag='match'):
        id = element.get('id')
        idx = matches[matches['id'] == numpy.int64(id)].index.values.astype(int)[0]

        for child in element:
            if child.findtext('team') == str(matches.at[idx, 'home_team_id']):
                matches.at[idx, 'HC'] += 1
            elif child.findtext('team') == str(matches.at[idx, 'away_team_id']):
                matches.at[idx, 'AC'] += 1

        element.clear(keep_tail=True)


def extract_shoton(matches):
    shoton = et.Element("shoton")

    for id, row in zip(matches['id'], matches['shoton']):
        if len(row.getchildren()):
            match = et.SubElement(shoton, 'match')
            match.set('id', str(id))
            for child in row.getchildren():
                el = et.fromstring(et.tostring(child))
                match.append(el)

    file = open('shoton.xml', 'w+')
    file.write(et.tostring(shoton, pretty_print=True).decode())

    matches['HST'] = 0
    matches['AST'] = 0
    for _, element in et.iterparse("shoton.xml", tag='match'):
        id = element.get('id')
        idx = matches[matches['id'] == numpy.int64(id)].index.values.astype(int)[0]

        for child in element:
            if child.findtext('team') == str(matches.at[idx, 'home_team_id']):
                matches.at[idx, 'HST'] += 1
            elif child.findtext('team') == str(matches.at[idx, 'away_team_id']):
                matches.at[idx, 'AST'] += 1

        element.clear(keep_tail=True)


def extract_shotoff(matches):
    shotoff = et.Element("shotoff")

    for id, row in zip(matches['id'], matches['shotoff']):
        if len(row.getchildren()):
            match = et.SubElement(shotoff, 'match')
            match.set('id', str(id))
            for child in row.getchildren():
                el = et.fromstring(et.tostring(child))
                match.append(el)

    file = open('shotoff.xml', 'w+')
    file.write(et.tostring(shotoff, pretty_print=True).decode())

    matches['HS'] = 0
    matches['AS'] = 0
    for _, element in et.iterparse("shotoff.xml", tag='match'):
        id = element.get('id')
        idx = matches[matches['id'] == numpy.int64(id)].index.values.astype(int)[0]
        matches.at[idx, 'HS'] = matches.at[idx, 'HST']
        matches.at[idx, 'AS'] = matches.at[idx, 'AST']

        for child in element:
            if child.findtext('team') == str(matches.at[idx, 'home_team_id']):
                matches.at[idx, 'HS'] += 1
            elif child.findtext('team') == str(matches.at[idx, 'away_team_id']):
                matches.at[idx, 'AS'] += 1

        element.clear(keep_tail=True)
