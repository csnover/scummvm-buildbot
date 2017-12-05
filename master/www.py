from buildbot.www.oauth2 import GitHubAuth
from buildbot.www.authz import Authz
from buildbot.www.auth import UserPasswordAuth
from buildbot.www.authz.roles import RolesFromGroups, RolesFromUsername
from buildbot.www.authz.endpointmatchers import AnyControlEndpointMatcher

def make_www(port, auth_role, secrets, is_dev_env):
    if is_dev_env:
        auth = UserPasswordAuth({"user": "pass"})
        role_matcher = RolesFromUsername(roles=[auth_role], usernames=["user"])
    else:
        auth = GitHubAuth(clientId=secrets["github_client_id"],
                          clientSecret=secrets["github_client_secret"])
        role_matcher = RolesFromGroups()

    return {
        "auth": auth,
        "authz": Authz(
            allowRules=[AnyControlEndpointMatcher(role=auth_role)],
            roleMatchers=[role_matcher]
        ),
        "change_hook_dialects": {
            "github": {
                "secret": secrets["github_hook_secret"],
                "strict": True
            }
        },
        "logfileName": None,
        "plugins": {
            "console_view": True,
            "grid_view": True,
            "waterfall_view": True
        },
        "port": port
    }
