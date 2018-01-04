import subprocess
import datetime
import shutil
import os
import fileinput
import glob
# from code_contribution_reporter.blameit import debug_info


debug = True


def debug_info(str_info):
    if debug is True:
        print(str_info)
    return


# parameters
project_dir = os.path.dirname(os.path.realpath(__file__))
piechart_template_file = project_dir + '/templates/piechart_template.html'
piechart_text_to_search_1 = 'TO_BE_REPLACED_DATEPOINTS'
piechart_text_to_search_2 = 'TO_BE_REPLACED_TITLE'


def generate_pie_chart(git_name, git_dir, since_when, before_when):
    # git_dir = 'D:/eBond/center/.git'
    # git_name = 'center'
    today = datetime.date.today()
    debug_info(today)
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
        debug_info(all_count)
    allDict_percent = {}
    for key, value in allDict_count.items():
        allDict_percent[key] = round(value / all_count * 100, 2)
    # { y: 51.08, label: "Chrome" },
    debug_info(allDict_percent)
    textToReplace_1 = ''
    textToReplace_2 = 'ALL commits counts for project ' + git_name + ' since ' + since_when
    for key, value in allDict_percent.items():
        debug_info('{ y: ' + str(value) + ', label: "' + key + '" },')
        textToReplace_1 += '{ y: ' + str(value) + ', label: "' + key + '/' + str(allDict_count[key]) + '" },'
    report_file = project_dir + '/reports/' + git_name + '-' \
        + since_when.replace(' ', '-') + '-piechart-' + str(today) + '.html'
    shutil.copy2(piechart_template_file, report_file)
    with fileinput.FileInput(report_file, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(piechart_text_to_search_1, textToReplace_1), end='')
    # need to improve this...
    with fileinput.FileInput(report_file, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(piechart_text_to_search_2, textToReplace_2), end='')
    if os.path.isfile(report_file + '.bak'):
        os.remove(report_file + '.bak')


