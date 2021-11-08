#According to the branch name, the commit message prefix is automatically added to associate issue and commit.
#
#Branch name | commit format
# --- | ---
# issue-1234  | #1234, message
# issue-1234-fix-bug  | #1234, message

import sys, os, re
from subprocess import check_output
from typing import Optional
from typing import Sequence

def main(argv: Optional[Sequence[str]] = None) -> int:
    commit_msg_filepath = sys.argv[1]

    #Detect our branch
    branch = check_output(['git', 'symbolic-ref', '--short', 'HEAD']).strip().decode('utf-8')
    #Matching, such as issue-123, issue-1234 fix
    result = re.match('^BTCWT-(\d+)((-.*)+)?$', branch)
    if not result:
        #Branch name does not match
        warning = "WARN: Unable to add issue prefix since the format of the branch name dismatch."
        warning += "\nThe branch should look like issue-<number> or issue-<number>-<other>, for example: issue-100012 or issue-10012-fix-bug)"
        print(warning)
        return
    issue_number = result.group(1)
    with open(commit_msg_filepath, 'r+') as f:
        content = f.read()
        if re.search('^#[0-9]+(.*)', content):
            # print('There is already issue prefix in commit message.')
            return
        issue_prefix = '#' + issue_number
        f.seek(0, 0)
        f.write("%s, %s" % (issue_prefix, content))
        # print('Add issue prefix %s to commit message.' % issue_prefix)

if __name__ == '__main__':
    exit(main())
