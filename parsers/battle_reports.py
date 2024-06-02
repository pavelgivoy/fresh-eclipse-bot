def parse_hq_report(text: str):
    reports = text.split('\n\n\n')
    reports[0] = '\n'.join(reports[0].split('\n')[1:])

    parsed_hq_report = []

    for report in reports:
        parsed_info: dict[str, str | int | None] = {
            'name': None,
            'result': None,
            'stock': 0,
            'glory': 0,
        }
        report_lines = report.split('\n')
        parsed_info['name'] = report_lines[0].split(' was ')[0].strip()
        parsed_info['result'] = report_lines[0].split(' was ')[1].strip()[:-1]
        if parsed_info['result'] == 'easily defended' and '🎖Attack:' not in report_lines[1]:
            parsed_info['result'] = 'too easily defended'
        if 'Attackers' in report_lines[1]:
            parsed_info['stock'] = report_lines[1].split()[-3].split('📦')[0]
            if parsed_info['stock'] == '':
                parsed_info['stock'] = 0
            else:
                parsed_info['stock'] = int(parsed_info['stock'])
            parsed_info['glory'] = report_lines[1].split()[-1].split('🎖')[0]
            if parsed_info['glory'] == '':
                parsed_info['glory'] = 0
            else:
                parsed_info['glory'] = int(parsed_info['glory'])

        parsed_hq_report.append(parsed_info)

    return parsed_hq_report


def parse_map_report(text: str):
    reports = text.split('\n\n')
    reports[0] = '\n'.join(reports[0].split('\n')[1:])

    parsed_map_report = []

    for report in reports:
        parsed_info: dict[str, str | None] = {
            'name': None,
            'result': None,
            'new_owner': None,
        }
        report_lines = report.split('\n')
        delimeter = ' was ' if ' was ' in report_lines[0] else ' belongs to '
        parsed_info['name'] = report_lines[0].split(delimeter)[0].strip()
        after_delimeter = report_lines[0].split(delimeter)[-1].strip()
        if delimeter == ' belongs to ' and '.' in after_delimeter:
            parsed_info['new_owner'], parsed_info['result'] = after_delimeter.split(
                '.')
            parsed_info['result'] = parsed_info['result'].strip(' :')
        elif delimeter == ' belongs to ' and ':' in after_delimeter:
            new_owner = after_delimeter.strip(':')
            if new_owner == '':
                new_owner = 'Неизвестные силы'
            parsed_info['new_owner'] = new_owner
            parsed_info['result'] = 'Captured'
        else:  # here only ' was ' delimeter
            defenders_str_index = 2 if '🎖Attack:' in report else 1
            defenders = report_lines[defenders_str_index]
            if 'Forbidden' in defenders and '[' not in defenders and ']' not in defenders:
                parsed_info['new_owner'] = 'Запретные силы'
            parsed_info['result'] = after_delimeter
            if after_delimeter == 'easily protected' and defenders_str_index == 1:
                parsed_info['result'] = 'too easily protected'

        parsed_map_report.append(parsed_info)

    return parsed_map_report
