import xml.etree.ElementTree as ET

DEFAULT_CONFIG = {
    "job_name": "Unknown_Job",
    "description": "No description provided.",
    "script_path": "Jenkinsfile",
    "scm_url": "https://github.com/example/default-repo.git",
    "repo_owner": "default-owner",
    "repository": "default-repo",
    "credentials_id": "default-credentials",
    "triggers": "H/5 * * * *",
    "maven_goals": "clean install",
    "matrix_axes": ["os=linux", "os=windows"]
}

def parse_config_xml(xml_file):
    """
    Parses Jenkins config.xml and extracts job properties, ensuring the job name is set to the repository name.
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        job_type = None
        job_config = DEFAULT_CONFIG.copy()

        if root.tag == "flow-definition":
            job_type = "pipeline"
        elif root.tag == "project":
            job_type = "freestyle"
        elif root.tag == "maven2-moduleset":
            job_type = "maven"
        elif root.tag == "matrix-project":
            job_type = "matrix"
        elif root.tag == "org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject":
            job_type = "multibranch"

        if not job_type:
            return None, None

        # Extract Repository Name and Use as Job Name
        repo_name = root.findtext(".//repository") or "default-repo"
        job_config["job_name"] = repo_name

        job_config["description"] = root.findtext("description", job_config["description"])
        job_config["scm_url"] = root.findtext(".//hudson.plugins.git.UserRemoteConfig/url", job_config["scm_url"])
        job_config["triggers"] = root.findtext(".//triggers/hudson.triggers.SCMTrigger/spec", job_config["triggers"])

        if job_type == "pipeline":
            script_node = root.find("definition/script")
            job_config["script_path"] = script_node.text if script_node is not None else job_config["script_path"]

        if job_type == "maven":
            job_config["maven_goals"] = root.findtext("goals", job_config["maven_goals"])

        if job_type == "matrix":
            axes = root.findall(".//axes/hudson.matrix.LabelAxis")
            job_config["matrix_axes"] = [axis.findtext("name") + "=" + ",".join([v.text for v in axis.findall("values/string")]) for axis in axes] if axes else DEFAULT_CONFIG["matrix_axes"]

        if job_type == "multibranch":
            job_config["repo_owner"] = root.findtext(".//repoOwner", job_config["repo_owner"])
            job_config["repository"] = repo_name
            job_config["credentials_id"] = root.findtext(".//credentialsId", job_config["credentials_id"])

        return job_type, job_config

    except Exception as e:
        print(f"Error parsing config.xml: {e}")
        return None, None

