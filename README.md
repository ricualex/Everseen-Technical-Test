Build docker images using build_images.sh
Start services with docker-compose using docker/evertest.yml
DB data or log files are not mounted. Consider adding your specific host path to /app/log/ volumes section in docker/evertest.yml.
Similar test cases from test_cases.json can be found in robot/ereceiver_service.robot written in robot framework
