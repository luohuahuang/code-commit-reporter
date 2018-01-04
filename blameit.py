import os
import subprocess
import shutil
import datetime
import glob
import fileinput

from code_contribution_reporter.linechartgen import generate_line_chart
from code_contribution_reporter.piechartgen import generate_pie_chart

debug = True


def debug_info(str_info):
    if debug is True:
        print(str_info)
    return


project_dir = os.path.dirname(os.path.realpath(__file__))
files = glob.glob(project_dir + '/reports/*.html')
for f in files:
    os.remove(f)

file = open(project_dir + '/config.txt', 'r')
allproject = {}
for line in file:
    if (line.startswith('#') is False) and (line.startswith('project.git')):
        s_git = line.split('=')[1].strip()
        s = s_git.split('/')[-1]
        prj_name = s.split('.')[0]
        allproject[prj_name] = prj_name + '/.git'
        # debug_info('xxx' + prj_name + 'xxx')
        shutil.rmtree(project_dir + '/' + prj_name, ignore_errors= FileNotFoundError)
        subprocess.run(['git', 'clone', s_git],
                       stdout=subprocess.PIPE).stdout.decode('utf-8')

today = datetime.date.today()
debug_info(today)

for key, value in allproject.items():
    debug_info('Generating report for project ' + key)
    generate_line_chart(key, value, '2016-10-01', str(today))
# parser.generatePieChart('center', 'D:/eBond/center/.git', '1200')
    generate_pie_chart(key, value, "120 months ago", '2099-01-01')
    generate_pie_chart(key, value, "12 months ago", '2099-01-01')
    generate_pie_chart(key, value, "6 months ago", '2099-01-01')
    generate_pie_chart(key, value, "3 months ago", '2099-01-01')
    generate_pie_chart(key, value, "1 month ago", '2099-01-01')

all_reports_files = os.listdir(project_dir + '/reports')

index_template_file = project_dir + '/templates/index.html'
index_file = project_dir + '/reports/index.html'
shutil.copy2(index_template_file, index_file)

to_be_inserted = ''
for name in all_reports_files:
    # <a href="abc.index">center</a><br>
    if '.js' in name:
        continue
    to_be_inserted = to_be_inserted + '<a href="' + name + '">' + name.split('.')[0] + '</a><br>'

with fileinput.FileInput(index_file, inplace=True) as file:
    for line in file:
        print(line.replace('TO_BE_REPLACED', to_be_inserted), end='')

