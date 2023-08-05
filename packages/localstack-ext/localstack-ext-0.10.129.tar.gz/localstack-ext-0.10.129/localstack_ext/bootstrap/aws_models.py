from localstack.utils.aws import aws_models
KhBJv=super
KhBJR=None
KhBJF=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  KhBJv(LambdaLayer,self).__init__(arn)
  self.cwd=KhBJR
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,KhBJF,env=KhBJR):
  KhBJv(RDSDatabase,self).__init__(KhBJF,env=env)
 def name(self):
  return self.KhBJF.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
