from catapult_docs_cli.utils import clean_dicts, merge_dicts, clean_line, indent
from .base import Command, Table, Title, Paragraph, Parser


class PropertiesCommand(Command):
    """Command to parse config files from catapult-server (/resources/*.properties) into RST text.

    The command searches in the code the description for each property.
    """

    def execute(self):
        """Contains all the logic to execute a command."""
        for c in self.config['properties']:
            print(Title(c['title']).to_string())
            if c['text']:
                print(Paragraph(c['text']).to_string())
            print(PropertiesTable(
                PropertiesParser(c['source'], c['descriptions'], self.config['serverPath']).parse()).to_string() + '\n')


class PropertiesTable(Table):
    """Class to format a set of properties into RST.

    Each row contains:
        - The property name.
        - The property type.
        - The property description.
        - The property default value.
    """

    def __init__(self, rows):
        super().__init__(['Property', 'Type', 'Description', 'Default'], rows)

    def _format_rows(self):
        """Formats the table rows as a str.

        Returns:
            str: The rows formatted as a str.
        """
        result = ''
        for row in self.rows:
            key = row['key']
            classification = '' if 'type' not in row else row['type']
            description = '' if 'description' not in row else row['description']
            default = '' if 'default' not in row else row['default']
            result += '\n' + indent(key + "; " + classification + "; " + description + "; " + default, 4)
        return result


class PropertiesParser(Parser):
    """Class to parse Catapult properties from catapult-server code

    Parsers looks for the properties list in one main file (.properties),
    and looks for the descriptions in a set of files (*Configuration.h).

    Args:
        source_file (str): Relative path of the source file with the properties list (.properties).
        description_files (:obj:`list` of str): Relative paths of the files with the descriptions (*Configuration.h).
        server_path (str): Absolute path where catapult-server is located.
    """

    def __init__(self, source_file, description_files, server_path):
        super().__init__(server_path + source_file, list(map(lambda file: server_path + file, description_files)))

    def _parse_source_file(self):
        """Parses the source file.

        Picks the name and default value of each property.

        Returns:
            rows (:obj:`list` of str): The properties formatted as rows.
        """
        try:
            with open(self.source_file, encoding='utf-8') as file:
                lines = file.readlines()
                rows = []
                for line in lines:
                    # remove line break
                    line = line.replace('\n', '')
                    # format section
                    if '[' in line:
                        rows.append({'key': "**" + line.replace('[', '').replace(']', '') + '**'})
                    # format regular property
                    elif line != '' and '#' not in line:
                        line_array = line.split('=')
                        # get key
                        key = line_array[0].replace(' ', '')
                        # if key already exists, make it unique
                        while any(key in x for x in rows):
                            key += "!"
                        # get default value
                        default = line_array[1].lstrip()
                        rows.append({'key': key, 'default': default})
                return rows
        except IOError:
            print('Operation failed: %s does not exist' % self.source_file)

    def _parse_description_files(self):
        """Parses the source file.

        Picks the name and description of each property.

        Returns:
            rows (:obj:`list` of str): The properties formatted as rows.
        """
        rows = []
        for path in self.description_files:
            try:
                with open(path, encoding='utf-8') as file:
                    # buffers to store last two lines processed
                    buffer1 = ''
                    buffer2 = ''
                    lines = file.readlines()
                    for line in lines:
                        line = clean_line(line)
                        # detect line to process
                        if ("///" in buffer1) and (";" in line) and ("(" not in line):
                            line_split = line.split(' ')
                            # get key
                            key = line_split[len(line_split) - 1].replace(';', '').replace(' ', '')
                            key = key[0].lower() + key[1:]
                            while any(key in x for x in rows):
                                key += "!"
                            # get type
                            classification = ' '.join(line_split[:len(line_split) - 1]).lstrip()
                            # get description
                            description = ''
                            if "///" in buffer2:
                                description = buffer2.split('///')[1].lstrip() + " "
                            description += buffer1.split('///')[1].lstrip()
                            # if key already exists, make it unique
                            rows.append({'key': key, 'type': classification, 'description': description})
                        buffer2 = buffer1
                        buffer1 = line
            except IOError:
                print('Operation failed: %s does not exist' % path)
        return rows

    def parse(self):
        """Merges source and description parsers.

        Returns:
            rows (:obj:`list` of str): The properties formatted as rows.
        """
        return clean_dicts(merge_dicts(self._parse_source_file(), self._parse_description_files()))
