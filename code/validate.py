#!/usr/bin/env python

# TODO: notify if schema is not valid (validation can be done in a pre-push git hook)
# TODO: reports on errors
# TODO: look at the schema validation of json files (or transform them into CSV before sending them into repo)

import goodtables
from termcolor import colored

class Validate():

    def init(self):
        self.valid = False

    def run(self):
        report = goodtables.validate('datapackage.json', preset='datapackage')
        # TODO: Notify on errors.
        # TODO: save fancy reports to $CIRCLE_ARTIFACTS

        with open('reports/validations.txt', 'w') as file:
            self.valid = True
            for t in report['tables']:
                file.write('File %s' % t['source'])
                if t['valid']:
                    file.write(colored('\t VALID\n', 'green'))
                else:
                    self.valid = False
                    for error in t['errors']:
                        file.write(colored('\t%s\n'%error['message'], 'red'))

        # TODO: if no errors then complete task
        # TODO: Fail CircleCI when not valid.
        return self.valid

if __name__ == '__main__':
    Validate().run()