from buildbot.plugins import schedulers, util
AnyBranchScheduler = schedulers.AnyBranchScheduler
ForceScheduler = schedulers.ForceScheduler
ChangeFilter = util.ChangeFilter
ChoiceStringParameter = util.ChoiceStringParameter
CodebaseParameter = util.CodebaseParameter
NestedParameter = util.NestedParameter
StringParameter = util.StringParameter

def file_is_important(change):
    # TODO: Ignore changes to non-source-code, non-make, non-engine-config files
    return True

def make_schedulers(builder_names, project_id, repository_id):
    force_reason = StringParameter(name="reason", label="Message:", required=True, size=60)
    force_codebase = CodebaseParameter(label="Repository",
                                       codebase="",
                                       branch=StringParameter(name="branch",
                                                              label="Branch or tag:",
                                                              default="master",
                                                              strict=False,
                                                              required=True),
                                       revision=None,
                                       repository=repository_id,
                                       project=project_id)
    force_properties = [
        NestedParameter(name="",
                        label="Options",
                        layout="vertical",
                        fields=[
                            StringParameter(name="force_extra_configure_args",
                                            label="Extra configure arguments:",
                                            required=False,
                                            size=60)
                        ])
    ]

    return [
        AnyBranchScheduler(name=project_id,
                           change_filter=ChangeFilter(project=project_id),
                           treeStableTimer=5,
                           fileIsImportant=file_is_important,
                           builderNames=builder_names),
        ForceScheduler(name="manual",
                       label="Manual build",
                       buttonName="Run manual build",
                       builderNames=builder_names,
                       reason=force_reason,
                       codebases=[force_codebase],
                       properties=force_properties)
    ]
