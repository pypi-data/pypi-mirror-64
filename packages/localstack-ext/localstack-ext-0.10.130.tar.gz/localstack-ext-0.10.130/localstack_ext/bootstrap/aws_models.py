from localstack.utils.aws import aws_models
yGHNR=super
yGHNq=None
yGHNA=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  yGHNR(LambdaLayer,self).__init__(arn)
  self.cwd=yGHNq
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,yGHNA,env=yGHNq):
  yGHNR(RDSDatabase,self).__init__(yGHNA,env=env)
 def name(self):
  return self.yGHNA.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
