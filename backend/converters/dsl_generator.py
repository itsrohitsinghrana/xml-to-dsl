def generate_dsl(job_type, job_config):
    """
    Generates Jenkins Job DSL with correct syntax for all job types.
    """
    dsl = ""

    # Freestyle Job
    if job_type == "freestyle":
        dsl = f"""
job('{job_config["job_name"]}') {{
    description('{job_config["description"]}')
    logRotator(-1, 10)
    scm {{
        git('{job_config["scm_url"]}')
    }}
    triggers {{
        scm('{job_config["triggers"]}')
    }}
    steps {{
        shell('echo Building {job_config["job_name"]}')
    }}
}}
"""

    # Pipeline Job
    elif job_type == "pipeline":
        dsl = f"""
pipelineJob('{job_config["job_name"]}') {{
    description('{job_config["description"]}')
    definition {{
        cps {{
            script('''pipeline {{
                agent any
                stages {{
                    stage('Build') {{
                        steps {{
                            echo 'Building {job_config["job_name"]}'
                        }}
                    }}
                }}
            }}''')  // Properly closed triple quotes
            sandbox()
        }}
    }}
}}
"""

    # Maven Job
    elif job_type == "maven":
        dsl = f"""
mavenJob('{job_config["job_name"]}') {{
    description('{job_config["description"]}')
    logRotator(-1, 10)
    scm {{
        git('{job_config["scm_url"]}')
    }}
    triggers {{
        scm('{job_config["triggers"]}')
    }}
    goals('{job_config["maven_goals"]}')
}}
"""

    # Matrix (Multi-Configuration) Job
    elif job_type == "matrix":
        dsl = f"""
matrixJob('{job_config["job_name"]}') {{
    description('{job_config["description"]}')
    logRotator(-1, 10)
    axes {{
        {''.join([f"label('{axis}'); " for axis in job_config["matrix_axes"]])}
    }}
    builders {{
        shell('echo Running Matrix Build for {job_config["job_name"]}')
    }}
}}
"""

    # Multibranch Pipeline Job
    elif job_type == "multibranch":
        dsl = f"""
multibranchPipelineJob('{job_config["job_name"]}') {{
    description('{job_config["description"]}')
    branchSources {{
        branchSource {{
            source {{
                bitbucket {{
                    id('{job_config["credentials_id"]}')
                    serverUrl('{job_config["scm_url"]}')
                    repoOwner('{job_config["repo_owner"]}')
                    repository('{job_config["repository"]}')
                    credentialsId('{job_config["credentials_id"]}')
                    traits {{
                        bitbucketBranchDiscovery {{
                            strategyId(3)  // Discover branches, PRs
                        }}
                        regexSCMHeadFilter {{
                            regex('(dev|staging|master|feature/.+|release/.+|preprod|production|integration|hotfix/.+)')
                        }}
                    }}
                }}
            }}
        }}
    }}
    
    factory {{
        workflowBranchProjectFactory {{
            scriptPath('{job_config["script_path"]}')
        }}
    }}
    
    orphanedItemStrategy {{
        discardOldItems {{
            daysToKeep(7)
            numToKeep(10)
        }}
    }}
}}
"""

    # ListView for All Jobs
    dsl += f"""
listView('All Jobs View') {{
    description('View for all jobs')
    recurse(false)
    jobs {{
        regex('.*')  // Includes all jobs
    }}
    columns {{
        status()
        weather()
        name()
        lastSuccess()
        lastFailure()
        lastDuration()
        buildButton()
    }}
}}
"""

    return dsl

