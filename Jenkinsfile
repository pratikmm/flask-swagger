pipeline { 
    environment { 
        registry = "dockerpratik/flask-swagger" 

        registryCredential = 'dockerpratik' 

        dockerImage = 'flask-swagger'
      
        containerName = 'flask_server'

  }

  agent any 

  stages { 

      stage('Cloning Github repo') { 

          steps { 

              git 'https://github.com/pratikmm/flask-swagger.git' 

          }

      } 

      stage('Building Docker image') { 

          steps { 

              script { 

                  dockerImage = docker.build registry + ":$BUILD_NUMBER" 

              }

          } 

      }

      stage('Pushing image to Dockerhub') { 

          steps { 

              script { 

                    docker.withRegistry( '', registryCredential ) { 

                    dockerImage.push() 

                  }

              } 

          }
      }
      stage('Deeploying Docker container') { 

          steps {
                sh '''
                if [ ! "$(docker ps -q -f name=$containerName)" ]; then
                    if [ "$(docker ps -aq -f status=exited -f name=$containerName)" ]; then
                    # cleanup
                    docker rm $containerName
                    fi
                    if [ "$(docker ps -aq -f status=running -f name=$containerName)" ]; then
                    #stop
                    echo "stopping container"
                    docker stop $containerName
                    # cleanup
                    echo "removing container"
                    docker rm $containerName
                    fi
                # run your container
                docker run -d --name $containerName -p 80:80 $registry:$BUILD_NUMBER
                fi
                '''
              } 

          }


      stage('Cleaning up local docker image') { 

          steps { 

              sh "docker rmi $registry:$BUILD_NUMBER" 

          }

      } 

  }

}