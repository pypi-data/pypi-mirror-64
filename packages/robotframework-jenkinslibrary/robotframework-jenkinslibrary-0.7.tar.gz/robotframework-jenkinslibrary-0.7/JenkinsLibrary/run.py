from jenkins_face import JenkinsFace
import json

protocol = 'https'
url = 'jenkins-batch-truemoney.cicd.mn1.ocp.ascendmoney-dev.internal'
username = 'panchorn.ler-edit-view'
password = '1163443a265e4b27cc69b8e55ed179af7e'

job_name = 'job/truemoney-batch-common/job/truemoney-batch-common-truemoney-poi-settlement-dev-run-pipeline'

jenkins = JenkinsFace()
jenkins.create_session_jenkins(protocol, url, username, password)

# GET JOB DETAUL
# job_detail = jenkins.get_jenkins_job(job_name)
# print(job_detail['nextBuildNumber'])

# BUILD JOB WITH PARAMS
# req = {
# 	"JavaOptions": "-XX:MaxMetaspaceSize=128m -Xss1m",
# 	"StartupArgs": "700000067 25/02/2020 16:00:00 26/02/2020 15:59:59"
# }
# job_trigger_response = jenkins.build_with_parameters(job_name, None)
# print(job_trigger_response)


# GET JOB BUILD
# job_detail = jenkins.get_job_build(job_name)
# print(job_detail['building'])

job_detail = jenkins.get_jenkins_job_build(job_name, build_number=56)
print(job_detail)
