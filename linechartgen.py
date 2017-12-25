import subprocess
import datetime
import shutil
import os
import fileinput
import glob

# parameters
project_dir = os.path.dirname(os.path.realpath(__file__))
linechart_template_file = project_dir + '/templates/linechart_template.html'
linechart_text_to_search_1 = 'TO_BE_REPLACED_DATEPOINTS'
linechart_text_to_search_2 = 'TO_BE_REPLACED_TITLE'

# ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthsDict = {'1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr',
              '5': 'May', '6': 'Jun', '7': 'Jul', '8': 'Aug',
              '9': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}

files = glob.glob(project_dir + '/reports/*linechart*.html')
for f in files:
    os.remove(f)

debug = True


def debug_info(str_info):
    if debug is True:
        print(str_info)
    return


def generate_line_chart(git_name, git_dir, since_when, before_when):
    # git_dir = 'D:/eBond/center/.git'
    # git_name = 'center'
    today = datetime.date.today()

    orig_year = before_when.split('-')[0]
    orig_month = before_when.split('-')[1]
    if orig_month.startswith('0'):
        orig_month = orig_month.replace('0', '', 1)

    # run - all stats.
    # it will return a summary for the whole project:
    #    e.g,
    #    255  gaojun
    #    46  THINK
    # command_commits = 'git --git-dir=' + git_dir + '--since="MONTHS months ago" ' + 'shortlog -sn'
    output_all = subprocess.run(['git', '--git-dir=' + git_dir, 'shortlog',
                                 '--since="' + since_when + '"', '--before="' + before_when + '"', '-sn'],
                                stdout=subprocess.PIPE).stdout.decode('utf-8')
    allStats = output_all.split("  ")
    allDict_count = {}
    all_count = 0
    for stat in allStats:
        if not stat or stat == '':
            continue
        s = stat.strip().split()
        allDict_count[s[1]] = int(s[0])
        all_count += int(s[0])
        # debuginfo(all_count)

    textToReplace_1 = ''
    textToReplace_2 = ''
    count = 11
    while count >= 0:
        if (int(orig_month) - count) < 0:
            textToReplace_2 = textToReplace_2 + '\'' + monthsDict[str(int(orig_month) - count + 12)]  + '\'' + ','
        elif (int(orig_month) - count) == 0:
            textToReplace_2 = textToReplace_2 + '\'' + monthsDict[str(int(orig_month) + 1)] + '\'' + ','
        else:
            textToReplace_2 = textToReplace_2 + '\'' + monthsDict[str(int(orig_month) - count)] + '\'' + ','
        count -= 1

    for key, value in allDict_count.items():
        debug_info('Generating report for author ' + key)
        s_output = '{name: \'' + key + '\', data: ['
        count = 11
        while count >= 0:
            if (int(orig_month) - count) < 0:
                since_when = str(int(orig_year) - 1) + '-' + str(int(orig_month) - count + 12) + '-' + '01'
                before_when = str(int(orig_year) - 1) + '-' + str(int(orig_month) - count + 12) + '-' + '31'
                debug_info('since_when: ' + since_when + ' # ' + 'before_when: ' + before_when)
                # textToReplace_2 = textToReplace_2 + monthsDict[str(int(orig_month) - count + 12)] + ','
            elif (int(orig_month) - count) == 0:
                since_when = str(int(orig_year) - 1) + '-' + str(int(orig_month) + 1) + '-' + '01'
                before_when = str(int(orig_year) - 1) + '-' + str(int(orig_month) + 1)  + '-' + '31'
                debug_info('since_when: ' + since_when + ' # ' + 'before_when: ' + before_when)
            else:
                since_when = orig_year + '-' + str(int(orig_month) - count) + '-' + '01'
                before_when = orig_year + '-' + str(int(orig_month) - count) + '-' + '31'
                debug_info('since_when: ' + since_when + ' # ' + 'before_when: ' + before_when)
                # textToReplace_2 = textToReplace_2 + monthsDict[str(int(orig_month) - count)] + ','
            output_all = subprocess.run(['git', '--git-dir=' + git_dir, 'shortlog', '--author=' + key,
                                         '--since="' + since_when + '"', '--before="' + before_when + '"', '-sn'],
                                        stdout=subprocess.PIPE).stdout.decode('utf-8')
            allStats = output_all.split()
            if not allStats or allStats == '':
                s_output = s_output + '0, '
            for stat in allStats:
                s = stat.strip().split(' ')
                s_output = s_output + s[0] + ', '
                break
            count -= 1
        s_output = s_output + ']}'
        textToReplace_1 = textToReplace_1 + s_output + ','
    debug_info(textToReplace_1)
    debug_info(textToReplace_2)
    report_file = project_dir + '/reports/' + git_name + '-linechart-' + str(today) + '.html'
    shutil.copy2(linechart_template_file, report_file)
    with fileinput.FileInput(report_file, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(linechart_text_to_search_1, textToReplace_1), end='')
    # need to improve this...
    with fileinput.FileInput(report_file, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(linechart_text_to_search_2, textToReplace_2), end='')
    if os.path.isfile(report_file + '.bak'):
        os.remove(report_file + '.bak')


file = open(project_dir + '/config.txt', 'r')
allproject = {}
for line in file:
    if (line.startswith('#') is False) and (line.startswith('project.git')):
        s = line.split('=')[1].strip().split('#')
        allproject[s[0]] = s[1]
today = datetime.date.today()
debug_info(today)
for key, value in allproject.items():
    debug_info('Generating report for project ' + key)
    generate_line_chart(key, value, '2016-10-01', str(today))


'''
{
        name: 'liukai',
        data: [7.0, 6.9, 9.5, 14.5, 18.4, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
    },
'''
