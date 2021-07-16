import os
import subprocess

def getExtension(file, IncludeDot=True):
    ret = os.path.splitext(file)[1]
    if not IncludeDot:
        ret = ret.lstrip('.')
    return ret

def getInputfileType(inputfile):
    ''' determin inputfile is json or yaml '''
    ext = getExtension(inputfile, IncludeDot=False)
    if ext.lower()=='yaml':
        return 'yaml'
    return 'json'

def getGitHash(gitdir, git, Verbose=False):
    ''' get hash from dir'''

    args = [git, '-C', gitdir, 'rev-parse', 'HEAD']
    if Verbose:
        print(args)
    hash = subprocess.check_output(args).decode('utf-8').strip()
    if len(hash) != 40:
        exit('hex digits of hash is not 40')
    return hash

def getGitBaseArgs(gitdir, git):
    return [git, '-C', gitdir]

def gitCallGetReturnValue(gitdir, git, args, Verbose=False):
    callargs = getGitBaseArgs(gitdir,git)
    callargs.extend(args)
    if Verbose:
        print(callargs)
    return subprocess.call(callargs)

def gitCallGetOutput(gitdir, git, args, Verbose=False):
    callargs = getGitBaseArgs(gitdir,git)
    callargs.extend(args)
    if Verbose:
        print(callargs)
    return subprocess.check_output(callargs).decode('utf-8')

def hasGitStagedChanges(gitdir, git, Verbose=False):
    ret = gitCallGetReturnValue(gitdir,git,[
        #'diff-index', '--quiet', '--cached', 'HEAD', '--',        
        'diff-files', '--quiet',
    ])
    if ret != 0 and ret != 1:
        exit('Ambiguous return code "{}" from git'.format(ret))
    return ret==1

def hasGitUntrackedAndUnignoredFiles(gitdir, git, Verbose=False):
    ret = gitCallGetOutput(gitdir,git,
        'ls-files --exclude-standard --others'.split(' ')
    )
    return not not ret

def isGitCommited(gitdir, git, Verbose=False):
    ''' check dir is committed (no untracking and stating) '''
    return hasGitStagedChanges(gitdir,git) or hasGitUntrackedAndUnignoredFiles(gitdir,git)