from tomlkit import loads, dumps, table, aot


def load_toml(filename):
    with open(filename, 'r') as f:
        return loads(f.read())


def save_toml(filename, toml):
    with open(filename, 'w') as f:
        f.write(dumps(toml))


def migrate(pipfile, pyproject_toml, dry_run):
    pipenv = load_toml(pipfile)
    pyproject = load_toml(pyproject_toml)

    if 'source' not in pyproject['tool']['poetry']:
        pyproject['tool']['poetry']['source'] = aot()
    migrate_source_repo(pipenv['source'], pyproject['tool']['poetry']['source'])
    migrate_dependencies(pipenv['packages'], pyproject['tool']['poetry']['dependencies'])
    migrate_dependencies(pipenv['dev-packages'], pyproject['tool']['poetry']['dev-dependencies'])

    if dry_run:
        print(dumps(pyproject))
    else:
        save_toml(pyproject_toml, pyproject)


def migrate_dependencies(src, dist):
    for name, ver in src.item():
        if name in dist:
            continue
        dist.add(name, ver)


def migrate_source_repo(src, dist):
    for s in src:
        if s['name'] == 'pypi':
            continue
        source = table()
        source.add('name', s['name'])
        source.add('url', s['url'])
        dist.append(source)
