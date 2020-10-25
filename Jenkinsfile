pipeline { 
    environment { 
        registry = "dockerpratik/flask-swagger" 

      registryCredential = 'dockerpratik' 

      dockerImage = 'flask-swagger' 

  }

  agent any 

  stages { 

      stage('Cloning our Git') { 

          steps { 

              git 'https://github.com/pratikmm/flask-swagger.git' 

          }

      } 

      stage('Building our image') { 

          steps { 

              script { 

                  dockerImage = docker.build registry + ":$BUILD_NUMBER" 

              }

          } 

      }

      stage('Deploy our image') { 

          steps { 

              script { 

                  docker.withRegistry( '', registryCredential ) { 

                      dockerImage.push() 

                  }

              } 

          }

      } 

      stage('Cleaning up') { 

          steps { 

              sh "docker rmi $registry:$BUILD_NUMBER" 

          }

      } 

  }

}