import os
import sys
from FinalStateAnalysis.PatTools.datadefs import datadefs

cfg = 'analyze_cfg.py'
jobId = '2011-11-23-v1-TauTNP'

patJobId = '2011-11-08-EWKPatTuple'
patCfg = 'patTuple_cfg'

def get_dir(sample):
    dir_name = '-'.join([patJobId, sample, patCfg])
    base_dir = '--input-dir=root://cmsxrootd.hep.wisc.edu//store/user/efriis/'
    return base_dir + dir_name

for sample, sample_info in sorted(datadefs.iteritems(), key=lambda (x,y): x):
    if 'Tau' not in sample_info['analyses']:
        continue
    if '2011B' in sample:
        continue

    path_name = os.path.join(os.environ['scratch'], '-'.join(
        [jobId, sample, 'analyzeFinalStates']))
    sys.stderr.write('Building sample submit dir %s\n' % (sample))
    if os.path.exists(path_name):
        sys.stderr.write('Skipping existing submit directory for %s\n' % sample)
        continue

    options = []
    farmout_options = []
    farmout_options.append(get_dir(sample))

    command = [
        'farmoutAnalysisJobs2',
        '--varparsing',
        '--fwklite',
        #'--no-submit',
        #'--job-count=20',
        #'--input-files-per-job=%i' % (sample_info['ana_group']*2),
        ' --exclude-input-files="*plots.root"',
        '--input-files-per-job=%i' % 3,
    ]

    #if 'WplusJets' in sample:
        #command.append('--job-count=10')

    command.extend(farmout_options)

    command.append('-'.join([jobId, sample]))
    command.append(os.path.join(
        os.environ['CMSSW_BASE'], 'bin',
        os.environ['SCRAM_ARCH'], 'analyzeFinalStates'))
    command.append(os.path.abspath(cfg))
    command.extend(options)
    print ' '.join(command)