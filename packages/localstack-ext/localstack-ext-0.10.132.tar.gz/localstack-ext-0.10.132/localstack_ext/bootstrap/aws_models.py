from localstack.utils.aws import aws_models
RoEDx=super
RoEDa=None
RoEDB=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  RoEDx(LambdaLayer,self).__init__(arn)
  self.cwd=RoEDa
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,RoEDB,env=RoEDa):
  RoEDx(RDSDatabase,self).__init__(RoEDB,env=env)
 def name(self):
  return self.RoEDB.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
