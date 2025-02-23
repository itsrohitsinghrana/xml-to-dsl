
multibranchPipelineJob('gs_openadr') {
    description('')
    branchSources {
        branchSource {
            source {
                bitbucket {
                    id('c84d984e-57ee-4a62-b2b0-ce213b7881c5')
                    serverUrl('https://bitbucket.org/enphaseembedded/devopsautomation')
                    repoOwner('EnphaseEmbedded')
                    repository('gs_openadr')
                    credentialsId('c84d984e-57ee-4a62-b2b0-ce213b7881c5')
                    traits {
                        bitbucketBranchDiscovery {
                            strategyId(3)  // Discover branches, PRs
                        }
                        regexSCMHeadFilter {
                            regex('(dev|staging|master|feature/.+|release/.+|preprod|production|integration|hotfix/.+)')
                        }
                    }
                }
            }
        }
    }
    
    factory {
        workflowBranchProjectFactory {
            scriptPath('Jenkinsfile')
        }
    }
    
    orphanedItemStrategy {
        discardOldItems {
            daysToKeep(7)
            numToKeep(10)
        }
    }
}

listView('All Jobs View') {
    description('View for all jobs')
    recurse(false)
    jobs {
        regex('.*')  // Includes all jobs
    }
    columns {
        status()
        weather()
        name()
        lastSuccess()
        lastFailure()
        lastDuration()
        buildButton()
    }
}
