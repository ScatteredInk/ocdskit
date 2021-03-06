import json
from collections import OrderedDict

from .base import BaseCommand


class Command(BaseCommand):
    name = 'combine-release-packages'
    help = 'reads release packages from standard input, collects releases, and prints one release package'

    def handle(self):
        output = OrderedDict([('extensions', OrderedDict()), ('releases', [])])

        for line in self.buffer():
            package = json.loads(line, object_pairs_hook=OrderedDict)

            # Use sample metadata.
            output['uri'] = package['uri']
            output['publishedDate'] = package['publishedDate']
            output['publisher'] = package['publisher']

            if 'extensions' in package:
                # Python has no OrderedSet, so we use OrderedDict to keep extensions in order without duplication.
                output['extensions'].update(dict.fromkeys(package['extensions'], True))

            for field in ('license', 'publicationPolicy', 'version'):
                if field in package:
                    output[field] = package[field]

            output['releases'].extend(package['releases'])

        if output['extensions']:
            output['extensions'] = list(output['extensions'])
        else:
            del output['extensions']

        self.print(output)
