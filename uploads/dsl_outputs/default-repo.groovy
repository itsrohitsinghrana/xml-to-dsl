
mavenJob('default-repo') {
    description('')
    logRotator(-1, 10)
    scm {
        git('https://github.com/adamsdavis1976/mule-test.git')
    }
    triggers {
        scm('H/5 * * * *')
    }
    goals('clean verify -P ci')
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
