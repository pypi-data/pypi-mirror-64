from localstack.utils.aws import aws_models
IAjFK=super
IAjFk=None
IAjFl=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  IAjFK(LambdaLayer,self).__init__(arn)
  self.cwd=IAjFk
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,IAjFl,env=IAjFk):
  IAjFK(RDSDatabase,self).__init__(IAjFl,env=env)
 def name(self):
  return self.IAjFl.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
