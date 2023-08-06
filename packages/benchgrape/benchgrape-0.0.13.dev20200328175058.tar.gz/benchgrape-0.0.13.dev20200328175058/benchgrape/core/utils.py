
DEFAULT_TOKEN_LOCATION = './benchmark_tokens.json'


def map_benchmark_data(raw_data):
    """"
    map benchmark data do internal format -> currently just a proxy where
    we could interfere
    :param raw_data: ``dict``
    :return: ``dict``
    """
    organization = raw_data['organization']
    organization['url'] = raw_data['url']

    users = []
    for id, user_data in raw_data['users'].items():
        meta = user_data
        meta['id'] = id
        users.append(meta)

    groups = []
    for id, group_data in raw_data['groups'].items():
        meta = group_data
        meta['id'] = id
        groups.append(meta)

    pcs = []
    for id, pc_data in raw_data['private_conversations'].items():
        meta = pc_data
        meta['id'] = id
        pcs.append(meta)

    return organization, users, groups, pcs
