pipeline { 
    environment { 
        registry = "dockerpratik/flask-swagger" 

      registryCredential = 'dockerpratik' 

      dockerImage = 'flask-swagger'
      
      containerName = 'flask_server'

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

      stage('Pushing our image') { 

          steps { 

              script { 

                  docker.withRegistry( '', registryCredential ) { 

                      dockerImage.push() 

                  }

              } 

          }
      }
      stage('Deploy docker run') { 

          steps {
                sh '''
                if [ ! "$(docker ps -q -f name=$containerName)" ]; then
                    if [ "$(docker ps -aq -f status=exited -f name=$containerName)" ]; then
                    # cleanup
                    docker rm $containerName
                    fi
                    if [ "$(docker ps -aq -f status=running -f name=$containerName)" ]; then
                    #stop
                    docker stop $containerName
                    # cleanup
                    docker rm $containerName
                    fi
                # run your container
                docker run -d --name flask-server -p 80:80 $registry:$BUILD_NUMBER
                fi
                '''
              } 

          }


      stage('Cleaning up') { 

          steps { 

              sh "docker rmi $registry:$BUILD_NUMBER" 

          }

      } 

  }

}